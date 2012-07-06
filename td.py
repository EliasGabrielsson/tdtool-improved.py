# ******************************************
#
# Python wrapper for libtelldus on Linux
#
# Developed by David Karlsson
#             (david.karlsson.80@gmail.com)
#
# Released as is without any garantees on
# functionality.
#
# *******************************************
import platform
import time
from ctypes import c_int, c_ubyte, c_void_p, c_char_p, POINTER, string_at

#platform specific imports:
if (platform.system() == 'Windows'):
    #Windows
    from ctypes import windll, WINFUNCTYPE
    tdlib = windll.LoadLibrary('TelldusCore.dll') #import our library
else:
    #Linux
    from ctypes import cdll, CFUNCTYPE
    tdlib = cdll.LoadLibrary('libtelldus-core.so.2') #import our library

#Device methods
TELLSTICK_TURNON =         1
TELLSTICK_TURNOFF =        2
TELLSTICK_BELL =           4
TELLSTICK_TOGGLE =         8
TELLSTICK_DIM =           16
TELLSTICK_LEARN =         32
TELLSTICK_EXECUTE =       64
TELLSTICK_UP =           128
TELLSTICK_DOWN =         256
TELLSTICK_STOP =         512

methodsReadable = {1: 'ON',
                   2: 'OFF',
                   4: 'BELL',
                   8: 'TOGGLE',
                   16: 'DIM',
                   32: 'LEARN',
                   64: 'EXECUTE',
                   128: 'UP',
                   256: 'DOWN',
                   512: 'STOP'}



#Sensor value types
TELLSTICK_TEMPERATURE =    1
TELLSTICK_HUMIDITY =       2

#Error codes
TELLSTICK_SUCCESS =                       0
TELLSTICK_ERROR_NOT_FOUND =              -1
TELLSTICK_ERROR_PERMISSION_DENIED =      -2
TELLSTICK_ERROR_DEVICE_NOT_FOUND =       -3
TELLSTICK_ERROR_METHOD_NOT_SUPPORTED =   -4
TELLSTICK_ERROR_COMMUNICATION =          -5
TELLSTICK_ERROR_CONNECTING_SERVICE =     -6
TELLSTICK_ERROR_UNKNOWN_RESPONSE =       -7
TELLSTICK_ERROR_SYNTAX =                 -8
TELLSTICK_ERROR_BROKEN_PIPE =            -9
TELLSTICK_ERROR_COMMUNICATING_SERVICE = -10
TELLSTICK_ERROR_CONFIG_SYNTAX =         -11
TELLSTICK_ERROR_UNKNOWN =               -99

#Controller typedef
TELLSTICK_CONTROLLER_TELLSTICK =          1
TELLSTICK_CONTROLLER_TELLSTICK_DUO =      2
TELLSTICK_CONTROLLER_TELLSTICK_NET =      3

#Device changes
TELLSTICK_DEVICE_ADDED =                  1
TELLSTICK_DEVICE_CHANGED =                2
TELLSTICK_DEVICE_REMOVED =                3
TELLSTICK_DEVICE_STATE_CHANGED =          4

#Change types
TELLSTICK_CHANGE_NAME =                   1
TELLSTICK_CHANGE_PROTOCOL =               2
TELLSTICK_CHANGE_MODEL =                  3
TELLSTICK_CHANGE_METHOD =                 4
TELLSTICK_CHANGE_AVAILABLE =              5
TELLSTICK_CHANGE_FIRMWARE =               6


methodsSupportedDefault = 0

def getNumberOfDevices():
    return tdlib.tdGetNumberOfDevices()

def getDeviceId(i):
    return tdlib.tdGetDeviceId(int(i))

def getDeviceIdFromStr(s):
    try:
        id = int(s)
        return getDeviceId(id), getName(id)
    except:
        pass

    for i in range(getNumberOfDevices()):
        if s == getName(i):
            return getDeviceId(i), s

    return -1, 'UNKNOWN'


def getName(id):
    getNameFunc = tdlib.tdGetName
    getNameFunc.restype = c_void_p

    vp = getNameFunc(id)
    cp = c_char_p(vp)
    s = cp.value
    
    tdlib.tdReleaseString(vp)

    return s

def methods(id, methodsSupported = None, readable = False):
    if methodsSupported == None:
        methodsSupported = methodsSupportedDefault

    methods = tdlib.tdMethods(id, methodsSupported)
    if readable:
        l = []
        for m in methodsReadable:
            if methods & m:
                l.append(methodsReadable[m])
        return ','.join(l)

    return methods

def turnOn(intDeviceId):
    return tdlib.tdTurnOn(intDeviceId)

def turnOff(intDeviceId):
    return tdlib.tdTurnOff(intDeviceId)

def turnOn(intDeviceId):
    return tdlib.tdTurnOn(intDeviceId)

def bell(intDeviceId):
    return tdlib.tdBell(intDeviceId)

def dim(intDeviceId, level):
    return tdlib.tdDim(intDeviceId, level)

def up(intDeviceId):
    return tdlib.tdUp(intDeviceId)

def down(intDeviceId):
    return tdlib.tdDown(intDeviceId)

def stop(intDeviceId):
    return tdlib.tdStop(intDeviceId)

def learn(intDeviceId):
    return tdlib.tdLearn(intDeviceId)

def lastSentCommand(intDeviceId, methodsSupported = None, readable = False):
    if methodsSupported == None:
        methodsSupported = methodsSupportedDefault

    if readable:
        return methodsReadable.get(tdlib.tdLastSentCommand(intDeviceId, methodsSupported), 'UNKNOWN')

    return tdlib.tdLastSentCommand(intDeviceId, methodsSupported)

def lastSentValue(intDeviceId):
    func = tdlib.tdLastSentValue
    func.restype = c_char_p

    ret = func(intDeviceId)
    
#Release string here?
    return ret

def getErrorString(intErrorNo):
    getErrorStringFunc = tdlib.tdGetErrorString
    getErrorStringFunc.restype = c_void_p

    vp = getErrorStringFunc(intErrorNo)
    cp = c_char_p(vp)
    s = cp.value
    
    tdlib.tdReleaseString(vp)

    return s

def addDevice():
    return tdlib.tdAddDevice()

def removeDevice(intDeviceId):
    return tdlib.tdRemoveDevice(intDeviceId)

def setName(intDeviceId, chNewName):
    if not isinstance(chNewName, str):
        raise ValueError('chNewName needs to be a str')
    if not isinstance(intDeviceId, int):
        raise ValueError('intDeviceId needs to be an integer')

    return tdlib.tdSetName(intDeviceId, chNewName)
    
def getProtocol(intDeviceId):
    if not isinstance(intDeviceId, int):
        raise ValueError('intDeviceId needs to be an integer')
    
    tdGetProtocolFunc = tdlib.tdGetProtocol
    tdGetProtocolFunc.restype = c_void_p

    vp = tdGetProtocolFunc(intDeviceId)
    cp = c_char_p(vp)
    s = cp.value
    
    tdlib.tdReleaseString(vp)

    return s

def getModel(intDeviceId):
    if not isinstance(intDeviceId, int):
        raise ValueError('intDeviceId needs to be an integer')
    
    tdGetModelFunc = tdlib.tdGetModel
    tdGetModelFunc.restype = c_void_p

    vp = tdGetModelFunc(intDeviceId)
    cp = c_char_p(vp)
    s = cp.value
    
    tdlib.tdReleaseString(vp)

    return s

def getDeviceParameter(intDeviceId, strName, defaultValue):
    if not isinstance(intDeviceId, int):
        raise ValueError('intDeviceId needs to be an integer')
    if not isinstance(strName, str):
        raise ValueError('strName needs to be a str')
    if not isinstance(defaultValue, str):
        raise ValueError('defaultValue needs to be a str')


    tdGetDeviceParameterFunc = tdlib.tdGetDeviceParameter
    tdGetDeviceParameterFunc.restype = c_void_p

    vp = tdGetDeviceParameterFunc(intDeviceId, strName, defaultValue)
    cp = c_char_p(vp)
    s = cp.value
    
    tdlib.tdReleaseString(vp)

    return s

def init(defaultMethods = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | TELLSTICK_TOGGLE | TELLSTICK_DIM | TELLSTICK_LEARN):

    global methodsSupportedDefault

    methodsSupportedDefault = defaultMethods

    #tdlib.tdInit()

def close():
    tdlib.tdClose()

#Callback fro DeviceEvent
#DEVICEEVENTFUNC = CFUNCTYPE(None, c_int, c_int, POINTER(c_ubyte), c_int, c_void_p)


if (platform.system() == 'Windows'):
    DEVICEFUNC = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_void_p)
    DEVICECHANGEFUNC = WINFUNCTYPE(None, c_int, c_int, c_int, c_int, c_void_p)
    SENSORFUNC = WINFUNCTYPE(None, c_char_p, c_char_p, c_int, c_int, c_char_p, c_int, c_int, c_void_p)
else:
    DEVICEFUNC = CFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_void_p)
    DEVICECHANGEFUNC = CFUNCTYPE(None, c_int, c_int, c_int, c_int, c_void_p)
    SENSORFUNC = CFUNCTYPE(None, c_char_p, c_char_p, c_int, c_int, c_char_p, c_int, c_int, c_void_p)




callbacks = {'lastAdd': 0,
             'deviceEvent': {},
             'deviceChangeEvent': {},
             'sensorEvent': {}
             }

def deviceEvent(deviceId, method, data, callbackId, context):
    print 'DeviceEvent'

    if 0:
        print 'deviceId:', deviceId
        print 'method:', method
        print 'data:', data
        print 'callbackId:', callbackId
        print 'context:', context

    for key in callbacks['deviceEvent']:
        f = callbacks['deviceEvent'][key]
        try:
            print f
            f(deviceId, method, data, callbackId)
        except:
            print 'Error calling registered callback'
            raise

def deviceChangeEvent(deviceId, changeEvent, changeType, callbackId, context):
    print 'DeviceChangeEvent'
    
    if 0:
        print 'deviceId:', deviceId
        print 'changeEvent:', changeEvent
        print 'changeType:', changeType
        print 'callbackId:', callbackId

    for key in callbacks['deviceChangeEvent']:
        f = callbacks['deviceChangeEvent'][key]
        try:
            print f
            f(deviceId, method, data, callbackId)
        except:
            print 'Error calling registered callback'
            raise


def sensorEvent(protocol, model, id, dataType, value, timestamp, callbackId, context):
    print 'SensorEvent'

    if 0:
        print 'protocol:', protocol
        print 'model:', model
        print 'id:', id
        print 'datatype:', dataType
        print 'value:', value
        print 'timestamp:', timestamp
        print 'callbackId:', callbackId
        print 'context:', context

    for key in callbacks['sensorEvent']:
        f = callbacks['sensorEvent'][key]
        try:
            f(deviceId, method, data, callbackId)
        except:
            print 'Error calling registered callback'


device_func = DEVICEFUNC(deviceEvent)
tdlib.tdRegisterDeviceEvent(device_func, 0)

deviceChange_func = DEVICECHANGEFUNC(deviceChangeEvent)
tdlib.tdRegisterDeviceChangeEvent(deviceChange_func, 0)

sensor_func = SENSORFUNC(sensorEvent)
tdlib.tdRegisterSensorEvent(sensor_func, 0)

tdlib.tdInit()

def registerEvent(func, eventType):

    global callbacks
    callbacks[eventType][callbacks['lastAdd']] = func

    id = callbacks['lastAdd']
    callbacks['lastAdd'] += 1

    print callbacks

    return id

def registerDeviceEvent(func):
    return registerEvent(func, 'deviceEvent')

def registerDeviceChangedEvent(func):
    return registerEvent(func, 'deviceChangeEvent')
    deviceChangeEvent_func = DEVICECHANGEEVENTFUNC(func)

    return tdlib.tdRegisterDeviceChangeEvent(deviceChangeEvent_func, c_void_p(0))

def registerSensorEvent(func):
    return registerEvent(func, 'sensorEvent')
    

def unregisterCallback(callbackId):
    global callbacks
    
    if callbackId in callbacks['deviceEvent']:
        del callbacks['deviceEvent'][callbackId]
    elif callbackId in callbacks['deviceChangeEvent']:
        del callbacks['deviceChangeEvent'][callbackId]
    elif callbackId in callbacks['sensorEvent']:
        del callbacks['sensorEvent'][callbackId]


def setProtocol(intDeviceId, strProtocol):
    return tdlib.tdSetProtocol(intDeviceId, strProtocol)

def setModel(intDeviceId, strModel):
    return tdlib.tdSetModel(intDeviceId, strModel)

def setDeviceParameter(intDeviceId, strName, strValue):
    return tdlib.tdSetDeviceParameter(intDeviceId, strName, strValue)

#Completly untested calls
def connectTellStickController(vid, pid, serial):
    tdlib.tdConnectTellStickController(vid, pid, serial)

def disconnectTellStickController(vid, pid, serial):
    tdlib.tdDisConnectTellStickController(vid, pid, serial)


#Missing support for these API calls:
#
#int tdRegisterRawDeviceEvent( TDRawDeviceEvent eventFunction, void *context );
#int tdRegisterControllerEvent( TDControllerEvent eventFunction, void *context);
#int tdSendRawCommand(const char *command, int reserved);    


if __name__ == '__main__':
    import time

    init()

    print 'getNumberOfDevices', getNumberOfDevices()
    
    print 'Id\tName'
    for i in range(getNumberOfDevices()):
        print getDeviceId(i), getName(i), methods(i)


    print 'Methods(1)', methods(1)
    print 'methods(1, readable=True)', methods(1, readable = True)
    print 'methods(3124, readable=True)', methods(3124, readable = True)
    print 'TurnOn(1)', turnOn(1)
    time.sleep(1)
    print 'TurnOff(1)', turnOff(1)
    time.sleep(1)
    print 'Dim (1, 121)', dim(1, 121)
    
    print 'LastSentCommand(1)', lastSentCommand(1)
    print 'LastSentValue(1)', lastSentValue(1)
    print 'GetErrorString(-2)', getErrorString(-2)
        
    print 'getDeviceIdFromStr', getDeviceIdFromStr('2')    
    print 'getDeviceIdFromStr', getDeviceIdFromStr('Vardagsrum')
    print 'getDeviceIdFromStr', getDeviceIdFromStr('234')


    devId = addDevice()
    if devId > 0:
        print 'AddDevice', devId
        print 'setName', repr(setName(devId, 'Test'))
        print 'getName', repr(getName(devId))
        print 'getProtocol', getProtocol(devId)
        print 'setProtocol', setProtocol(devId, 'arctech')
        print 'getProtocol', getProtocol(devId)

        print 'getModel', getModel(devId)
        print 'setModel', setModel(devId, 'selflearning-switch')
        print 'getModel', getModel(devId)

        print 'getDeviceParameter (unit)', repr(getDeviceParameter(devId, "unit", ""))
        print 'setDeviceParameter (unit)', repr(setDeviceParameter(devId, 'unit', '123'))                                       
        print 'getDeviceParameter (unit)', repr(getDeviceParameter(devId, "unit", ""))

        print 'getDeviceParameter (house)', repr(getDeviceParameter(devId, "house", ""))
        print 'setDeviceParameter (house)', repr(setDeviceParameter(devId, "house", "321"))
        print 'getDeviceParameter (house)', repr(getDeviceParameter(devId, "house", ""))
    
        print 'Remove Device', removeDevice(devId)

    else:
        print 'addDevice returned error', getErrorString(devId)

    print 'Done with unit test'
