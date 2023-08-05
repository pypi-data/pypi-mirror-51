/**
 * erase.js - Erase include file that contains the erase handler command used
 * by handlers.js
 */


/**
 * Erase function for erasing device's entire flash

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
 */
function eraseCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            session.flash.erase();
        } catch (err) {
            return failResult(String(err));
        }
        return okResult()

    } else {
        return failResult("Target is not connected");
    }
}
