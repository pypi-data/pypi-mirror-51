/**
 * memory.js - Memory include file that contains the memory handler command used
 * by handlers.js
 */


/**
 * Memory-read function for reading device's memory

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.page} (Num): page number to read from
          {command.args.address} (Num): address to read from
          {command.args.numBytes} (Num): number of bytes to read
 */
function memoryReadDataCommandHandler(session, command) {
    if (session.target.isConnected()) {
        var data;
        var data_list = new Array();
        try {
            data = session.memory.readData(command.args.page, command.args.address, 8, command.args.numBytes);

            // Convert Java Array to regular array
            for (var i=0; i < data.length; i++) {
                data_list.push(data[i]);
            }

        } catch (err) {
            return failResult(String(err));
        }
        return okResult(data_list);

    } else {
        return failResult("Target is not connected");
    }
}

/**
 * Memory-write function for writing to a device's memory

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.page} (Num): page number to write to
          {command.args.address} (Num): address to write to
          {command.args.data} (Num or Array of Nums): value(s) to write to memory
          {command.args.typeSize} (Num): bit size (default = 8 bits)
 */
function memoryWriteDataCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            if (!command.args.typeSize) {
                command.args.typeSize  = 8;
            }
            session.memory.writeData(command.args.page, command.args.address, command.args.data, command.args.typeSize);
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}

/**
 * Read-Register function for reading device's register

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.name} (String): register name
 */
function memoryReadRegisterCommandHandler(session, command) {
    if (session.target.isConnected()) {
        var data;
        try {
            data = session.memory.readRegister(command.args.name);

        } catch (err) {
            return failResult(String(err));
        }
        return okResult(data);

    } else {
        return failResult("Target is not connected");
    }
}

/**
 * Write-register function for writing to device's register

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.name} (String): register name
          {command.args.value} (Num): value to write to register
 */
function memoryWriteRegisterCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            session.memory.writeRegister(command.args.name, command.args.value);
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}

/**
 * Verify function for verifying an image in a device's memory

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.file} (String): the path to the image to verify
          {command.args.binary} (Boolean): use binary verify (default = false)
          {command.args.address} (Num): Address to verify binary image (required if binary = true)
 */
function verifyCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            if (command.args['binary'] == true) {
                session.memory.verifyBinaryProgram(command.args.file, command.args.address);
            } else {
                session.memory.verifyProgram(command.args.file);
            }
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}
