 #!/usr/bin/env bash

if [ $0 != "bash" ];then
    echo "re-run this script with source e.g. '. ./activate.sh'"
    exit 1
fi

. ${PWD}/VENV/bin/activate
export PYTHONPATH=${PWD}/VENV/lib/python3.8/site-packages/:$PYTHONPATH


