import obd
from obd import OBDStatus
import time
# from placeholder import * # Import custom PIDs

rpm = '911 revs this is fake tho'
speed = 10

 # Debugging, bypass complaints about OBD not connecting
forcePass=False

def readOBD():
    attemptConnect = 0
    global responseDict,queryDict,carConnectionStatus
    
    carConnectionStatus = 1
    """ carConnectionStatuses
    1 - Initial attempt to connect
    2 - OBD has connected, car has not (car is probably not fully turned on)
    3 - Connected
    404 - Failed to connect
    5 - Connection failed but was bypassed
    """
    
    # Connect to OBD
    car = obd.OBD("192.168.0.10", 35000)
    print(car.status())
    # Error catching
    
    while car.status() != OBDStatus.CAR_CONNECTED and attemptConnect < 30: # Wait 60 seconds before producing an error
        if car.status() == OBDStatus.OBD_CONNECTED: # Car is off but OBD is connected
            print('Turn the car on idiot')
            carConnectionStatus = 2
        else:
            print(car.status())
        time.sleep(1)
        attemptConnect +=1
        print(attemptConnect)
    if car.status() != OBDStatus.CAR_CONNECTED and forcePass == False:
        carConnectionStatus = 404
        print('OBD failed to connect to car fully. Last status was ', car.status())
        
    else:
        carConnectionStatus = 3  if forcePass == False else 5
        
    
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
        