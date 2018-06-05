# tdtool-improved
This is a reimplementation `tdtool` using python for usage with Tellstick USB devices.
Compared to the original tool provided by Telldus this also enable detection of new devices similar to the GUI, Telldus Center. (Use: `tdtool-improved --event`)

This tool has originally been written by David Karlsson and have been slightly modified and mirrored on github to be integrated into [openhabian](https://github.com/openhab/openhabian/pull/390). The original repository can be found [here on bitbucket](https://bitbucket.org/davka003/pytelldus/).

## Installation
1. Make sure that a python envoriment is up and running on your system.
2. Copy the python script to a suitable place e.g. `/opt/tdtool-improved/`
3. Make `tdtool-improved.py` executable `chmod +x /opt/tdtool-improved/tdtool-improved.py`
4. Add the tool to your path by symlink it `ln -sf /opt/tdtool-improved/tdtool-improved.py /usr/bin/tdtool-improved`

## Usage
```
$ tdtool-improved -h
Usage: Support one of the following arguments (except --dimlevel that is allways allowed but ignored in all other cases than combined with --dim).

Options:
  -h, --help            show this help message and exit
  -l, --list            List currently configured devices
  -n on, --on=on        Turns on device. 'device' could either be an integer
                        of the device-id, or the name of the device. Both
                        device-id and name is outputed with the --list option.
  -f off, --off=off     Turns off device. 'device' could either be an integer
                        of the device-id, or the name of the device. Both
                        device-id and name is outputed with the --list option.
  -d dim, --dim=dim     Dim device. 'device' could either be an integer of the
                        device-id, or the name of the device. Both device-id
                        and name is outputed with the --list option. Note: The
                        dimlevel parameter must also be set on the commandline
  -v level, --dimlevel=level
                        Set dim level. 'level' should be an integer, 0-255.
                        Note: This parameter also requires the --dim/-d for
                        anything to happen.
  -b bell, --bell=bell  Sends bell command to devices supporting this.
                        'device' could either be an integer of the device-id,
                        or the name of the device. Both device-id and name is
                        outputed with the --list option.
  -e learn, --learn=learn
                        Sends a special learn command to devices supporting
                        this. This is normaly devices of 'selflearning' type.
                        'device' could either be an integer of the device-id,
                        or the name of the device. Both device-id and name is
                        outputed with the --list option.
  -t, --event           Listen for events untill interrupted by ctrl-c
```
## Licence
MIT