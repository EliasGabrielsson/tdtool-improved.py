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


methodsSupported = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | TELLSTICK_TOGGLE | TELLSTICK_DIM | TELLSTICK_LEARN

def getNumberOfDevices():
    return tdlib.tdGetNumberOfDevices()

def getDeviceId(i):
    return tdlib.tdGetDeviceId(int(i))

def getName(id):
    getNameFunc = tdlib.tdGetName
    getNameFunc.restype = c_void_p

    vp = getNameFunc(id)
    cp = c_char_p(vp)
    s = cp.value
    
    tdlib.tdReleaseString(vp)

    return s

def methods(id, methodsSupported = methodsSupported):
    methods = tdlib.tdMethods(id, methodsSupported)
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

def lastSentCommand(intDeviceId, methodsSupported = methodsSupported):
    return tdlib.tdLastSentCommand(intDeviceId, methodsSupported)

def lastSentValue(intDeviceId):
    func = tdlib.tdLastSentValue
    func.restype = c_char_p

    ret = func(intDeviceId)

    print repr(ret)
    
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
#int tdAddDevice();    

#
#bool tdSetName(int intDeviceId, const char* chNewName);
#char * tdGetProtocol(int intDeviceId);
#bool tdSetProtocol(int intDeviceId, const char* strProtocol);
#char * tdGetModel(int intDeviceId);
#bool tdSetModel(int intDeviceId, const char *intModel);

#char * tdGetDeviceParameter(int intDeviceId, const char *strName, const char *defaultValue);
#bool tdSetDeviceParameter(int intDeviceId, const char *strName, const char* strValue);


#bool tdRemoveDevice(int intDeviceId);

#int tdSendRawCommand(const char *command, int reserved);

#void tdConnectTellStickController(int vid, int pid, const char *serial);
#void tdDisconnectTellStickController(int vid, int pid, const char *serial);
    

if __name__ == '__main__':
    import time
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
