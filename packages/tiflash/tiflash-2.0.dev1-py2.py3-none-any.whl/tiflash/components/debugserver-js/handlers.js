load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/erase.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/reset.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/load.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/evaluate.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/memory.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/options.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/operations.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers/target.js");

sessionHandlers = {
    "erase": eraseCommandHandler,
    "reset": resetCommandHandler,
    "load": loadCommandHandler,
    "verify": verifyCommandHandler,
    "evaluate": evaluateCommandHandler,
    "readData": memoryReadDataCommandHandler,
    "writeData": memoryWriteDataCommandHandler,
    "readRegister": memoryReadRegisterCommandHandler,
    "writeRegister": memoryWriteRegisterCommandHandler,
    "setOption": setOptionCommandHandler,
    "getOption": getOptionCommandHandler,
    "performOperation": performOperationCommandHandler,
    "printSupportedOperations": printSupportedOperationsCommandHandler,
    "run": runCommandHandler,
    "halt": haltCommandHandler,
}
