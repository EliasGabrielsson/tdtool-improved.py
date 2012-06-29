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

from ctypes import *
from ctypes import byref
tdlib = CDLL("libtelldus-core.so.2")

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
        return methodsReadable[tdlib.tdLastSentCommand(intDeviceId, methodsSupported)]

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

    tdlib.tdInit()

def close():
    tdlib.tdClose()

#Callback fro DeviceEvent
DEVICEEVENTFUNC = CFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_void_p)

#This is a prototype of Device Event function that should be passed to
# registerDeviceEvent function
def deviceEvent(deviceId, method, data, callbackId, context):
    print 'DeviceEvent'
    print 'deviceId:', deviceId
    print 'method:', method
    print 'data:', data
    print 'callbackId:', callbackId
    print 'context:', context

def registerDeviceEvent(func):
    deviceEvent_func = DEVICEEVENTFUNC(func)
    
    return tdlib.tdRegisterDeviceEvent(deviceEvent_func, c_void_p(0))

#Callback for DeviceChangeEvent
DEVICECHANGEEVENTFUNC = CFUNCTYPE(None, c_int, c_int, c_int, c_int, c_void_p)

#This is a prototype of Device Change Event function that should be passed to
# registerDeviceEvent function
def deviceChangeEvent(deviceId, changeEvent, changeType, callbackId, context):
    print 'DeviceChangeEvent'
    print 'deviceId:', deviceId
    print 'changeEvent:', changeEvent
    print 'changeType:', changeType
    print 'callbackId:', callbackId


def registerDeviceChangedEvent(func):
    deviceChangeEvent_func = DEVICECHANGEEVENTFUNC(func)

    return tdlib.tdRegisterDeviceChangeEvent(deviceChangeEvent_func, c_void_p(0))


#Callback for 



#Callback for SensorEvent
SENSOREVENTFUNC = CFUNCTYPE(None, c_char_p, c_char_p, c_int, c_int, c_char_p, c_int, c_int, c_void_p)


#This is a prototype of Device Change Event function that should be passed to
# registerDeviceEvent function
def sensorEvent(protocol, model, id, dataType, value, timestamp, callbackId, context):
    print 'SensorEvent'
    print 'protocol:', protocol
    print 'model:', model
    print 'id:', id
    print 'datatype:', dataType
    print 'value:', value
    print 'teimstamp:', timestamp
    print 'callbackId:', callbackId
    print 'context:', context


def registerSensorEvent(func):
    sensorEvent_func = SENSOREVENTFUNC(func)
    return tdlib.tdRegisterSensorEvent(sensorEvent_func, c_void_p(0))
    

def unregisterCallback(callbackId):
    return tdlib.tdUnregisterCallback(callbackId)


#Missing support for these API calls:
#
#int tdRegisterRawDeviceEvent( TDRawDeviceEvent eventFunction, void *context );
#int tdRegisterControllerEvent( TDControllerEvent eventFunction, void *context);


#bool tdSetProtocol(int intDeviceId, const char* strProtocol);
#bool tdSetModel(int intDeviceId, const char *intModel);
#bool tdSetDeviceParameter(int intDeviceId, const char *strName, const char* strValue);

#int tdSendRawCommand(const char *command, int reserved);

#void tdConnectTellStickController(int vid, int pid, const char *serial);
#void tdDisconnectTellStickController(int vid, int pid, const char *serial);
    

if __name__ == '__main__':
    import time

    init()

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
        
        print 'getDeviceIdFromStr', getDeviceIdFromStr('2')
        
        print 'getDeviceIdFromStr', getDeviceIdFromStr('Vardagsrum')

        print 'getDeviceIdFromStr', getDeviceIdFromStr('234')

    print repr(setName(getDeviceId(1), 'Test'))
    print getProtocol(getDeviceId(1))
    print getModel(getDeviceId(1))
    print repr(getDeviceParameter(getDeviceId(1), "unit", ""))
    print repr(getDeviceParameter(getDeviceId(1), "house", ""))
    

    cb = registerDeviceEvent(deviceEvent)
    print cb
    print unregisterCallback(3)

    time.sleep(20)

    print 'Done with unit test'
