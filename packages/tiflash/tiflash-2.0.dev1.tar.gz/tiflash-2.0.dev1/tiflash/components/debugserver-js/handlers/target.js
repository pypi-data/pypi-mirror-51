/**
 * target.js - Target include file that contains the many target specific
 * command handlers used by handlers.js
 */


/**
 * Run function for issuing a run command to a target

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.async} (Boolean): run and return control immediately (default = false)
 */
function runCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            if (command.args && command.args.asynchronous) {
                session.target.runAsynch();
            } else {
                session.target.run();
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
 * Halt function for issuing a halt command to a target

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.wait} (Boolean): wait until target has been halted (default = false)
 */
function haltCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            session.target.halt();
            if (command.args.wait) {
                session.target.waitForHalt();
            }
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}
