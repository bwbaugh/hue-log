hue-log
=======

Log to a journal the state of each Philips Hue light as they change
throughout the day.

Usage
-----

### First time setup

1.  Execute `make` in order to set up the virtual environment.
2.  Activate the virtual environment e.g., `source venv/bin/activate`.
3.  Specify the IP address of the bridge in the `BRIDGE_IP` environment
    variable.
4.  Press the home button on the bridge before starting the program,
    which is needed so that the program can register with the bridge
    for authentication purposes.

### Running the program

Execute `python -m hue_log` to start the program.
