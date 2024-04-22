import obd
from obd import OBDStatus
import time


obdConnectStatus = 'Starting'
responseDict = {}
rawDict = {
    'rpm': 1,
    'speed': 1,
    'coolantTemp': 1,
    'throttlePos': 1,
    'inNeutral':0
}

def readOBD(obdCon,baudR=''):# '/dev/ttys007', 9600
    attemptConnect = 0
    global responseDict,queryDict,obdConnectStatus,rawDict
    # Connect to OBD
    try:
        obdConnectStatus = 'Trying to connect'
        car = obd.OBD(eval(obdCon),int(baudR))
    except:
        #TODO find exact error type for this
        obdConnectStatus = 'OBD script error'
        exit()
        
    print(car.supported_commands)
    # PID queries
    basePIDs = {
        'rpm': 'RPM',
        'speed': 'SPEED',
        'fuelStatus': 'FUEL_STATUS',
        'throttlePos': 'THROTTLE_POS',
        'coolantTemp': 'COOLANT_TEMP',
        'voltage': 'CONTROL_MODULE_VOLTAGE',
        }
    
    customPIDs = {}
    """ 
    customPIDs = {
        'throttlePosCustom': 'MX_5_ACCL_PDL',
        'inNeutral': 'MX5_NEUTRAL_SW',
        'SteeringPos': 'MX5_WHL_ANG',
    }
     """
    # Add custom PIDs to supported commands
    
    #Create copy of dict
    queryDict = basePIDs | customPIDs
    responseDict = queryDict.copy()
    #Formatted dictionary for use possibly
    formattedDcit = queryDict.copy()
    # Exit if OBD completely failed to connect.
    if car.status() == OBDStatus.NOT_CONNECTED:
        obdConnectStatus = 'Failed to connect'
        exit()
    
    
    # Add custom PIDs to supported commands
    for command in customPIDs:
        car.supported_commands.add(command)
    
    while attemptConnect < 30:
        # Wait 30 seconds to allow car to start
        obdConnectStatus = car.status()
        
        if car.status() == OBDStatus.CAR_CONNECTED:
            while car.status() == OBDStatus.CAR_CONNECTED:
            # get data
                for key, command in queryDict.items():
                    
                    # Format commands
                    queryT = eval(f'obd.commands.{command}')
                    response = car.query(queryT)
                    
                    # Attempt to run queries
                    try:
                        response = response.value
                        try:
                            responseDict[key] = response.magnitude
                            rawDict[key] = int(response.magnitude)
                        except:
                            responseDict[key] = response
                            rawDict[key] = int(response)
                    except:
                        # No response to query
                        responseDict[key] = 'NO_DATA'
                        print(f'{key} has no data')
                        continue                    
                time.sleep(.01)

            # Reset connection attempt timeout if car was able to connect.  Allows car to reconnect if there is a momentary connection loss
            attemptConnect = 0
        time.sleep(1)
        attemptConnect +=1
    # Update status if car goes 30 seconds without making a full connection
    if attemptConnect > 28:
        obdConnectStatus = 'Timed out'
    else:
        exit()