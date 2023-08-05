/**
 * evaluate.js - Evaluate include file that contains the evaluate command handler used
 * by handlers.js
 */


/**
 * Evaluate function for evaluating expressions

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
 */
function evaluateCommandHandler(session, command) {
    if (session.target.isConnected()) {
        var data;
        try {
            // Load symbols file if provided
            if (command.args.file) {
                session.symbol.load(command.args.file);
            }

            data = session.expression.evaluate(command.args.expression);
        } catch (err) {
            return failResult(String(err));
        }
        return okResult(data)

    } else {
        return failResult("Target is not connected");
    }
}
