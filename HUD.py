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


#debug toggle
debug = False

### This is meant to be used with Python-OBD or other OBD/canbus data on an RPI Display.  Will add flexible sizing if I can figure out how that works later

# Read config file
config = configparser.ConfigParser()
if configCheck() == True:
    config.read('dash_config.ini')
else:
    print('Tried to read/create config file and failed')

# Start OBD thread
obdThread = Thread(target=obdR.readOBD)
obdThread.start()

# Start creation of the HUD
hudRoot = Tk()
hudRoot.title('MainHUD')

# Size of RPi display
hudRoot.geometry('800x480')

# Centers the dash
hudMain = Frame(hudRoot)
hudBufferL = Frame(hudRoot)
hudBufferR = Frame(hudRoot)
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
speedUnit.set(config['Required']['speedUnits'])

# Trash data for debug
rpmRaw = 1001
speedRaw = 10
throttlePosRaw = 0
speed.set(speedRaw)
gear.set('?')

# Keep updating variables
# Values from obd are returned in Pint format which I've never used, sorry in advance for whatever i do
def refreshOBD():
    global rpmRaw,rpm
    time.sleep(5)
    while obdR.carConnectionStatus not in [3,404,5]:
        # Wait for OBD to connect
        time.sleep(2)
    if obdR.carConnectionStatus is 404:
        connectStatus.set('Failed to Connect')
    if obdR.carConnectionStatus is 5:
        connectStatus.set('DEBUG ENABLED')
    while obdR.carConnectionStatus in [3,5]:
        if obdR.carConnectionStatus is 3:
            connectStatusDisp.destroy()
        
        # RPM data
        rpmRaw = int(obdR.responseDict['rpm'])
        rpm.set(rpmRaw)
        
        # TODO make a seperate module that checks for config every second or something.
        # convert speed if needed, I know it can be cleaner.
        speedRaw = int(obdR.responseDict['speed'])
        if config['Required']['speedUnits'] == 'MPH':
            speed.set(int(speedRaw*0.621371))
        else:
            speed.set(int(speedRaw))
            speedUnit.set('KPH')
            
            
        
        # Gear
        gear.set(gearLogic(rpmRaw,speedRaw*0.621371))
        #Throttle data
        
        throttlePosRaw = obdR.responseDict['throttlePos']
        throttlePos.set(throttlePosRaw)
        
        #Coolant
        # TODO allow temp unit changing
        coolantRaw = obdR.responseDict["coolantTemp"]
        coolantTemp.set(coolantRaw)
       
        time.sleep(.01)

refreshData = Thread(target=refreshOBD)
if debug == False: refreshData.start()

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


# Error display
connectStatusDisp = ttk.Label(blFrame,textvariable=connectStatus,justify='center', font=("Roboto",20))
connectStatusDisp.configure(style="Red.TLabel")
connectStatusDisp.grid(column=0,row=0, sticky=(S, W))

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

## RPMs
rpmAnim = Canvas(RPMBar,width=720,highlightthickness=0)
rpmBarRect = rpmAnim.create_rectangle(0,0,10,40,fill='blue',outline='blue')
rpmNumChange = rpmAnim.create_text(360,20,text='1234',anchor='center',font=("Roboto",30))
rpmAnim.pack()

def textThread():
    # Display RPM bar
    # TODO Possibly move the RPM number and bar movement to their own thread to it can be smoother.
    # Display RPM number onscreen
    while True:
        rpmAnim.itemconfigure(rpmNumChange,text=str(rpmRaw))
        time.sleep(.01)
    
# RPM Bar thread
def rpmBarThr():
    global rpmAnim
    global rpmRaw
    
    # Multiplier to convert rpmRaw to the bar dimensions(locked for now)
    rpmMultiplier = 720 / int(config['Required']['redline'])
    while True:
        # Adjust bar
        rpmAnim.coords(rpmBarRect,0,0,rpmRaw*rpmMultiplier,40)

        # Check for high revs
        if rpmRaw > int(config['RPM']['rpmAlarm']):
            rpmAnim.itemconfigure(rpmBarRect,fill='red',outline='orange')
            time.sleep(.125)
            rpmAnim.itemconfigure(rpmBarRect,fill='orange',outline='red')  
            
        elif rpmRaw > int(config['RPM']['rpmAlert']):
            rpmAnim.itemconfigure(rpmBarRect,fill='red',outline='red')
            
        elif rpmRaw > int(config['RPM']['rpmWarn']):
            rpmAnim.itemconfigure(rpmBarRect,fill='orange',outline='orange')
        # Check for low revs (car stalled)
        elif rpmRaw < 600:
            rpmAnim.itemconfigure(rpmBarRect,fill='white',outline='white')
            time.sleep(.125)
            rpmAnim.itemconfigure(rpmBarRect,fill='black',outline='black')  
        else:
            rpmAnim.itemconfigure(rpmBarRect,fill='blue',outline='blue')
        time.sleep(.125 if rpmRaw > int(config['RPM']['rpmAlarm']) or rpmRaw < 1000 else .01) # Add slightly more delay when the bar is flashing
        

if config['Basic']['dynamicRedline'] == True:
    pass

# Start threads
rpmBarThread = Thread(target=rpmBarThr)
TextThr = Thread(target=textThread)
rpmBarThread.start()
TextThr.start()


hudRoot.mainloop()