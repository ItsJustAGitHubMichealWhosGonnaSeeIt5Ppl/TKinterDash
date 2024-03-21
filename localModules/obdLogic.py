import time

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
