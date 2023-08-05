/**
 * options.js - Options include file that contains the option handler commands used
 * by handlers.js
 */


/**
 * Set-Option function for setting an option for device

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.id} (String): option ID to set
          {command.args.value} (String): value to set option ID to
 */
function setOptionCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            var optionType = String(session.options.getValueType(command.args.id));

            switch(optionType) {
                case "string":
                    session.flash.options.setString(command.args.id, command.args.value);
                    break;
                case "boolean":
                    session.flash.options.setBoolean(command.args.id, command.args.value);
                    break;
                case "numeric":
                    session.flash.options.setNumeric(command.args.id, command.args.value);
                    break;
                default:
                    throw("Invalid option type: " + String(optionType));
                    break;
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
 * Get-Option function for getting an option value from device

 * @param {session} DSS Session object
 * @param {command} JSON object containing command name and args
          {command.args.id} (String): option ID to get
 */
function getOptionCommandHandler(session, command) {
    if (session.target.isConnected()) {
        try {
            var optionType = String(session.options.getValueType(command.args.id));
            var value;

            switch(optionType) {
                case "string":
                    value = session.flash.options.getString(command.args.id);
                    break;
                case "boolean":
                    value = session.flash.options.getBoolean(command.args.id);
                    break;
                case "numeric":
                    value = session.flash.options.getNumeric(command.args.id);
                    break;
                default:
                    throw("Invalid option type: " + optionType);
                    break;
            }

        } catch (err) {
            return failResult(String(err));
        }

        //  Convert to string type if not boolean
        if (typeof(value) == "object") {
            value = String(value);
        }

        return okResult(value);

    } else {
        return failResult("Target is not connected");
    }
}
