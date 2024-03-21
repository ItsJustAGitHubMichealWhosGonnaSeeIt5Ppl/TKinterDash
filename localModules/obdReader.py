import obd
from obd import OBDStatus
import time
# from placeholder import * # Import custom PIDs

rpm = '911 revs this is fake tho'
speed = 10
 # Debugging, bypass complaints about OBD not connecting
forcePass=False
def readOBD():
    global responseDict,carConnected,queryDict
    carConnected = False
    # Connect to OBD
    car = obd.OBD("192.168.0.10", 35000)
    
    # Error catching
    
    while car.status() != OBDStatus.CAR_CONNECTED and attemptConnect < 60 and forcePass == False: # Wait 60 seconds before producing an error
        if car.status() == OBDStatus.OBD_CONNECTED: # Car is off but OBD is connected
            print('Turn the car on idiot')
        else:
            print(car.status())
        time.sleep(1)
        attemptConnect +=1
    if car.status() != OBDStatus.CAR_CONNECTED and forcePass == False:
        raise SystemError('OBD failed to connect to car fully. Last status was ', car.status())
    carConnected == True
        
    
    #Print all supported commands, will get this to add to the list later
    print (car.supported_commands)
    # Default queries (for now)
    # Using dictionary so cars with custom PIDs can swap out the value in the dict but dont need to update HUD.py
    queryDict = {
        'rpm': 'RPM',
        'speed': 'SPEED',
        'fuelStatus': 'FUEL_STATUS',
        'throttlePos': 'THROTTLE_POS',
        'coolantTemp': 'COOLANT_TEMP',
        'voltage': 'CONTROL_MODULE_VOLTAGE'
        ''
        }
    # Create responses dictionary
    responseDict = queryDict.copy()
    while True:
        # get data
        for key, command in queryDict.items():
            # Format commands
            queryT = eval(f'obd.commands.{command}')
            
            # Run query (It got mad when I combined this with the line below, idk why)
            response = car.query(queryT)
            response = response.value
            try:
                responseDict[key] = response.magnitude
            except:
                responseDict[key] = response
        time.sleep(.01)
        