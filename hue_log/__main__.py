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
"""
import os
import sys

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


bridge = get_bridge()
