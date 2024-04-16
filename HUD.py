# Make Tkinter do its thing
from tkinter import *
from tkinter import ttk

# Local stuff
from localModules.configCreator import configCheck,configVer
from localModules.obdReader import rawDict
import localModules.obdReader as obdR
from localModules.obdLogic import gearLogic,SmartShift,allGears
# The rest
import configparser
from threading import Thread
import time
import os


### TO BE IMPLEMENTED
# TODO add speed offset (hard value or percent)
# TODO add battery voltage
# TODO add Brake and clutch position (or jut on off)
# TODO add steering wheel position graph thing
# TODO add optional race info section
# TODO add odometer
# TODO add tire pressure and temp
# TODO add general warning light/alert
# TODO add fuel status (mpg, tank status, range, etc)
# TODO add outdoor air temp
# TODO get variable redline working
# TODO add speedlimit warning/option
# TODO Get proShift data into smartShift so correct gear is displayed


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

if config['Version']['ConfigVer'] != configVer:
    print('Config Version Mismatch!')
    # exit()

bgColour = config['General']['background']
fgColour = config['General']['text']



# Start creation of the HUD
hudRoot = Tk()
hudRoot.title('MainHUD')
hudRoot.attributes("-fullscreen", True)

# Size of RPi display
hudRoot.geometry('800x480')
hudRoot.configure(bg=bgColour)

# Centers the dash
hudMain = Frame(hudRoot)
hudBufferL = Frame(hudRoot)
hudBufferR = Frame(hudRoot,width=10)
hudBufferL.grid(column=0,row=0,rowspan=2)
hudBufferR.grid(column=2,row=0, rowspan=2)
hudMain.grid(column=1,row=1, sticky=(E, W, S))

## Create the RPM frame (might not be needed)
RPMBar = Frame(hudRoot,height=40,width=720,background=bgColour,borderwidth=0,highlightthickness=0)
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


# Variables to be updated from OBD
rpm = StringVar()
voltage = StringVar()
gear = StringVar()
speed = StringVar()

shiftHint = StringVar()
shiftHintIc = StringVar()
steeringPos = StringVar()
throttlePos = StringVar()
speedUnit = StringVar()
coolantTemp = StringVar()
connectStatus = StringVar()
connectStatus.set('')

# Currently selected speed units
speedUnit.set('UNK')
#rpmRaw = 999
# speedRaw = 132
inNeutralRaw = 0
throttlePosRaw = 6
# coolantTempRaw = 35


# Keep updating variables
# Most values from obd are returned in Pint format which I've never used, sorry in advance for whatever i do
def refreshOBD():
    global rawDict
    
    # Start OBD thread, request OBD connection details if none present
   
    while config['General']['obdConnection'] == '':
        connectStatus.set('Missing OBD Config!')
        time.sleep(1)
        
    # Send new config info, terrible awful I hate it.
    obdDetails = config['General']['obdConnection'].split(',')[0]
    baudRate = config['General']['obdConnection'].split(',')[1]
    obdThread = Thread(target=obdR.readOBD,args=(obdDetails,baudRate,))
    obdThread.start()
    
    # Allow generaton of dictionary
    time.sleep(4)
    
    connectStatus.set(obdR.obdConnectStatus)
    while obdR.obdConnectStatus != 'Failed to connect':
        connectStatus.set(obdR.obdConnectStatus)
        # TODO Find a better way to do this, maybe the same way its done in the other function, dictionary loop
        for dataName, dataValue in rawDict.items():
                
            
            # Special changes as needed
            if dataName == 'speed':
                if eval(config['General']['speed'])[0] == 'MPH':
                    speed.set(int(rawDict['speed']*0.621371))
                    speedUnit.set('MPH')
                else:
                    speed.set(int(rawDict['speed']))
                    speedUnit.set('KPH')
            else:
            # Set new values
                try:
                    # print(f'{dataName}.set(int(dataValue))')
                    exec(f'{dataName}.set(int(dataValue))')
                    
                except(NameError,ValueError):
                    print(f'{dataName} could not be set or is not used')
    
        # Gear
        if inNeutralRaw == 1:
            gear.set('N')
        else:
            gearR = gearLogic(rawDict['rpm'],rawDict['speed']*0.621371)
            gear.set(gearR)
            smartS = SmartShift(gearR,rawDict['rpm'],rawDict['throttlePos'])
            shiftHint.set(smartS[0])
            shiftHintIc.set(smartS[1])
        time.sleep(.01)

refreshData = Thread(target=refreshOBD)
refreshData.start()

# 3x2 frames (tl = Top left, etc)
tlFrame = Frame(hudMain, width=240, height=220, background=bgColour)
tcFrame = Frame(hudMain, width=240, height=220, background=bgColour)
trFrame = Frame(hudMain, width=240, height=220, background=bgColour)
blFrame = Frame(hudMain, width=240, height=220, background=bgColour)
bcFrame = Frame(hudMain, width=240, height=220, background=bgColour)
brFrame = Frame(hudMain, width=240, height=220, background=bgColour)

# For some reason this makes the frames work better idk
tlFrame.grid(column=0, row=0, sticky=(N))
tcFrame.grid(column=1, row=0, sticky=(N))
trFrame.grid(column=2, row=0, sticky=(N, E))
blFrame.grid(column=0, row=1, sticky=(S, W))
bcFrame.grid(column=1, row=1, sticky=(S))
brFrame.grid(column=2, row=1, sticky=(S, E))


# Prevent resizing or does it idk
bcFrame.grid_propagate(0)
tcFrame.grid_propagate(0)
trFrame.grid_propagate(0)
brFrame.grid_propagate(0)

### BOTTOM LEFT

# Connection status display
obdStr = StringVar()
obdEntry = Entry(blFrame,textvariable=obdStr,font=("Ariel",10))
def saveConnection():
    data = obdEntry.get()
    obdStr.set(data)
    config.set('General','obdConnection', data)
    with open('dash_config.ini', 'w') as configfile:
        config.write(configfile)
        
        
connectStatusDisp = ttk.Label(blFrame,textvariable=connectStatus,justify='center', font=("Roboto",20))
    
if config['General']['obdConnection'] == '':
    save = Button(blFrame, text="Save", command = saveConnection)
    obdEntry.grid(column=0,row=0,sticky=(S, W))
    save.grid(column=1,row=0,sticky=(S))
connectStatusDisp.grid(column=0,row=1, columnspan=2,sticky=(S, W))

### BOTTOM RIGHT
## ProShift - Show all available gears, and what RPM you would be at if you shifted

def proShiftThread():
    proShiftCanv = Canvas(brFrame,width=200,height=200)
    proShiftCanv.pack()
    proShiftData = allGears(rawDict['speed']*0.621371,int(eval(config['General']['redline'])[0]))
    gearNum = 1
    proShiftY=15
    for x in proShiftData:
        exec(f'gear{gearNum} = proShiftCanv.create_text(10,proShiftY,text="nonsense",anchor="w",font=("Roboto",30))')
        gearNum+=1
        proShiftY +=30
    while True:
        proShiftData = allGears(rawDict['speed']*0.621371,int(eval(config['General']['redline'])[0]))
        gearNum = 1
        for gearD,rpmD in proShiftData.items():
            gearTemp = 'gear'+str(gearNum)
            proShiftCanv.itemconfigure(eval(gearTemp),text=f'{gearD}: {rpmD}')
            gearNum+=1
    

### TOP CENTRE

## Text/variable displays
## Speed
speedUnitDisp = Label(tcFrame,textvariable=speedUnit,justify='center', font=("Roboto",20,'bold'),fg=fgColour,bg=bgColour)
speedDisplay = Label(tcFrame,textvariable=speed,justify='center', font=("Roboto",100),fg=fgColour,bg=bgColour)

### BOTTOM CENTRE

## Gears
gearText = Label(bcFrame,text='Gear', font=("Roboto",20,'bold'),fg=fgColour,bg=bgColour)
gearSelect = Label(bcFrame,textvariable=gear, font=("Roboto",90),fg=fgColour,bg=bgColour)
shiftHintDisp = Label(bcFrame,textvariable=shiftHint,anchor='center', font=("Roboto",30),fg=fgColour,bg=bgColour)
shiftHintRecDisp = Label(bcFrame,textvariable=shiftHintIc,anchor='center', font=("Roboto",30),fg=fgColour,bg=bgColour)


#Show it
speedUnitDisp.grid(column=1,row=0)
speedDisplay.grid(column=1,row=1)
gearSelect.grid(column=1,row=1)
gearText.grid(column=1,row=0)
shiftHintDisp.place(x=155,y=60)
shiftHintRecDisp.place(x=180,y=60)

# Keep the text in the middle (it likes to run around otherwise)
bcFrame.columnconfigure(0, weight=1)
bcFrame.columnconfigure(2, weight=1) 
tcFrame.columnconfigure(0, weight=1)
tcFrame.columnconfigure(2, weight=1) 


### RIGHT SIDE FULL

## Coolant temp  bar
CoolantTempCanv = Canvas(hudBufferR,height=480, width=40,highlightthickness=1,background='black')
coolantTempBar = CoolantTempCanv.create_rectangle(40,480,0,0,fill='green',outline='green')
coolantTempDisp = CoolantTempCanv.create_text(20,220,text='1234',anchor='center',font=("Roboto",20),fill=fgColour)
CoolantTempCanv.pack(side='right',fill='both', expand=True)

### TOP RIGHT

## Throttle Pos bar
throttleBackGr = Canvas(trFrame,height=100, width=20,highlightthickness=1,background='grey')
throttleBarRect = throttleBackGr.create_rectangle(0,90,20,100,fill='blue',outline='blue')
throttleBackGr.pack()

### TOP FULL

## RPMs
rpmAnim = Canvas(RPMBar,width=720,highlightthickness=0,background='orange')
rpmBarRect = rpmAnim.create_rectangle(0,0,10,40,fill='blue',outline='blue')
rpmNumDisp = rpmAnim.create_text(360,20,text='1234',anchor='center',font=("Roboto",30))
rpmAnim.pack()

def textThread():
    # Display RPM bar
    while True:
        rpmAnim.itemconfigure(rpmNumDisp,text=rawDict['rpm'])
        time.sleep(.01)
        
def slowRefresh(sleep=1):
    # For items that don't need to be checked every .01 seconds
    
    # Convert coolant temp to value that can be displayed on the bar
    maxCoolantTemp = int(eval(config['General']['coolantmaxc'])[0])
    coolantMultiplier = 480 / maxCoolantTemp
    
    def coolantColour(colour,outline=False):
        if outline == False:
            outline = colour
        CoolantTempCanv.itemconfigure(coolantTempBar,fill=f'{colour}',outline=f'{outline}')
        
    
    #Main loop
    while True:
        #Coolant
        CoolantTempCanv.itemconfigure(coolantTempDisp,text=rawDict['coolantTemp'])
        CoolantTempCanv.coords(coolantTempBar,40,480-rawDict['coolantTemp']*coolantMultiplier,0,480)
        
        
        if rawDict['coolantTemp'] > maxCoolantTemp:
            #Overheating!
            coolantColour('red')
        elif rawDict['coolantTemp'] > int(maxCoolantTemp*.8):
            #Too hot!
            coolantColour('orange')
            # Too cold!
        elif rawDict['coolantTemp'] < int(maxCoolantTemp*.4):
            coolantColour('blue')
        else:
            coolantColour('green')
        # Check for high temps
        
        time.sleep(sleep)
    
# RPM Bar thread
def rpmBarThr():
    global rpmAnim
    
    #Start delay
    time.sleep(5)
    
    def rpmColour(colour,outline=False):
        if outline == False:
            outline = colour
        rpmAnim.itemconfigure(rpmBarRect,fill=f'{colour}',outline=f'{outline}')  
    
    # Multiplier to convert rpmRaw to the bar dimensions(locked for now)
    rpmMultiplier = 720 / int(eval(config['General']['redline'])[0])
    
    while True:
        # Phasing out old data still
        rpmVal = rawDict['rpm']
        
        # Adjust display bars
        rpmAnim.coords(rpmBarRect,0,0,rpmVal*rpmMultiplier,40)
        throttleBackGr.coords(throttleBarRect,0,100-rawDict['throttlePos'],20,100)


        # Normal revs
        if rpmVal < int(eval(config['RPMWarnings']['rpmWarn'])[0]) and rpmVal > 600:
            rpmColour('blue')
        # Check for low revs (car stalled)
        elif rpmVal < 600:
            rpmColour('white')
            time.sleep(.125)
            rpmColour('black')

        # Check for high revs
        elif rpmVal > int(eval(config['RPMWarnings']['rpmAlarm'])[0]):
            rpmColour('red')
            time.sleep(.125)
            rpmColour('orange')
            
        elif rpmVal > int(eval(config['RPMWarnings']['rpmAlert'])[0]):
            rpmColour('red')
            
        elif rpmVal > int(eval(config['RPMWarnings']['rpmWarn'])[0]):
            rpmColour('orange')

        else:
            rpmColour('blue')
            
        time.sleep(.125 if rpmVal > int(eval(config['RPMWarnings']['rpmAlarm'])[0]) or rpmVal < 1000 else .01) # Add slightly more delay when the bar is flashing
        

#if config['Preferences']['dynamicRedline'] == True:
 #   pass

#Threads
rpmBarThread = Thread(target=rpmBarThr)
TextThr = Thread(target=textThread)
slowThr = Thread(target=slowRefresh)
proShiftThr = Thread(target=proShiftThread)

# Start em
rpmBarThread.start()
slowThr.start()
TextThr.start()

# Optional threads
#if config['Preferences']['proShift'] == True:
proShiftThr.start()
    
    

hudRoot.mainloop()
