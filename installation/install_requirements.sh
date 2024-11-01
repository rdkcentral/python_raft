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
PYTHON_VENV=$MY_PATH/VENV
SUDO=0

NO_COLOR="\e[0m"
RED="\e[0;31m"
CYAN="\e[0;36m"
YELLOW="\e[1;33m"
GREEN="\e[0;32m"
RED_BOLD="\e[1;31m"
BLUE_BOLD="\e[1;34m"
YELLOW_BOLD="\e[1;33m"

DEBUG_FLAG=0
function ECHO()
{
    echo -e "$*"
}

function DEBUG()
{
    # if set -x is in use debug messages are useless as whole stript will be shown
    if [[ "$-" =~ "x" ]]; then
        return
    fi
  if [[ "${DEBUG_FLAG}" == "1" ]];then
      ECHO "${BLUE_BOLD}DEBUG: ${CYAN}$*${NO_COLOR}" > /dev/stderr
  fi
}

function INFO()
{
    ECHO "${GREEN}$*${NO_COLOR}"
}

function WARNING()
{
    ECHO "${YELLOW_BOLD}Warning: ${YELLOW}$*${NO_COLOR}" > /dev/stderr
}

function ERROR()
{
    ECHO "${RED_BOLD}ERROR: ${RED}$*${NO_COLOR}" 
    exit 1
}

function check_package_installed()
{
# Check if a given package is installed.
#
# Arguments:
#   $1: package_name: The package to check.
#
# Returns:
#   0: If package is installed.
#   1: If package is not installed.
#
    DEBUG "BEGIN: ${FUNCNAME} [$*]"
    local package_name="$1"
    DEBUG "command -v ${package_name}"
    local package_check="$(command -v ${package_name})"
    if [[ -n "${package_check}" ]]; then
        # If package check isn't empty
        return 0
    fi
    return 1
}

function version_check()
{
# Check if a version is correct or not
# Arguments:
#   $1: Version to check
#   $2: Required version
#         +: as the last character can be used to signify any version over the given number.
#         -: as the last character can be used to signify any version below the given number.
#
    DEBUG "BEGIN: ${FUNCNAME} [$*]"
    local check_version="$1"
    local required_version="$2"
    local check_version_split=(${check_version//\./" "})
    DEBUG "Version split: [${version_split[0]}]"
    local req_version_split=(${required_version//\./" "})
    local stop=$(("${#req_version_split[@]}"-1))
    DEBUG "LOOP STOP: [$stop]"
    for i in $(seq 0 ${stop})
    do
        local req_version_section="${req_version_split[$i]}"
        DEBUG "Req Version Sect: [${req_version_section}]"
        local check_version_section="${check_version_split[$i]}"
        DEBUG "Check Version Sect: [${check_version_section}]"
        case "${req_version_section}" in
            *"+")
                # Remove the + from the end of the string
                req_version_section="${req_version_section%+}"
                if [[ "$check_version_section" -ge "${req_version_section}" ]];then
                    return 0
                fi
                return 1
                ;;
            *"-")
                # Remove the - from end of the string
                req_version_section="${req_version_section%-}"
                if [[ "$check_version_section" -le "${req_version_section}" ]];then
                    return 0
                fi
                return 1
                ;;
            *)
                if [[ "${check_version_section}" != "${req_version_section}" ]];then
                    return 1
                fi
                ;;
        esac
    done
    return 0
}

##### MAIN #####

# Check for sudo rights.
if [[ -n "$(groups | grep sudo)" ]]; then
    # If sudo is in groups.
    DEBUG "SUDO=1"
    SUDO=1
fi

# Check python3 is installed.
check_package_installed python3
if [[ "$?" != "0" ]];then
    ERROR "Python 3 not found.\nPlease install python 3.10+"
fi

# Python Version check.
python_version="$(python3 --version)"
# Remove the only text before the space
version_check "${python_version##* }" "3.10+"
if [[ "$?" != "0" ]];then
    ERROR "Python version installed is too old. Version 3.10+ required"
fi

if [ -d "${PYTHON_VENV}" ] && [ -e "${PYTHON_VENV}"/bin/activate ];then
    . "${PYTHON_VENV}/bin/activate"
    pip install -qr $MY_PATH/requirements.txt
else
    rm -rf "${PYTHON_VENV}"
    mkdir -p "${PYTHON_VENV}"
    python3 -m venv "${PYTHON_VENV}"
    if [ "$?" != "0" ];then
        ERROR "The python virtual environment could not be created"
    fi
    . "${PYTHON_VENV}/bin/activate"
    pip install -qr "${MY_PATH}/requirements.txt"
fi

check_package_installed "cec-client"
if [[ "$?" != "0" ]];then
    if [[ "${SUDO}" == "1" ]];then
        sudo apt update && sudo apt install -y cec-client
    else
        WARNING "cec-client is not installed"
        WARNING "You will not be able to use the CECClient module"
    fi
fi
