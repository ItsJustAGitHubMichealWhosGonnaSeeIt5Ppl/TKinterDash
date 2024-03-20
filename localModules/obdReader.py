import obd
from obd import OBDStatus
import time
# from placeholder import * # Import custom PIDs

rpm = '911 revs this is fake tho'
speed = 10
forcePass = False # Debugging, bypass complaints about OBD not connecting

def readOBD():
    global responseDict
    
    # Connect to OBD
    car = obd.OBD("192.168.0.10", 35000)
    
    # Error catching
    while car.status() != OBDStatus.CAR_CONNECTED and attemptConnect < 60: # Wait 60 seconds before producing an error
        if car.status() == OBDStatus.OBD_CONNECTED:
            print('Car is off')
        else:
            print(car.status())
        time.sleep(1)
        attemptConnect +=1
    if car.status() != OBDStatus.CAR_CONNECTED and forcePass == False:
        raise SystemError('OBD failed to connect to car fully. Last status was ', car.status())
    
    #Print all supported commands, will get this to add to the list later
    print (car.supported_commands)
    # Default queries (for now)
    queryDict = {
        'rpm': 'RPM',
        'speed': 'SPEED',
        'fuelStatus': 'FUEL_STATUS',
        'throttlePos': 'THROTTLE_POS',
        }
    responseDict = queryDict.copy()

    while True:
        # get data
        for key, command in queryDict.items():
            # Format commands
            queryT = eval(f'obd.commands.{command}')
            
            # Run query (It got mad when I combined this with the line below, idk why)
            response = car.query(queryT)
            responseDict[key] = response.value
        time.sleep(.01)
        