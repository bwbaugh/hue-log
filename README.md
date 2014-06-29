hue-log
=======

Log to a journal the state of each Philips Hue light as they change
throughout the day.

Usage
-----

### Configuration

Before running, the program must first be configured.

#### First time setup

1.  Execute `make` in order to set up the virtual environment.
2.  Activate the virtual environment e.g., `source venv/bin/activate`.
3.  Specify the IP address of the bridge in the `BRIDGE_IP` environment
    variable.
4.  Press the home button on the bridge before starting the program,
    which is needed so that the program can register with the bridge
    for authentication purposes.

#### Verbose output

Optionally, set the `VERBOSE` environment variable to `1` in order to
log the full api dictionary whenever a log is emitted, otherwise only
relevant data will be outputted i.e., light state and timestamps.

### Running the program

Execute `python -m hue_log` to start the program.

The log will be written to standard out, so feel free to redirect the
output to the log file that should be used.
