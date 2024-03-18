from tkinter import *
from tkinter import ttk
from threading import Thread
import time


#### Config ####
redline = 7700
gears = 6
units = 'placeholder'

"""User Config - Will be changeable in the dash on the fly"""
# RPM bar will be orange
rpmWarn = 5000
# RPM bar will be red
rpmAlert = 6000
# RPM bar will flash
rpmAlarm = 7000




hudRoot = Tk()
hudRoot.title('TestHud')
# Size of RPi display ~
hudRoot.geometry('800x480')


# Centers the dash
hudMain = Frame(hudRoot)
hudBuffer = Frame(hudRoot)
hudBuffer2 = Frame(hudRoot)
hudBuffer.grid(column=0,row=0,rowspan=2)
hudBuffer2.grid(column=2,row=0, rowspan=2)
hudMain.grid(column=1,row=1, sticky=(E, W, S))
RPMBar = Frame(hudRoot,height=40,width=720,background='black',borderwidth=0,highlightthickness=0)
RPMBar.grid(column = 1, row = 0,sticky=(E, W, N))
# Create box for everything, also maybe helps with macOS.  sticky will anchor us to the walls (I think)

# allows for resizing? < No it keeps it all centered
hudRoot.columnconfigure(0, weight=1)
hudRoot.columnconfigure(2, weight=1) 
hudRoot.rowconfigure(1, weight=1)

#Stop RPM bar from resizing
RPMBar.pack_propagate(0)

# Fix styling issues for mac? 
style = ttk.Style(hudMain)
style.theme_use('classic')

# Variables to be updated from OBD
gear = StringVar()
gear.set('?')
rpmRaw = 1234
rpm = StringVar()
rpm.set(rpmRaw)
speed = StringVar()
speed.set(123)
steeringPos = StringVar()
steeringPos.set(0)
MvK = StringVar()
MvK.set('MPH')

## Start threads here
def rpmGet():
    pass
def gearGet():
    pass
def steeringPosGet():
    pass
def speedGet():
    pass

# rpmthread = threading(thread='rpmGet')



# 3x2 frames (tl = Top left, etc)
tlFrame = Frame(hudMain,width=240,height=220, background='red')
tcFrame = Frame(hudMain, width=240,height=220)
trFrame = Frame(hudMain, width=240,height=220,background='blue').grid(column=2,row=0, sticky=(N, E))
blFrame = Frame(hudMain, width=240,height=220,background='yellow').grid(column=0,row=1, sticky=(S, W))
bcFrame = Frame(hudMain, width=240,height=220,background='green')
brFrame = Frame(hudMain, width=240,height=220,background='purple').grid(column=2,row=1, sticky=(S, E))
tlFrame.grid(column=0,row=0, sticky=(N))
tcFrame.grid(column=1,row=0, sticky=(N))
bcFrame.grid(column=1,row=1, sticky=(S))
# Prevent resizing
bcFrame.grid_propagate(0)

### Text/variable displays
## Speed
speedMode = ttk.Label(tcFrame,textvariable=MvK,justify='center', font=("Roboto",20))
speedDisplay = ttk.Label(tcFrame,textvariable=speed,justify='center', font=("Roboto",120))

#Show it
speedDisplay.grid(column=0,row=1)
speedMode.grid(column=0,row=0)

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

 
## RPMs
# Adding this causes chaos
if True:
    # Center the RPM text
    #RPMBar.columnconfigure(0, weight=1)
    #RPMBar.columnconfigure(2, weight=1) 
    rpmNum2 = 350
    mode = '+'
    rpmAnim = Canvas(RPMBar,width=720,highlightthickness=0)
    rpmBarRect = rpmAnim.create_rectangle(0,0,10,40,fill='blue',outline='blue')
    rpmNumChange = rpmAnim.create_text(360,20,text='1234',anchor='center',font=("Roboto",30))
    rpmAnim.pack()
    
    
    #Testing RPM bar thread
    def rpmThreadTest():
        global mode
        global rpmNum2
        global rpmAnim
        while True:
            if mode == '+' and rpmNum2 > 700:
                mode = '-'
            elif mode == '-' and rpmNum2 < 10:
                mode = '+'
                
            rpmRaw = rpmRaw + 1 if mode=='+' else rpmRaw - 1
            time.sleep(.05)
            rpmAnim.coords(rpmBarRect,0,0,rpmNum2,40)
            rpm.set(rpmRaw)
            
    
    rpmThreadTestStarter = Thread(target=rpmThreadTest)
    rpmThreadTestStarter.start()
    
    # RPM Bar thread
    def rpmBarThr():
        global colorGate
        global rpmNum2
        global rpmAnim
        
        # Multiplier to convert rpmRaw to the bar dimensions(locked for now)
        rpmMultiplier = 720 / redline
        while True:
            # Display RPM bar
            rpmAnim.coords(rpmBarRect,0,0,rpmRaw*rpmMultiplier,40)
            
            # Display RPM number onscreen
            rpmAnim.itemconfigure(rpmNumChange,text=str(rpmRaw))

            
            # Check for high revs
            if rpmRaw > rpmAlarm:
                rpmAnim.itemconfigure(rpmBarRect,fill='red',outline='orange')
                time.sleep(.125)
                rpmAnim.itemconfigure(rpmBarRect,fill='orange',outline='red')  
            elif rpmRaw > rpmAlert:
                rpmAnim.itemconfigure(rpmBarRect,fill='red',outline='red')
            elif rpmRaw > rpmWarn:
                rpmAnim.itemconfigure(rpmBarRect,fill='orange',outline='orange')
            elif rpmRaw < 1000:
                rpmAnim.itemconfigure(rpmBarRect,fill='white',outline='while')
                time.sleep(.125)
                rpmAnim.itemconfigure(rpmBarRect,fill='black',outline='black')  
            else:
                rpmAnim.itemconfigure(rpmBarRect,fill='blue',outline='blue')
            time.sleep(.05 + .75 if rpmRaw > rpmAlarm or rpmRaw < 1000 else 0) # Add slightly more delay when the bar is flashing
               
            
    Thread(target=rpmBarThr).start()
    # RPM bar 
    

    
    # Another text option
    
    
    #rpmNum = ttk.Label(RPMBar,textvariable=rpm,justify='center', font=("Roboto",30))
    #rpmNum.place(x=300)

hudRoot.mainloop()