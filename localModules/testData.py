#TODO create fake RPM, speed, gear, etc here
import random
import time
import threading

def fakeCarOBD(engineOn, rpm, speed):
    # Base state of car
    requestedThrottlePos = 0
    gear = 0
    ingear = False
    coolantTemp = 0
    
    #No changing
    maxRPM = 7500
    idle = 1100
    rpmMulti = maxRPM / 100
    throttlePos = 0
    
    # Gear Ratios (we're going simple)
    gearRatios = {
        '0':3.5, # Reverse
        '1':3,
        '2':2,
        '3':1.5,
        '4':1.2,
        '5':1,
        '6':0.8,
    }
    
    
    while True:
        time.sleep(.1)
        if engineOn == False:
            speed = 0
            while rpm > 0: # RPM drop if car is turned off
                rpm  = rpm - random.randint(200, 1250)
                rpm = 0 if rpm < 0 else rpm
                time.sleep(.1)
            time.sleep(.5)
            
        # Ok I guess the engine is on
        elif engineOn == True:
            idleRPM = idle + random.randint(-50, 50) # Add excitement to life
            
            # Figure out the RPM
            if throttlePos < 3:
                rpm = idleRPM
            else:
                rpm = idleRPM + (throttlePos * rpmMulti) - idle # Gives that random RPM number
            # Figure out the speed
            if ingear == True:
                speed = (rpm /60) / gearRatios[str(gear)]
            else:
                speed = speed - 2 if speed > 2 else 0
                
                
                
                

    
    




#Testing RPM bar thread
def rpmThreadTest():
    time.sleep(5)
    mode = '+'
    global rpmAnim
    global rpmRaw
    while True:
        if mode == '+' and rpmRaw > 7700:
            mode = '-'
        elif mode == '-' and rpmRaw < 600:
            mode = '+'
            
        rpmRaw = rpmRaw + 1 if mode=='+' else rpmRaw - 1
        time.sleep(.001)
        rpm.set(rpmRaw)
        

#rpmThreadTestStarter = threading.Thread(target=rpmThreadTest)
#rpmThreadTestStarter.start()