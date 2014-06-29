# -*- coding: utf-8 -*-
"""Connects to a Philips Hue bridge and logs the state of each light.

Usage
-----

### Configuration

-   Specify the IP address of the bridge in the `BRIDGE_IP` environment
    variable.
-   If running for the first time, press the home button on the bridge
    before starting the program, which is needed so that the program
    can register with the bridge for authentication purposes.

### Running the program

Execute `python -m hue_log` to start the program.

The log will be written to standard out, so feel free to redirect the
output to the log file that should be used.
"""
import json
import os
import sys
import time

from phue import Bridge
from phue import PhueRegistrationException


def get_bridge():
    """Connect to the bridge and return the Bridge instance.

    If the environment is not configured or there is some other problem
    connecting to the bridge then the program will exit.

    Returns:
        Bridge instance.
    """
    try:
        BRIDGE_IP = os.environ['BRIDGE_IP']
    except KeyError:
        sys.stderr.write('The `BRIDGE_IP` environment variable must be set.\n')
        sys.exit(1)
    try:
        return Bridge(BRIDGE_IP)
    except PhueRegistrationException as error:
        # Inform the user that the link button wasn't pressed.
        sys.stderr.write(error.message + '\n')
        sys.exit(1)


def extract_relevant_data(api):
    """Extract relevant information from the api that should be logged.

    Args:
        api: Dictionary of the full api dictionary from the Bridge.

    Returns:
        Dictionary of the relevant information that should be logged.
        Includes the imestamp from the `api` dict in the "config".
    """
    relevant_data = {
        'config': {
            'UTC': api['config']['UTC'],
            'localtime': api['config']['localtime'],
            'timezone': api['config']['timezone'],
        },
        'lights': api['lights'],
    }
    return relevant_data


bridge = get_bridge()
last_light_data = None
while 1:
    try:
        # TODO(bwbaugh|2014-06-28): Periodically back up the entire `api`.
        api = bridge.get_api()
        relevant_data = extract_relevant_data(api)
        current_light_data = relevant_data['lights']
        if current_light_data != last_light_data:
            # Only emit a log line if a light's state has changed.
            # NOTE: The first iteration will always emit a log line
            # since we don't have access to the state prior to when the
            # program started.
            sys.stdout.write(json.dumps(relevant_data) + '\n')
            # Make sure the line is immediately visible since it may be
            # a while before the next log line.
            sys.stdout.flush()
            last_light_data = current_light_data
        # Sleep before next read for rate limiting.
        time.sleep(5)
    except KeyboardInterrupt:
        break
