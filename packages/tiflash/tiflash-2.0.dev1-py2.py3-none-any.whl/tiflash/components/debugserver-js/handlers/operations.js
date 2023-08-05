/**
 * operations.js - Operations include file that contains the operation handler commands used
 * by handlers.js
 */


/**
 * Perform-Operation function for performing a device operation

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.opcode} (String): operation code for the flash operation
 */
function performOperationCommandHandler(session, command) {
    if (session.target.isConnected()) {
        var data;
        try {
            data = session.flash.performOperation(command.args.opcode);

        } catch (err) {
            return failResult(String(err));
        }
        return okResult(data)

    } else {
        return failResult("Target is not connected");
    }
}

/**
 * Print-Operations function for printing all supported flash operations

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
 */
function printSupportedOperationsCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            session.flash.listSupportedOperations();
        } catch (err) {
            return failResult(String(err));
        }

        return okResult();

    } else {
        return failResult("Target is not connected");
    }
}
