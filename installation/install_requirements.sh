#!/usr/bin/env bash
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component's LICENSE file the
# * following copyright and licenses apply:
# *
# * Copyright 2023 RDK Management
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *
# http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *
#* ******************************************************************************

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

