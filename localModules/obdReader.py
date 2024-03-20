import obd
import time
from placeholder import * # Import custom PIDs




def readOBD():
    globals(speed,rpm,responseDict)
    
    # Connect to OBD
    car = obd.OBD("192.168.0.10", 35000)
    
    # Create queries
    queryDict = {
        'rpm': 'RPM',
        'speed': 'SPEED',
        'fuelLevel': 'FUEL_LEVEL',
        'fuelStatus': 'FUEL_STATUS',
        'throttlePos': 'THROTTLE_POS',
        }
    responseDict = queryDict.copy()
    while True:
        # get data
        for key, value in queryDict.items:
            response = car.query(f'obd.commands.{value}')
            responseDict[key] = response.value
        time.sleep(.01)
        