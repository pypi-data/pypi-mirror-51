/* Helpers */

function failResult(message) {
    /* returns a json object for status FAIL */
    var result = { "status": "FAIL" };

    if (message != undefined) {
        result["message"] = message;
    }

    return result;
}

function okResult(data) {
    /* returns a json object for status OK */
    var result = { "status": "OK" };

    if (data != undefined) {
        result["data"] = data;
    }

    return result;
}

function createStringArray(javaArray) {
    var arr = []
    for (var i = 0; i < javaArray.length; i++) {
        arr.push(String(javaArray[i]));
    }

    return arr;
}
