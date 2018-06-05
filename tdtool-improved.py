#!/usr/bin/env python

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
from datetime import datetime

def myDeviceEvent(deviceId, method, data, callbackId):
    print '%d: DeviceEvent Device: %d - %s' %( time.time(), deviceId, td.getName(deviceId) )
    print '  method: %d - %s, data: %s' %( method, td.methodsReadable.get(method, 'Unknown' ), data )

def myDeviceChangeEvent(deviceId, changeEvent, changeType, callbackId):
    print '%d: DeviceChangeEvent Device: %d - %s' %(time.time(), deviceId, td.getName(deviceId))
    print '  changeEvent: %d' %( changeEvent )
    print '  changeType: %d' %( changeType )

def myRawDeviceEvent(data, controllerId, callbackId):
    print '%d: RawDeviceEvent: %s' %(time.time(), data)
    print '  controllerId:', controllerId

def mySensorEvent(protocol, model, id, dataType, value, timestamp, callbackId):
    print '%d: SensorEvent' %(time.time())
    print '  protocol: %s' %(protocol)
    print '  model: %s' %(model)
    print '  id: %d' %(id)
    print '  dataType: %d' %(dataType)
    print '  value: %s' %(value)
    print '  timestamp: %d' %(timestamp)

def getDeviceIdAndName(input):
    if (input.isdigit()):
        deviceId = int(input)
        deviceName = td.getName(int(input))
    else:
        deviceId, deviceName = td.getDeviceIdFromStr(input)

    return deviceId, deviceName


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

    td.init( defaultMethods = td.TELLSTICK_TURNON | td.TELLSTICK_TURNOFF ) #Application can configure to support different methods
#    td.init()

    if options.on != None and options.off == None and options.bell == None and options.list == False and options.dim == None and options.learn == None and options.event == False:

        #
        #   ON
        #
                    
        deviceId, deviceName = getDeviceIdAndName(options.on)
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
                    
        deviceId, deviceName = getDeviceIdAndName(options.off)
        
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
                    
        deviceId, deviceName = getDeviceIdAndName(options.bell)
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
            deviceId = td.getDeviceId(i)
            cmd = td.lastSentCommand(deviceId, methodsSupported = td.TELLSTICK_ALL, readable = True)
            value = td.lastSentValue(deviceId)
            if value:
                value = " (%s)" % value
            print deviceId, '\t', td.getName(deviceId), '\t\t', cmd, value, '\t\t', td.methods(deviceId, methodsSupported = td.TELLSTICK_ALL, readable = True)
        sensors = td.getSensors()
        print '\nNumber of sensors:', len(sensors)
        for s in sensors:
            print "Sensor: %-40s %-11s: %12s %s" % ("%s.%s.%s" % (s.protocol, s.model, s.id),
                                                    td.sensorValueTypeReadable[s.dataType] or "Unknown", s.value, 
                                                    datetime.fromtimestamp(s.timestamp).strftime('%Y-%m-%d %H:%M:%S'))
        print '\n'


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
                    
        deviceId, deviceName = getDeviceIdAndName(options.dim)
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
                    
        deviceId, deviceName = getDeviceIdAndName(options.learn)
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
        cbId = []

        cbId.append(td.registerDeviceEvent(myDeviceEvent))
        print 'Register device event returned:', cbId[-1]

        cbId.append(td.registerDeviceChangedEvent(myDeviceChangeEvent))
        print 'Register device changed event returned:', cbId[-1]

        cbId.append(td.registerRawDeviceEvent(myRawDeviceEvent))
        print 'Register raw device event returned:', cbId[-1]

        cbId.append(td.registerSensorEvent(mySensorEvent))
        print 'Register sensor event returned:', cbId[-1]

        print 'Event handlers registered now waiting for events. Exit with ctrl-c.'
            
        try:
            while(1):
                time.sleep(1)
        except KeyboardInterrupt:
            print 'KeyboardInterrupt received, exiting'
            for i in cbId:
                td.unregisterCallback(i)

    else:
        parser.error("Can only handle one of --on, --off, --bell, --list, --dim, --learn, --event")

    td.close()