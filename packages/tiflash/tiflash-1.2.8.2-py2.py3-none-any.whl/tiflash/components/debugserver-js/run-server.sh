#!/bin/bash
SCRIPT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
ENTRY_POINT="${SCRIPT_PATH}/test.js"

### Windows:
#CCS_EXE_PATH=C:/ti/ccsv8/eclipse/eclipsec.exe
### Linux:
#CCS_EXE_PATH=/opt/ti/ccsv8/eclipse/eclipse
### MacOS:
CCS_EXE_PATH=/Applications/ti/ccsv8/eclipse/Ccstudio.app/Contents/MacOS/ccstudio


# Arg1: port number to use
if [ $# -eq 0 ]; then
    PORT=0
else
    PORT=$1
fi

DSS_SCRIPTING_ROOT="${SCRIPT_PATH}" $CCS_EXE_PATH -noSplash -application com.ti.ccstudio.apps.runScript -ccs.script $ENTRY_POINT -ccs.rhinoArgs $PORT
