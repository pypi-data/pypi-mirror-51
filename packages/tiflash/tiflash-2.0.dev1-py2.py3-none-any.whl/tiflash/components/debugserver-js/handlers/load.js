/**
 * load.js - Load include file that contains the load handler command used
 * by handlers.js
 */


/**
 * Load function for loading an image into a device's flash

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.file} (String): the path to the image to load
          {command.args.binary} (Boolean): use binary load (default = false)
          {command.args.address} (Num): Address to load binary image (required if binary = true)
 */
function loadCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            if (command.args['binary'] == true) {
                session.memory.loadBinaryProgram(command.args.file, command.args.address);
            } else {
                session.memory.loadProgram(command.args.file);
            }
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}

/**
 * Multiload function for loading images into a device's flash

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args} (Array): List of JSON objects containing flashing parameters
          {command.args.element.file} (String): the path to the image to load
          {command.args.element.binary} (Boolean): use binary load (default = false)
          {command.args.element.address} (Num): Address to load binary image (required if binary = true)
 */
function multiloadCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            if (command.args['binary'] == true) {
                session.memory.loadBinaryProgram(command.args.file, command.args.address);
            } else {
                session.memory.loadProgram(command.args.file);
            }
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}
