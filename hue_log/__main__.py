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

Optionally, set the `VERBOSE` environment variable to `1` in order to
log the full api dictionary whenever a log is emitted, otherwise only
relevant data will be outputted i.e., light state and timestamps.

### Running the program

Execute `python -m hue_log` to start the program.

The log will be written to standard out, so feel free to redirect the
output to the log file that should be used.
"""
import json
import os
import socket
import sys
import time

from phue import Bridge
from phue import PhueRegistrationException
from retrying import retry


# If enabled, emit the full api dict, otherwise only the relevant data.
IS_VERBOSE = bool(int(os.environ.get('VERBOSE', 0)))


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


def _is_network_exception(exception):
    return isinstance(exception, socket.error)


@retry(
    retry_on_exception=_is_network_exception,
    # Balance being robust against extended outages and crashing to
    # indicate that the program cannot function due to an extended issue.
    stop_max_delay=1000 * 60 * 60 * 12,
    wait_exponential_multiplier=1000 * 1,
    wait_exponential_max=1000 * 5,
)
def _get_api(bridge):
    """Helper to retry if there is a temporary network problem."""
    return bridge.get_api()


bridge = get_bridge()
last_light_data = None
while 1:
    try:
        api = _get_api(bridge)
        if IS_VERBOSE:
            relevant_data = api
        else:
            # TODO(bwbaugh|2014-06-28): Periodically back up the entire `api`.
            relevant_data = extract_relevant_data(api)
        current_light_data = relevant_data['lights']
        if current_light_data != last_light_data:
            # Only emit a log line if a light's state has changed.
            # NOTE: The first iteration will always emit a log line
            # since we don't have access to the state prior to when the
            # program started.
            sys.stdout.write(json.dumps(relevant_data, sort_keys=True) + '\n')
            # Make sure the line is immediately visible since it may be
            # a while before the next log line.
            sys.stdout.flush()
            last_light_data = current_light_data
        # Sleep before next read for rate limiting.
        time.sleep(5)
    except KeyboardInterrupt:
        break
