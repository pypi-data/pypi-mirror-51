// Import the DSS packages into our namespace to save on typing
importPackage(Packages.com.ti.debug.engine.scripting);
importPackage(Packages.com.ti.ccstudio.scripting.environment);
importPackage(Packages.java.lang);
importClass(java.lang.Thread,java.lang.Runnable,java.lang.System);
importPackage(Packages.org.mozilla.javascript);

// Import necessary packages for network interaction.
importPackage(java.net);
importPackage(java.io);

load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/utils/json2.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/utils/helpers.js");

function DebugServer(cfg, socket) {

    this.configPath = null;
    this.serverSocket = socket;
    this.serverPort = socket.getLocalPort();

    this.script = ScriptingEnvironment.instance();

    this.debugServer = this.script.getServer("DebugServer.1");
    this.ccsServer = undefined;

    if (cfg.ccxml != undefined) {
        this.debugServer.setConfig(cfg.ccxml);
        this.configPath = cfg.ccxml;
    }

    if (cfg.debug == true) {
        this.script.traceSetConsoleLevel(TraceLevel.ALL);
    }

    this.debugSessions = {};

    this.serverHandlers = {
        "setTimeout": setTimeoutCommandHandler,
        "getTimeout": getTimeoutCommandHandler,
        "setConsoleLevel": setConsoleLevelCommandHandler,
        "setConfig": setConfigCommandHandler,
        "getConfig": getConfigCommandHandler,
        "createConfig": createConfigCommandHandler,
        "getListOfCPUs": getListOfCPUsCommandHandler,
        "getListOfDevices": getListOfDevicesCommandHandler,
        "getListOfConnections": getListOfConnectionsCommandHandler,
        "getListOfConfigurations": getListOfConfigurationsCommandHandler,
        "attachCCS": attachCCSCommandHandler,
        "openSession": openSessionCommandHandler,
        "getListOfSessions": getListOfSessionsCommandHandler,
        "terminateSession": terminateSessionCommandHandler,
        "killServer": killServerCommandHandler,
    };

    this.sessionHandlers = {
        "connect": connectCommandHandler,
        "disconnect": disconnectCommandHandler,
        "stop": stopCommandHandler,
    };

}

DebugServer.prototype.addServerHandlers = function(handlers) {
    for (var command in handlers) {
        this.serverHandlers[command] = handlers[command];
    }
}

DebugServer.prototype.addSessionHandlers = function(handlers) {
    for (var command in handlers) {
        this.sessionHandlers[command] = handlers[command];
    }
}

DebugServer.prototype.run = function() {
    var keepRunning = true;
    while (keepRunning) {

        print("Waiting for connections...");
        var client = this.serverSocket.accept();

        var input = new BufferedReader(new InputStreamReader(client.getInputStream()));
        var output = new PrintWriter(client.getOutputStream(), true);
        var line = input.readLine();

        while (line != null) {  /* Exits once port is closed by client */

            var result;
            var response = line;
            print("Received: " + response);

            var command = undefined;
            try {
                command = JSON.parse(response);
            } catch (e) {
                result = failResult("Invalid JSON format: '" + line + "'");
            }


            if (command) {
              if (!command.name) {
                /* No command name specified */
                result = failResult("No command name specified");
              } else {

                try {
                    result = this.handleServerCommand(command);

                    /* Kill Server on request */
                    if (command.name == "killServer") {
                        keepRunning = false;
                    }
                } catch (err) {
                    result = failResult(command.name + ": " + err.message);
                }
              }
            }

            var result_str = JSON.stringify(result);
            print("Result JSON: " + result_str);
            output.println(result_str);

            line = input.readLine();
        }
        input.close();
        output.close();
        client.close();
    }
}

DebugServer.prototype.shutdown = function() {
    for (var session in this.debugSessions) {
        this.terminateSession(session);
    }
    this.debugServer.stop();
}

DebugServer.prototype.handleServerCommand = function(command) {
    /* Make sure command exists */
    if (!(server.serverHandlers[command.name])) {
        return failResult("Invalid command: " + command.name);
    }

    /* return status of running command */
    return server.serverHandlers[command.name](this, command);
}

/* Server Commands */

function setTimeoutCommandHandler(server, command) {
    server.script.setScriptTimeout(command.args.timeout);
    return okResult();
}

function getTimeoutCommandHandler(server, command) {
    var timeout = server.script.getScriptTimeout();
    return okResult(timeout);
}

function killServerCommandHandler(server, command) {
    server.shutdown();
    return okResult();
}

function setConsoleLevelCommandHandler(server, command) {
    server.script.traceSetConsoleLevel(TraceLevel[command.args.level]);
    return okResult();
}

function setConfigCommandHandler(server, command) {
    var result;
    if (!(command.args.path)) {
        result = failResult(command.name + ": Missing path field");
    } else {
        f = new File(command.args.path)
        if (f.isFile()) {
            server.debugServer.setConfig(command.args.path);
            server.configPath = command.args.path;
            result = okResult();
        } else {
            result = failResult(command.name + ": Cannot find config file - " + command.args.path);
        }
    }

    return result;
}

function getConfigCommandHandler(server, command) {
    var data = server.configPath;
    var result = okResult(data);

    return result;
}

function createConfigCommandHandler(server, command) {
    var result;
    if (!(command.args.connection)) {
        result = failResult(command.name +": Missing 'connection' argument");
    } else if (!(command.args.board) && !(command.args.device)) {
        result = failResult(command.name +": Missing 'board' or 'device' argument");
    } else if (!(command.args.name)) {
        result = failResult(command.name +": Missing 'name' argument");
    } else {
        var cfgGen = server.debugServer.createTargetConfigurationGenerator();

        //  Set Directory to place new configuration
        if (command.args.directory) {
            cfgGen.setOutputDirectory(command.args.directory);
        }

        //  Set Connection
        cfgGen.setConnection(command.args.connection);

        // Set Board
        if (command.args.board) {
            cfgGen.setBoard(command.args.board);
        }

        // Set Device
        if (command.args.device) {
            cfgGen.setDevice(command.args.device);
        }

        //  Generate Config file
        cfgGen.createConfiguration(command.args.name);

        var outputDirectory = cfgGen.getOutputDirectory();

        result = okResult({"directory": String(outputDirectory), "name": String(command.args.name)});
    }

    return result;
}

function getListOfCPUsCommandHandler(server, command) {
    var result;
    if (server.configPath == null) {
        result = failResult(command.name + ": CCXML must be set before retreiving a list of CPUs");
    } else {
        var cpu_list = createStringArray(server.debugServer.getListOfCPUs());

        result = okResult(cpu_list)
    }

    return result;
}

function getListOfDevicesCommandHandler(server, command) {
    var result;
    if (server.configPath == null) {
        result = failResult(command.name + ": CCXML must be set before retreiving a list of devices");
    } else {
        var configGenerator = server.debugServer.createTargetConfigurationGenerator();
        var dev_list = createStringArray(configGenerator.getListOfDevices());

        result = okResult(dev_list)
    }

    return result;
}

function getListOfConnectionsCommandHandler(server, command) {
    var result;
    if (server.configPath == null) {
        result = failResult(command.name + ": CCXML must be set before retreiving a list of connections");
    } else {
        var configGenerator = server.debugServer.createTargetConfigurationGenerator();
        var conn_list = createStringArray(configGenerator.getListOfConnections());

        result = okResult(conn_list)
    }

    return result;
}

function getListOfConfigurationsCommandHandler(server, command) {
    var result;
    if (server.configPath == null) {
        result = failResult(command.name + ": CCXML must be set before retreiving a list of devices");
    } else {
        var configGenerator = server.debugServer.createTargetConfigurationGenerator();
        var cfg_list = createStringArray(configGenerator.getListOfConfigurations());

        result = okResult(cfg_list)
    }

    return result;
}

function attachCCSCommandHandler(server, command) {
    var result;
    if (server.configPath == null) {
        result =  failResult(command.name + ": CCXML must be set before retreiving a list of devices");
    } else if (server.ccsServer != undefined) {
        result = failResult(command.name + ": CCS instance has already been attached");
    } else {
        try {
            server.ccsServer = server.script.getServer("CCSServer.1");
            server.ccsServer.openSession(".*");
            result = okResult()
        } catch (err) {
            result = failResult(String(err));
        }
    }

    return result;
}

function openSessionCommandHandler(server, command) {
    /* Check if session already exists/opened */
    var result;
    var sessionName = command.args.name;
    if (server.debugSessions[sessionName]) {
        result = failResult("Session: " + sessionName + " already exists");
    } else {
        /* Open socket */
        var socket = ServerSocket(0);   //  Have Java automatically allocate the port
        var port = socket.getLocalPort();

        /* Add session object */
        server.debugSessions[sessionName] = {};

        /* Open Session */
        server.debugSessions[sessionName]["handle"] = server.debugServer.openSession(sessionName);

        /* Set port */
        server.debugSessions[sessionName]["port"] = port;

        /* Set socket */
        server.debugSessions[sessionName]["socket"] = socket;

        /* Start Session Thread */
        server.debugSessions[sessionName]["thread"] = server.createSessionThread(socket, server.debugSessions[sessionName]["handle"]);
        server.debugSessions[sessionName]["thread"].start();

        /* Set data message to send back */
        var data = {"name": sessionName, "port": port};

        result = okResult(data);
    }

    return result;
}

function getListOfSessionsCommandHandler(server, command) {
    var listOfSessions = [];

    for (var session in server.debugSessions) {
        listOfSessions.push({"name": session, "port": server.debugSessions[session]['port']});
    }

    return okResult(listOfSessions);
}

DebugServer.prototype.terminateSession = function (sessionName) {
    //  Close socket
    if (!server.debugSessions[sessionName]["socket"].isClosed()) {
        server.debugSessions[sessionName]["socket"].close();
    }

    if (server.debugSessions[sessionName]["thread"].isAlive() ) {
        //server.debugSessions[sessionName]["thread"].interrupt();
        server.debugSessions[sessionName]["thread"].join();
    }

    server.debugSessions[sessionName]["handle"].terminate();
    delete server.debugSessions[sessionName];
}


function terminateSessionCommandHandler(server, command) {
    var result;
    var sessionName = command.args.name;
    if (!(server.debugSessions[sessionName])) {
        result = failResult("Session: " + sessionName + " does not exist");
    } else {
        server.terminateSession(sessionName);
        result = okResult();
    }

    return result;
}

DebugServer.prototype.createSessionThread = function (socket, session) {
    var server = this;
    return new Thread(
        new Runnable() {
          run: function() {
              var keep_running = true;
              while (keep_running) {

                  try { /* Catch socket.close() from Server 'terminate' function */
                    var client = socket.accept();
                  } catch (err) {
                      keep_running = false;
                      break;
                  }
                var input  = new BufferedReader(new InputStreamReader(client.getInputStream()));
                var output = new PrintWriter(client.getOutputStream(), true);
                print(">>>>> Accepted connection :["+client+"]");

                /* We keep reading commands from the socket until the socket is closed by the client. */
                var line = input.readLine();
                while (line != null) {  /* Exits only once port is closed by client */
                    print('COMMAND: ' + line);
                    /* The line should contain a JSON-encoded string */
                    try {
                       var command = JSON.parse(line);
                    } catch (err) {
                        /* Here we catch any execution error that may occur during the handler execution. */
                        var response = failResult("failed while parsing JSON command: " + err.description);
                        output.println(response);
                        command = undefined;
                    }

                    if (command) {
                      /* We do a basic sanity-check on the command before calling the appropriate handler. */
                      if (!command.name) {
                        /* No command name specified */
                        var response = failResult("No command name specified");
                      } else if (!(server.sessionHandlers[command.name])) {
                        /* Command name specified is not among the supported commands */
                        var response = failResult(command.name + ": unsupported command");
                      } else {
                        try {
                            /* We start by running the handler. */
                            var result = server.sessionHandlers[command.name](session, command);
                            /* Special case for the stop command, we set keep_running to false. */
                            if (command.name == "stop") {
                                keep_running = false;
                            }

                            /* Send back to the client a JSON-encode result, on one line. */
                            var response = JSON.stringify(result);
                        } catch (err) {
                            /* Here we catch any execution error that may occur during the handler execution. */
                            var response = failResult(command.name + ": exception - " + err.description);
                        }
                      }
                    print("RESPONSE: " + response);
                    output.println(response);
                    }
                    line = input.readLine();
                }

                /* We are done with this client, therefore we release all the resources allocated. */
                input.close();
                output.close();
                print(">>>>> Closed connection :["+client+"]");
                client.close();


                /* Detect if the target is still running, and halt it */
                if ( (session.target.isConnected()) && (!session.target.isHalted()) ){
                    session.target.halt();
                }

                if (session.target.isConnected()) {
                    session.target.disconnect();
                }
              }
            }
          }
     );
}




/* Session Commands */

function connectCommandHandler(session, command) {
    /* Connect to the target */
    if (!session.target.isConnected()) {
        try {
            session.target.connect();
        } catch (err) {
            return failResult(String(err));
        }
        return okResult();

    } else {
        return failResult("Target is already connected");
    }
}

function disconnectCommandHandler(session, command) {
    /* Disconnect to the target */
    if (session.target.isConnected()) {
        try {
            session.target.disconnect();
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}

function stopCommandHandler(session, command) {
    return okResult();
}
