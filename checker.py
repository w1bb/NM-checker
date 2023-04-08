#!/usr/bin/python

# =========================== [ MIT License Notice ] ===========================
#
# Copyright (c) 2023 Valentin-Ioan VINTILĂ
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ==============================================================================

CHECKER_PATH = "checker"
JSON_CONFIG_PATH = f"{CHECKER_PATH}/config.json"

import json
import sys
import os

# This function will read the checker configuration from a given JSON file and
# save the info in specific variables.
# - - -
# Params: filename = A path to the JSON config file.
# - - -
# Returns: json_config
def read_configuration(filename):
    if os.path.isfile(filename) == False:
        return None
    fjson = open(filename, "r")
    json_config = json.load(fjson)
    return json_config

# This function will check that the provided JSON configuration is valid.
# - - -
# Params: json_config = The JSON configuration that shall be applied.
# - - -
# Returns: True iff no problem occured, False otherwise
def check_configuration(json_config):
    # Check the JSON file itself (through json_config)
    if not 'test-groups' in json_config:
        print("[ FATAL:JSON ] Missing 'test-groups'. Please check the JSON file for errors.")
        return False
    if type(json_config['test-groups']) != type([]):
        print("[ FATAL:JSON ] 'test-groups' must be a list. Please check the JSON file for errors.")
        return False
    for test_group in json_config['test-groups']:
        if type(test_group) != type({}):
            print("[ FATAL:JSON ] Each test group must be a dict (use {}). Please check the JSON file for errors.")
            print(f"[ FATAL:JSON ] The problem was encountered for {test_group}")
            return False
        if not 'name' in test_group:
            print("[ FATAL:JSON ] Each test group must contain a 'name' field. Please check the JSON file for errors.")
            print(f"[ FATAL:JSON ] The problem was encountered for {test_group}")
            return False
        if not 'folder' in test_group:
            print("[ FATAL:JSON ] Each test group must contain a 'folder' field. Please check the JSON file for errors.")
            print(f"[ FATAL:JSON ] The problem was encountered for {test_group}")
            return False
        if not 'expected-file' in test_group:
            print("[ FATAL:JSON ] Each test group must contain a 'expected-file' field. Please check the JSON file for errors.")
            print(f"[ FATAL:JSON ] The problem was encountered for {test_group}")
            return False
        if not 'tests' in test_group:
            print("[ FATAL:JSON ] Each test group must contain a 'tests' field. Please check the JSON file for errors.")
            print(f"[ FATAL:JSON ] The problem was encountered for {test_group}")
            return False
        if type(test_group['tests']) != type([]):
            print("[ FATAL:JSON ] The 'test' field inside a test group must be a list. Please check the JSON file for errors.")
            print(f"[ FATAL:JSON ] The problem was encountered for {test_group}")
            return False
        for test in test_group['tests']:
            if type(test) != type({}):
                print("[ FATAL:JSON ] Each test inside a test group must be a dict (use {}). Please check the JSON file for errors.")
                print(f"[ FATAL:JSON ] The problem was encountered inside the '{test_group['name']}' test group: {test}")
                return False
            if not 'name' in test:
                print("[ FATAL:JSON ] Each test inside a test group must contain a 'name' field. Please check the JSON file for errors.")
                print(f"[ FATAL:JSON ] The problem was encountered inside the '{test_group['name']}' test group: {test}")
                return False
            if not 'test-score' in test:
                print("[ FATAL:JSON ] Each test inside a test group must contain a 'name' field. Please check the JSON file for errors.")
                print(f"[ FATAL:JSON ] The problem was encountered inside the '{test_group['name']}' test group: {test}")
                return False

    # Check the subfiles and subfolders
    for test_group in json_config['test-groups']:
        expected_dir = f"{CHECKER_PATH}/{test_group['folder']}"
        if not os.path.isdir(expected_dir):
            print(f"[ FATAL:DIR ] Missing folder for test group '{test_group['name']}' (expected '{expected_dir}')")
            return False
        for test in test_group['tests']:
            expected_subdir = f"{expected_dir}/{test['name']}"
            if not os.path.isdir(expected_subdir):
                print(f"[ FATAL:SUBDIR ] Missing subfolder for test group '{test_group['name']}' / test '{test['name']}' (expected '{expected_subdir}')")
                return False
            test_file = f"{expected_subdir}/test.m"
            if not os.path.isfile(test_file):
                print(f"[ FATAL:TEST ] Missing 'test.m' for test group '{test_group['name']}' / test '{test['name']}' (expected '{test_file}')")
                return False

    # All went well
    return True

# This function runs a given test.
# - - -
# Params: test = The test that shall be run
# - - -
# Returns: (percent, msg), where:
#          percent = A score from 0 to 1
#          msg = A text description of the final result
def run_test(test):
    percent = 0
    msg = "OK"

    return (percent, msg)

# This function will go through each test of a group individually. Output shall
# be provided throughout the whole process.
def run_test_group(test_group):
    None

# This function will go through each test group individually and mark them
# accordingly. Output shall be provided throughout the whole process.
def run_all_test_groups():
    None

# Checker's true entrypoint
def main(arguments):
    # Check for the checker folder
    if not os.path.isdir("checker"):
        print(f"[ FATAL ] Missing 'checker' folder!")
        return -1
        
    # Get the JSON config
    json_config = read_configuration(JSON_CONFIG_PATH)
    if json_config == None:
        print(f"[ FATAL ] Missing JSON config file (expected '{JSON_CONFIG_PATH}')!")
        return -1
    
    # Check the config
    if check_configuration(json_config) == False:
        print(f"[ FATAL ] JSON config ('{JSON_CONFIG_PATH}') is invalid!")
        return -1
    print(json_config)

# Pass control to the main() function
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))