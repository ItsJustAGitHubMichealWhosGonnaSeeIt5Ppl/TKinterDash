import time

currentGear = '?'

def gearLogic(rpm,speed):
    """ Figure out gear from RPM, speed, final drive ratio, and gear ratios. does not currently know about reverse
    :param rpm: (int) vehicle RPM
    :param speed: Vehicle speed"""
    
    global currentGear
    # Find a way to allow this value to be updated
    gears = [3.709, 2.19, 1.536, 1.177, 1, 0.832]
    finalDrive = 3.727
    # Final gear expects speed to be in MPH
    findGear = (speed*0.0166667)*856*finalDrive
    gear = 0
    for x in gears:
        gear+=1
        if findGear*x < rpm+50 and findGear*x >rpm-50:
            # print('gear is ',gear)
            currentGear = gear
            break
        else:
            # Does not work
            currentGear = '?'
    currentGear = str(currentGear)
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


def SmartShift(gear,rpm,throttle):
    """Recommend gear
    CALIBRATED TO MY CAR, will try to figure out how to adapt this for other vechiles

    Args:
        gear (int),(str): Current gear
        rpm (int): current RPM
        throttle (int): Current throttle position (0 - 100)
    """

    uniC = {
        1:'①',
        2:'②',
        3:'③',
        4:'④',
        5:'⑤',
        6:'⑥',
    }
    
    
    
    ## random data to implement
    # If cruising in 6th at 3500 RPM, shifting to third for extra power is an option
    
    
    # Action can be Shift Up, Shift Down, or nothing
    recAction = ''
    # Recommended gear for user
    recGear = ''
    
    if gear.isdigit() is not True:
        # Skip if not in gear or gear cant be detected
        return recAction, recGear
    gear = int(gear)
    if rpm < 600:
        recAction = '▼'
        recGear = 'Ⓝ'
    elif gear > 2 and rpm < 2000 and throttle > 20:
        # Avoid recommending shifting if in a low gear already
        recAction = '▼'
        recGear = uniC[gear -1]
    elif gear < 6 and rpm > 3000 and throttle < 25:
        recAction = '▲'
        recGear = uniC[gear +1]
    
    return recAction, recGear
        
    