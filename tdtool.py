# ******************************************
#
# Example usage of td.py that mimic tdtool
#
# Developed by David Karlsson
#             (david.karlsson.80@gmail.com)
#
# Released as is without any garantees on
# functionality.
#
# *******************************************
import optparse
import td
import time

def myDeviceEvent(deviceId, method, data, callbackId):
    print 'DeviceEvent'
    print 'deviceId: 0x%x' %( deviceId )
    print 'method: 0x%x' %( method )
    print 'data: %s' %(data )
    print 'callbackId: 0x%x' %( callbackId )
    



def myDeviceChangeEvent(deviceId, changeEvent, changeType, callbackId):
    print 'DeviceChangeEvent'
    print 'deviceId: %x' %( deviceId )
    print 'changeEvent: %x' %( changeEvent )
    print 'changeType: %x' %( changeType )
    print 'callbackId: %x' %(callbackId)


if __name__ == '__main__':
    usage = "Support one of the following arguments (except --dimlevel that is allways allowed but ignored in all other cases than combined with --dim)."

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
    parser.add_option("-t", "--event",
                      action="store_true", default=False,
                      help="Listen for events untill interrupted by ctrl-c")

    (options, args) = parser.parse_args()

    #td.init( methodsSupported = td.TELLSTICK_TURNON | td.TELLSTICK_TURNOFF ) #Application can configure to support different methods
#    td.init()

    if options.on != None and options.off == None and options.bell == None and options.list == False and options.dim == None and options.learn == None and options.event == False:

        #
        #   ON
        #
                    
        deviceId, deviceName = td.getDeviceIdFromStr(options.on)
        if deviceId == -1:
            parser.error('unknown device: ' + options.on) 

        resCode = td.turnOn(deviceId)
        if resCode != 0:
            res = td.getErrorString(resCode)
        else:
            res = 'Success'

        print 'Turning on device:', deviceId, deviceName, '-', res



    elif options.on == None and options.off != None and options.bell == None and options.list == False and options.dim == None and options.learn == None and options.event == False:

        #
        #   OFF
        #
                    
        deviceId, deviceName = td.getDeviceIdFromStr(options.off)
        if deviceId == -1:
            parser.error('unknown device: ' + options.off) 

        resCode = td.turnOff(deviceId)
        if resCode != 0:
            res = td.getErrorString(resCode)
        else:
            res = 'Success'

        print 'Turning off device:', deviceId, deviceName, '-', res


    elif options.on == None and options.off == None and options.bell != None and options.list == False and options.dim == None and options.learn == None and options.event == False:

        #
        #   BELL
        #
                    
        deviceId, deviceName = td.getDeviceIdFromStr(options.bell)
        if deviceId == -1:
            parser.error('unknown device: ' + options.bell) 

        resCode = td.bell(deviceId)
        if resCode != 0:
            res = td.getErrorString(resCode)
        else:
            res = 'Success'

        print 'Sending bell to:', deviceId, deviceName, '-', res


    elif options.on == None and options.off == None and options.bell == None and options.list == True and options.dim == None and options.learn == None and options.event == False:

        #
        #    LIST
        #

        print 'Number of devices:', td.getNumberOfDevices()
        for i in range(td.getNumberOfDevices()):
            cmd = td.lastSentCommand(i, readable = True)
            if cmd == 'DIM':
                cmd += ':' + str(td.lastSentValue(i))
            print td.getDeviceId(i), '\t', td.getName(i), '\t\t', cmd, '\t\t', td.methods(i, readable = True)
        print ''

    elif options.on == None and options.off == None and options.bell == None and options.list == False and options.dim != None and options.dimlevel != None and options.learn == None and options.event == False:
 
         #
        #    DIM
        #

        try:
            dimlevel = int(options.dimlevel)
        except:
            parser.error('--dimlevel LEVEL needs to be an integer and 0-255')

        if dimlevel < 0 or dimlevel > 255:
            parser.error('--dimlevel LEVEL needs to be an integer and 0-255')
                    
        deviceId, deviceName = td.getDeviceIdFromStr(options.dim)
        if deviceId == -1:
            parser.error('unknown device: ' + options.dim) 

        resCode = td.dim(deviceId, dimlevel)
        if resCode != 0:
            res = td.getErrorString(resCode)
        else:
            res = 'Success'

        print 'Dimming device:', deviceId, deviceName, 'to', dimlevel, '-', res


    elif options.on == None and options.off == None and options.bell == None and options.list == False and options.dim == None and options.learn != None and options.event == False:

        #
        #   LEARN
        #
                    
        deviceId, deviceName = td.getDeviceIdFromStr(options.learn)
        if deviceId == -1:
            parser.error('unknown device: ' + options.learn) 

        resCode = td.learn(deviceId)
        if resCode != 0:
            res = td.getErrorString(resCode)
        else:
            res = 'Success'

        print 'Learning device:', deviceId, deviceName, '-', res

    elif options.on == None and options.off == None and options.bell == None and options.list == False and options.dim == None and options.learn == None and options.event == True:

        #
        #  Event
        #
        
        res = td.registerDeviceEvent(myDeviceEvent)
        print 'Register device event returned:', res

        res = td.registerDeviceChangedEvent(myDeviceChangeEvent)
        print 'Register device changed event returned:', res

        print 'Event handlers registered now waiting for events. Exit with ctrl-c.'
            
        try:
            while(1):
                time.sleep(1)
        except KeyboardInterrupt:
            print 'KeyboardInterrupt received, exiting'

    else:
        parser.error("Can only handle one of --on, --off, --bell, --list, --dim, --learn, -event")

    td.close()



