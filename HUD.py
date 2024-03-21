# Make Tkinter do its thing
from tkinter import *
from tkinter import ttk

# Local stuff
from localModules.configCreator import configCheck
import localModules.obdReader as obdR
# The rest
import configparser
from threading import Thread
import time
import pint


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
hudBuffer = Frame(hudRoot)
hudBuffer2 = Frame(hudRoot)
hudBuffer.grid(column=0,row=0,rowspan=2)
hudBuffer2.grid(column=2,row=0, rowspan=2)
hudMain.grid(column=1,row=1, sticky=(E, W, S))

## Create the RPM frame (might not be needed)
RPMBar = Frame(hudRoot,height=40,width=720,background='black',borderwidth=0,highlightthickness=0)
RPMBar.grid(column = 1, row = 0,sticky=(E, W, N))


# Create box for everything, also maybe helps with macOS.  sticky will anchor us to the walls (I think)
# allows for resizing? < No it keeps it all centered
hudRoot.columnconfigure(0, weight=1)
hudRoot.columnconfigure(2, weight=1) 
hudRoot.rowconfigure(1, weight=1)

#Stop RPM bar from resizing except I think this doesnt
RPMBar.pack_propagate(0)

# Fix styling issues for mac? 
style = ttk.Style(hudMain)
style.theme_use('classic')


# Variables to be updated from OBD
rpm = StringVar()
gear = StringVar()
speed = StringVar()
steeringPos = StringVar()
throttlePos = StringVar()
speedUnit = StringVar()
coolantTemp = StringVar()


# Currently selected speed units
speedUnit.set(config['Required']['speedUnits'])

# Trash data for debug
rpmRaw = 1001
speedRaw = 10
throttlePosRaw = 0
speed.set(speedRaw)

# Keep updating variables
# Values from obd are returned in Pint format which I've never used, sorry in advance for whatever i do
def refreshOBD():
    global rpmRaw,rpm
    time.sleep(5)
    while False and obdR.carConnected !=True:
        # Wiat for the car to actually turn on
        time.sleep(2)
    while True:
        # gear.set('?')
         # steeringPos.set(0)
        
        # RPM data
        rpmRaw = int(obdR.responseDict['rpm'])
        rpm.set(rpmRaw)
        
        # TODO make a seperate module that checks for config every second or something.
        # convert speed if needed, I know it can be cleaner.    
        if config['Required']['speedUnits'] == 'MPH':
            speedRaw = int(obdR.responseDict['speed'])
        else:
            speedRaw = int(obdR.responseDict['speed'])
        speed.set(speedRaw)
       
        #Throttle data
        throttlePosRaw = obdR.responseDict['throttlePos']
        throttlePos.set(f'Gas Pedal: {throttlePosRaw}')
        
        #Coolant
        # TODO allow temp unit chaning
        coolantRaw = obdR.responseDict["coolantTemp"]
        coolantTemp.set(f'Coolant: {coolantRaw}')
       
        time.sleep(.01)
        
        
refreshData = Thread(target=refreshOBD)
if debug == False: refreshData.start()

# 3x2 frames (tl = Top left, etc)
tlFrame = Frame(hudMain,width=240,height=220, background='red')
tcFrame = Frame(hudMain, width=240,height=220)
trFrame = Frame(hudMain, width=240,height=220,background='blue')
blFrame = Frame(hudMain, width=240,height=220,background='yellow').grid(column=0,row=1, sticky=(S, W))
bcFrame = Frame(hudMain, width=240,height=220,background='green')
brFrame = Frame(hudMain, width=240,height=220,background='purple').grid(column=2,row=1, sticky=(S, E))

# For some reason this makes the frames work better idk
tlFrame.grid(column=0,row=0, sticky=(N))
tcFrame.grid(column=1,row=0, sticky=(N))
bcFrame.grid(column=1,row=1, sticky=(S))
trFrame.grid(column=2,row=0, sticky=(N, E))

# Prevent resizing or does it idk
bcFrame.grid_propagate(0)


### Text/variable displays
## Speed
speedUnitDisp = ttk.Label(tcFrame,textvariable=speedUnit,justify='center', font=("Roboto",20))
speedDisplay = ttk.Label(tcFrame,textvariable=speed,justify='center', font=("Roboto",120))

#Show it
speedUnitDisp.grid(column=0,row=0)
speedDisplay.grid(column=0,row=1)


## Gears
gearText = ttk.Label(bcFrame,text='Gear', font=("Roboto",20))
gearSelect = ttk.Label(bcFrame,textvariable=gear, font=("Roboto",90))

# Actually display it
gearSelect.grid(column=1,row=1)
# gearSelect.place(x=120,y=150,anchor=S) < OLD dont use
gearText.grid(column=1,row=0)

# Keep the text in the middle (it likes to run around otherwise)
bcFrame.columnconfigure(0, weight=1)
bcFrame.columnconfigure(2, weight=1) 

## Misc for testing
throttleDisplay = ttk.Label(trFrame,textvariable=throttlePos,justify='center', font=("Roboto",20))
tempDisplay = ttk.Label(trFrame,textvariable=coolantTemp,justify='center', font=("Roboto",20))
throttleDisplay.grid(column=0,row=0)

tempDisplay.grid(column=0,row=1)
## RPMs
# Center the RPM text
#RPMBar.columnconfigure(0, weight=1)
#RPMBar.columnconfigure(2, weight=1) 

rpmAnim = Canvas(RPMBar,width=720,highlightthickness=0)
rpmBarRect = rpmAnim.create_rectangle(0,0,10,40,fill='blue',outline='blue')
rpmNumChange = rpmAnim.create_text(360,20,text='1234',anchor='center',font=("Roboto",30))
rpmAnim.pack()

# RPM Bar thread
def rpmBarThr():
    global rpmAnim
    global rpmRaw
    
    # Multiplier to convert rpmRaw to the bar dimensions(locked for now)
    rpmMultiplier = 720 / int(config['Required']['redline'])
    while True:
        # Display RPM bar
        # TODO Possibly move the RPM number and bar movement to their own thread to it can be smoother.
        rpmAnim.coords(rpmBarRect,0,0,rpmRaw*rpmMultiplier,40)
        
        # Display RPM number onscreen
        rpmAnim.itemconfigure(rpmNumChange,text=str(rpmRaw))

        
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
rpmBarThread.start()
hudRoot.mainloop()