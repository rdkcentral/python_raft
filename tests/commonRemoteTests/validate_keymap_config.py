#!/usr/bin/env python3
#** *****************************************************************************
# *
# * If not stated otherwise in this file or this component"s LICENSE file the
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

import argparse
import os
import sys

import yaml

# Add the framework path to system
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../../")

from framework.core.rcCodes import rcCode as rc


class ArgParser(argparse.ArgumentParser):

    def __init__(self):
        super().__init__()
        self.add_argument("keymap_file",
                          action = "store",
                          help = "Keymap file to validate",
                          metavar = "KEYMAP_FILe")
        self.add_argument("--map-name",
                          action = "store",
                          help = "Individual key map in the file to validate, selected by name.",
                          dest = "keymap_name",
                          default = None)
        self.add_argument("--map-index",
                          action = "store",
                          help = "Individual key map in the file to validate, selected by index.",
                          dest = "keymap_index",
                          default = None,
                          type = int)
        self._args = self.parse_args()

    @property
    def keymap_file(self):
        return self._args.keymap_file

    @property
    def keymap_name(self):
        return self._args.keymap_name

    @property
    def keymap_index(self):
        return self._args.keymap_index
    
class MissingNameError(BaseException):
    msg = "The keymap does not have a name set."

class MissingCodesError(BaseException):

    def __init__(self,name:str):
        super().__init__()
        self.msg = f"The keymap {name} has no codes set."

class CodesTypeError(BaseException):

    def __init__(self, name:str):
        super().__init__()
        self.msg = f"Keymap [{name}]'s codes section not valid\n" \
                    "The codes key must have a dictionary value e.g.\n" \
                    "codes:\n  NUM_0: \"ZERO\"\n  NUM_1: \"ONE\""

class InvalidCodesError(BaseException):
    _deprecated_keys = {
        "ANTENNA_CABLE": "ANTENNA",
        "AUDDESC": "AUD_DESC",
        "BACKUP": "BACK",
        "BOXOFF": "POWER",
        "CIP": "CI_PLUS",
        "DOWN" : "ARROW_DOWN",
        "FFWD": "FFORWARD",
        "FORWARD": "FFORWARD",
        "LEFT": "ARROW_LEFT",
        "POWEROFF": "POWER",
        "POWERON": "POWER",
        "PREVPROG": "PREV_CH",
        "PRE_CH": "PREV_CH",
        "RIGHT": "ARROW_RIGHT",
        "RST": "RESET",
        "SUBT": "SUBTITLE",
        "TV": "SOURCE",
        "UNPAIRED": "PICK_UP",
        "UP": "ARROW_UP",
        "VOL_BUZZ": "VOL_DOWN",
        "VOL_MAX": "VOL_UP"
    }

    def __init__(self,name: str, invalid_codes: list):
        super().__init__()
        self.msg = ""
        self._substitutions = []
        for code in invalid_codes:
            if code in self._deprecated_keys.keys():
                self._substitutions.append(f"{code} => {self._deprecated_keys.get(code)}")
                invalid_codes.remove(code)
        self._invalid_codes = invalid_codes
        if len(self._invalid_codes) > 0:
            self.msg += f"The following codes in keymap [{name}] are not valid:\n\t" + "\n\t".join(self._invalid_codes)
        if len(self._substitutions) > 0:
            if len(self.msg) > 0:
                self.msg += "\n"
            self.msg += f"The follow codes in keymap [{name}] have been deprecated.\nBelow are possible substitutions:\n\t" \
                        + "\n\t".join(self._substitutions)

def validate_keymap(keymap_dict):
    map_name = keymap_dict.get("name",None)
    if map_name is None:
        raise MissingNameError()
    codes = keymap_dict.get("codes", None)
    if codes is None:
        raise MissingCodesError(map_name)
    if not isinstance(codes, dict):
        raise CodesTypeError(map_name)
    failed_codes = []
    valid_codes = dir(rc)
    for key in codes.keys():
        if key not in valid_codes:
            failed_codes.append(key)
    if failed_codes:
        raise InvalidCodesError(map_name, failed_codes)
    print(f"Keymap [{map_name}] is valid.")

def validate_keymaps(keymaps_list):
    passed = True
    for index, map in enumerate(REMOTE_MAPS):
        try:
            validate_keymap(map)
        except MissingNameError as e:
            print(f"Keymap at index {index} does not have a name set")
            passed = False
        except(MissingCodesError, CodesTypeError, InvalidCodesError) as e:
            print(e.msg)
            passed = False
    return passed

if __name__ == "__main__":
    ARGS = ArgParser()
    try:
        with open(ARGS.keymap_file, "r", encoding="utf-8") as KEYMAP_FILE:
            KEYMAPS = yaml.load(KEYMAP_FILE, yaml.SafeLoader)
    except Exception as e:
        print(f"Cannot open specified keymap file. [{ARGS.keymap_file}]:\n{e}")
        raise SystemExit(1)
    REMOTE_MAPS = KEYMAPS.get("remoteMaps",{})
    if isinstance(REMOTE_MAPS,dict):
        REMOTE_MAPS = list(map(lambda x: REMOTE_MAPS.get(x),REMOTE_MAPS.keys()))
    if ARGS.keymap_name:
        found_keymap = list(filter(lambda x: x.get("name") == ARGS.keymap_name, REMOTE_MAPS))
        if found_keymap:
            try:
                validate_keymap(found_keymap[0])
                raise SystemExit(0)
            except (MissingNameError,
                    MissingCodesError,
                    CodesTypeError,
                    InvalidCodesError) as e:
                print(e.msg)
                raise SystemExit(1)
        else:
            print(f"No keymap found with the name [{ARGS.keymap_name}]")
            raise SystemExit(1)
    if isinstance(ARGS.keymap_index, int):
        try:
            found_keymap = REMOTE_MAPS[ARGS.keymap_index]
        except IndexError:
            print(f"Map index provided [{ARGS.keymap_index}] out of range for keymap file")
            raise SystemExit(1)
        try:
            validate_keymap(found_keymap)
            raise SystemExit(0)
        except (MissingNameError,
                MissingCodesError,
                CodesTypeError,
                InvalidCodesError) as e:
            print(e.msg)
            raise SystemExit(1)
    if validate_keymaps(REMOTE_MAPS) is False:
        raise SystemExit(1)


