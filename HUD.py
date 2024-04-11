# Make Tkinter do its thing
from tkinter import *
from tkinter import ttk

# Local stuff
from localModules.configCreator import configCheck
import localModules.obdReader as obdR
from localModules.obdLogic import gearLogic
# The rest
import configparser
from threading import Thread
import time
import os



### This is meant to be used with Python-OBD or other OBD/canbus data on an RPI Display.  Will add flexible sizing if I can figure out how that works later

# Read config file
config = configparser.ConfigParser()
if configCheck() == True:
    configPath = 'dash_config.ini'
    config.read(configPath)
    print(config.sections())
else:
    print('Tried to read/create config file and failed')
    exit()

# Start OBD thread
obdThread = Thread(target=obdR.readOBD)
obdThread.start()

# Start creation of the HUD
hudRoot = Tk()
hudRoot.title('MainHUD')
hudRoot.attributes("-fullscreen", True)

# Size of RPi display
hudRoot.geometry('800x480')
hudRoot.configure(bg='black')

# Centers the dash
hudMain = Frame(hudRoot)
hudBufferL = Frame(hudRoot)
hudBufferR = Frame(hudRoot,width=10)
hudBufferL.grid(column=0,row=0,rowspan=2)
hudBufferR.grid(column=2,row=0, rowspan=2)
hudMain.grid(column=1,row=1, sticky=(E, W, S))

## Create the RPM frame (might not be needed)
RPMBar = Frame(hudRoot,height=40,width=720,background='black',borderwidth=0,highlightthickness=0)
RPMBar.grid(column = 1, row = 0,sticky=(E, W, N))

# Create box for everything, also maybe helps with macOS.  sticky will anchor us to the walls (I think)
# allows for resizing? < No it keeps it all centered
hudRoot.columnconfigure(0, weight=1)
hudRoot.columnconfigure(2, weight=1) 
hudRoot.rowconfigure(1, weight=1)

#Stop itemsfrom resizing?
RPMBar.pack_propagate(0)
hudRoot.pack_propagate(0)
hudBufferR.grid_propagate(0)

# Fix styling issues for mac? 
style = ttk.Style(hudMain)
style.theme_use('classic')
style.configure("Red.TLabel", foreground="red")
style.configure("Green.TLabel", foreground="green")


# Variables to be updated from OBD
rpm = StringVar()
gear = StringVar()
speed = StringVar()
steeringPos = StringVar()
throttlePos = StringVar()
speedUnit = StringVar()
coolantTemp = StringVar()
connectStatus = StringVar()
connectStatus.set('Trying to connect')

# Currently selected speed units
speedUnit.set('???')
rpmRaw = 999
speedRaw = 132
inNeutralRaw = 1
throttlePosRaw = 6
coolantTempRaw = 35

# Keep updating variables
# Most values from obd are returned in Pint format which I've never used, sorry in advance for whatever i do
def refreshOBD():
    global rpmRaw,speedRaw
    connectStatus.set(obdR.obdConnectStatus)
    while obdR.obdConnectStatus != 'Failed to connect':
        connectStatus.set(obdR.obdConnectStatus)
        # TODO Find a better way to do this, maybe the same way its done in the other function, dictionary loop
        
        for dataName, dataValue in obdR.responseDict.items():
                
            try:
                eval(f'{dataName}Raw = {int(dataValue)}')
            except(ValueError):
                # No usable data
                pass
                # print(f'{dataName} has no data')
            
            # Special changes as needed
            if dataName == 'speed':
                if eval(config['General']['speed'])[0] == 'MPH':
                    speed.set(int(speedRaw*0.621371))
                    speedUnit.set('MPH')
                else:
                    speed.set(int(speedRaw))
                    speedUnit.set('KPH')
            # Set new values
            try:
                eval(f'{dataName}.set({dataName}Raw)')
            except(NameError):
                print(f'{dataName} could not be set or is not used')
    
        # Gear
        if inNeutralRaw == 1:
            gear.set('N')
        else:
            gear.set(gearLogic(rpmRaw,speedRaw*0.621371))
        time.sleep(.01)

refreshData = Thread(target=refreshOBD)
refreshData.start()

# 3x2 frames (tl = Top left, etc)
tlFrame = Frame(hudMain,width=240,height=220, background='red')
tcFrame = Frame(hudMain, width=240,height=220)
trFrame = Frame(hudMain, width=240,height=220,background='blue')
blFrame = Frame(hudMain, width=240,height=220,background='yellow')
bcFrame = Frame(hudMain, width=240,height=220,background='green')
brFrame = Frame(hudMain, width=240,height=220,background='purple')

# For some reason this makes the frames work better idk
tlFrame.grid(column=0,row=0, sticky=(N))
tcFrame.grid(column=1,row=0, sticky=(N))
trFrame.grid(column=2,row=0, sticky=(N, E))
blFrame.grid(column=0,row=1, sticky=(S, W))
bcFrame.grid(column=1,row=1, sticky=(S))
brFrame.grid(column=2,row=1, sticky=(S, E))


# Prevent resizing or does it idk
bcFrame.grid_propagate(0)


# Connection status display
connectStatusDisp = ttk.Label(blFrame,textvariable=connectStatus,justify='center', font=("Roboto",20))
connectStatusDisp.configure(style="Red.TLabel")
connectStatusDisp.grid(column=1,row=1, sticky=(S, W))

### Text/variable displays
## Speed
speedUnitDisp = ttk.Label(tcFrame,textvariable=speedUnit,justify='center', font=("Roboto",20))
speedDisplay = ttk.Label(tcFrame,textvariable=speed,justify='center', font=("Roboto",100))

#Show it
speedUnitDisp.grid(column=0,row=0)
speedDisplay.grid(column=0,row=1)


## Gears
gearText = ttk.Label(bcFrame,text='Gear', font=("Roboto",20))
gearSelect = ttk.Label(bcFrame,textvariable=gear, font=("Roboto",90))

# Actually display it
gearSelect.grid(column=1,row=1)
gearText.grid(column=1,row=0)

# Keep the text in the middle (it likes to run around otherwise)
bcFrame.columnconfigure(0, weight=1)
bcFrame.columnconfigure(2, weight=1) 

## Misc for testing
#throttleDisplay = ttk.Label(trFrame,textvariable=throttlePos,justify='center', font=("Roboto",20))
tempDisplay = ttk.Label(hudBufferR,textvariable=coolantTemp,justify='center', font=("Roboto",20))
#throttleDisplay.grid(column=0,row=0)
tempDisplay.grid(column=0,row=1)



## Throttle Pos bar
throttleBackGr = Canvas(trFrame,height=100, width=20,highlightthickness=1,background='grey')
throttleBarRect = throttleBackGr.create_rectangle(0,90,20,100,fill='blue',outline='blue')
throttleBackGr.pack()

## RPMs
rpmAnim = Canvas(RPMBar,width=720,highlightthickness=0,background='orange')
rpmBarRect = rpmAnim.create_rectangle(0,0,10,40,fill='blue',outline='blue')
rpmNumChange = rpmAnim.create_text(360,20,text='1234',anchor='center',font=("Roboto",30))
rpmAnim.pack()

def textThread():
    # Display RPM bar
    while True:
        rpmAnim.itemconfigure(rpmNumChange,text=str(rpmRaw))
        time.sleep(.01)


    
# RPM Bar thread
def rpmBarThr():
    global rpmAnim
    global rpmRaw
    
    # Multiplier to convert rpmRaw to the bar dimensions(locked for now)
    rpmMultiplier = 720 / int(eval(config['General']['redline'])[0])
    while True:
        # Adjust bars
        rpmAnim.coords(rpmBarRect,0,0,rpmRaw*rpmMultiplier,40)
        throttleBackGr.coords(throttleBarRect,0,100-throttlePosRaw,20,100)

        # Check for high revs
        if rpmRaw < int(eval(config['RPMWarnings']['rpmWarn'])[0]) and rpmRaw > 600:
            rpmAnim.itemconfigure(rpmBarRect,fill='blue',outline='blue')
            
        elif rpmRaw > int(eval(config['RPMWarnings']['rpmAlarm'])[0]):
            rpmAnim.itemconfigure(rpmBarRect,fill='red',outline='orange')
            time.sleep(.125)
            rpmAnim.itemconfigure(rpmBarRect,fill='orange',outline='red')  
            
        elif rpmRaw > int(eval(config['RPMWarnings']['rpmAlert'])[0]):
            rpmAnim.itemconfigure(rpmBarRect,fill='red',outline='red')
            
        elif rpmRaw > int(eval(config['RPMWarnings']['rpmWarn'])[0]):
            rpmAnim.itemconfigure(rpmBarRect,fill='orange',outline='orange')
        # Check for low revs (car stalled)
        elif rpmRaw < 600:
            rpmAnim.itemconfigure(rpmBarRect,fill='white',outline='white')
            time.sleep(.125)
            rpmAnim.itemconfigure(rpmBarRect,fill='black',outline='black')  
        else:
            rpmAnim.itemconfigure(rpmBarRect,fill='blue',outline='blue')
            
        time.sleep(.125 if rpmRaw > int(eval(config['RPMWarnings']['rpmAlarm'])[0]) or rpmRaw < 1000 else .01) # Add slightly more delay when the bar is flashing
        

#if config['Preferences']['dynamicRedline'] == True:
 #   pass

# Start threads
rpmBarThread = Thread(target=rpmBarThr)
TextThr = Thread(target=textThread)
rpmBarThread.start()
TextThr.start()
hudRoot.mainloop()
