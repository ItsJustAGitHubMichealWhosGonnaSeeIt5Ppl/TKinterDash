import obd
from obd import OBDStatus
import time


def readOBD():
    attemptConnect = 0
    global responseDict,queryDict,obdConnectStatus
    
    # Connect to OBD
    try:
        car = obd.OBD("192.168.0.10", 35000)
    except:
        #TODO find exact error type for this
        obdConnectStatus = 'OBD script error'
        exit()
        
    # PID queries
    basePIDs = {
        'rpm': 'RPM',
        'speed': 'SPEED',
        'fuelStatus': 'FUEL_STATUS',
        'throttlePos': 'THROTTLE_POS',
        'coolantTemp': 'COOLANT_TEMP',
        'voltage': 'CONTROL_MODULE_VOLTAGE',
        }
    
    
    customPIDs = {
        'throttlePosCustom': 'MX_5_ACCL_PDL',
        'inNeutral': 'MX5_NEUTRAL_SW',
        'SteeringPos': 'MX5_WHL_ANG',
    }
    
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
                        except:
                            responseDict[key] = response
                    
                    except:
                        # No response to query
                        responseDict[key] = 'NO_DATA'
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