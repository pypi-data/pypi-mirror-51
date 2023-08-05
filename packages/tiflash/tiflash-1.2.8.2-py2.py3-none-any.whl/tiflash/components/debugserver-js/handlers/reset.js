/**
 * reset.js - Reset include file that contains the reset handler command used
 * by handlers.js
 */


/**
 * Reset function for (board) resetting device

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
 */
function resetCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            session.target.reset();
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}
