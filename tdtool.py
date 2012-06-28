import sys
import os
import optparse
import time


if __name__ == '__main__':
    usage = """-[bdefhlnrv] [ --list ] [ --help ]
                      [ --on device ] [ --off device ] [ --bell device ]
                      [ --learn device ]
                      [ --dimlevel level --dim device ]
                      [ --raw input ]"""

    parser = optparse.OptionParser(usage = usage)
    parser.add_option("-l", "--list",
                      action="store_true", default=False,
                      help="List currently configured devices")
    parser.add_option("-n", "--on", dest="on",
                      metavar = 'on',
                      help="Turns on device. 'device' could either be an integer of the device-id, or the name of the device. Both device-id and name is outputed with the --list option.")
    parser.add_option("-f", "--off", dest="off",
                      metavar = 'off',
                      help="Turns off device. 'device' could either be an integer of the device-id, or the name of the device. Both device-id and name is outputed with the --list option.")
    parser.add_option("-d", "--dim", dest="dim",
                      metavar = 'dim',
                      help="Dim device. 'device' could either be an integer of the device-id, or the name of the device. Both device-id and name is outputed with the --list option. Note: The dimlevel parameter must also be set on the commandline")
    parser.add_option("-v", "--dimlevel", dest="dimlevel",
                      metavar = 'level',
                      help="Set dim level. 'level' should be an integer, 0-255. Note: This parameter also requires the --dim/-d for anything to happen.")
    parser.add_option("-b", "--bell", dest="bell",
                      metavar = 'bell',
                      help="Sends bell command to devices supporting this. 'device' could either be an integer of the device-id, or the name of the device. Both device-id and name is outputed with the --list option.")
    parser.add_option("-e", "--learn", dest="learn",
                      metavar = 'learn',
                      help="Sends a special learn command to devices supporting this. This is normaly devices of 'selflearning' type. 'device' could either be an integer of the device-id, or the name of the device. Both device-id and name is outputed with the --list option.")

    (options, args) = parser.parse_args()

    print options


if 0:

    print 'getNumberOfDevices() return', getNumberOfDevices()
    
    print 'Id\tName'
    for i in range(getNumberOfDevices()):
        print getDeviceId(i), getName(i), methods(i)

    if 0:
        print 'Methods', methods(1)
        print 'TurnOn', turnOn(1)
        time.sleep(1)
        print 'TurnOff', turnOff(1)
        time.sleep(1)
        print 'Dim', dim(1, 121)
    
    print 'LastSentCommand', lastSentCommand(1)
    print 'LastSentValue', lastSentValue(1)
    print 'GetErrorString', getErrorString(-2)
    print 'AddDevice', addDevice()
