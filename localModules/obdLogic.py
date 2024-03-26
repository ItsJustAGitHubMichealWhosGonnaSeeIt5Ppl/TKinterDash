import time

currentGear = '?'

def gearLogic(rpm,speed,nSwitch='None'):
    """ Figure out gear, does not currently know about reverse
    :param rpm: (int) vehicle RPM
    :param speed: Vehicle speed
    :param nSwitch: Neutral switch, if nothingis input, assume no switch exists"""
    
    global currentGear
    # Find a way to allow this value to be updated
    gears = [3.709, 2.19, 1.536, 1.177, 1, 0.832]
    finalDrive = 3.727
    # Final gear expects speed to be in MPH
    findGear = (speed*0.0166667)*856*finalDrive
    
    if nSwitch is 'None':
        nSwitch = False # Set vehicle to in gear
        
    if nSwitch == False:
        gear = 0
        for x in gears:
            gear+=1
            if findGear*x < rpm+50 and findGear*x >rpm-50:
                print('hit',gear)
                currentGear = gear
                break
            else:
                # Does not work
                currentGear = '?'
        currentGear = str(currentGear)
    elif nSwitch == True:
        currentGear = 'N'
    return currentGear
    
    

# Coolant Temp logic

# Fake data for testing
#Temp all in C
tempNow = 10
tempMax = 130
tempDesired = 90
rpmMax = 7700
rpmCap = 4000 # When we'll just say fuck it go
rpmMin = 2500 # RPM we can't go below
warmedUp = 0


# Written verbosely for now
def coolantTemp(tempNow):
    if tempNow < tempDesired - 5:
        warmedUp = 0

    while warmedUp != True:
        tempMultiplier = rpmCap / tempDesired
        if tempNow > 88: # Warmed up, give it the beans (but wait for oil, how do we count this)
            warmedUp +=1 # Every minute warmed up will be 6
            SuggestedMaxRPM = rpmCap + ((warmedUp/6) * 200)
            if warmedUp > 30: # Wait 5 more minutes idk why just feels right
                warmedUp = True
        elif tempNow * tempMultiplier < rpmMin:
            SuggestedMaxRPM = rpmMin
        else:
            maxCleaned = int((tempNow * tempMultiplier) / 100) # Rounds to the nearest hundred
            SuggestedMaxRPM = maxCleaned * 100
        time.sleep(10)
