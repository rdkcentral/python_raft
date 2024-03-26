#!/bin/bash

MY_PATH="`dirname \"${BASH_SOURCE[0]}\"`"
python_venv=$MY_PATH/VENV

venv_check=$(dpkg --list | grep python3-venv)
if [ -z "$venv_check" ]; then
    echo "Please install python3-venv with the following command"
    echo "sudo apt install -y python3-venv"
    exit
fi

if [ -d "$python_venv" ] && [ -e "$python_venv"/bin/activate ];then
    . "$python_venv"/bin/activate
    pip install -qr $MY_PATH/requirements.txt
else
    rm -rf "$python_venv"
    mkdir -p "$python_venv"
    python3 -m venv "$python_venv"
    if [ "$?" != "0" ];then
        echo "The python virtual environment could not be created"
    fi
    . "$python_venv"/bin/activate
    pip install -qr $MY_PATH/requirements.txt
fi

