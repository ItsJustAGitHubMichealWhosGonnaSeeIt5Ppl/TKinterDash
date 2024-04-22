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

friendlyNames = {}
# Friendly names for config items
friendlyNames['Tabs'] = {
    'Version':'About',
    'useCustomData': 'Advanced'
}

friendlyNames['Version'] = {
    'hudver': 'HUD Version',
    'configver': 'Config File Version',
    'pythonobdver': 'Python OBD Version'
}
friendlyNames['General'] = {
    'redline': 'Redline',
    'coolantmaxc': 'Coolant Max Temp',
    'gears': 'Gears',
    'speed': 'Speed Units',
    'distance': 'Distance Units',
    'temperature': 'Temp Units',
}





    # Get config data
config = configparser.ConfigParser()
if configCheck() == True:
    config.read('dash_config.ini')
else:
    print('Tried to read/create config file and failed')
    exit()
# Build menu
cMenuRoot = Tk()
cMenuRoot.title('Settings')
# Size of RPi display
cMenuRoot.geometry('600x400')
cMenuRoot.configure(bg='grey')



# Create a bar to hold menu options
cMenuTabBar = ttk.Notebook(cMenuRoot)

# Settings tab creation

"""     cMenuTabCanvas = Canvas(cMenuRoot,scrollregion=(0,0,1000,1000))
cMenuTabFrame = Frame(cMenuTabCanvas)
cMenuTabScrollbar = Scrollbar(cMenuRoot,orient="vertical", command=cMenuTabCanvas.yview)
cMenuTabCanvas.configure(yscrollcommand=cMenuTabScrollbar.set)

cMenuTabScrollbar.pack(side="right", fill="y")
cMenuTabCanvas.pack(side="left", fill="both", expand=True)
cMenuTabCanvas.create_window((4,4), window=cMenuTabFrame, anchor="nw") """

    
    
    
    
    
class ConfigActions:
    def __init__(self,mainFrame,sectionName,name,value,row):
        self.value = StringVar()
        self.valueR = value
        self.name = name
        self.frame = mainFrame
        self.section = sectionName
        self.row = row
        #Create item name
        try:
            self.fname = friendlyNames[self.section][self.name]
        except:
            self.fname = self.name
        Label(self.frame,text=self.fname,font=("Font",15)).grid(column=0,row=self.row)
    
    def createTextRow(self):
        #Friendly name check
        self.textRow = Label(self.frame,text=self.valueR,font=("Roboto",15,))
        self.textRow.grid(column=1,row=self.row)
    def createSpinboxRow(self):
        #Create value
        self.value.set(self.valueR[0])
        print(self.valueR[0])
        self.entry = Spinbox(self.frame,width=4,from_=self.valueR[1][0],to=self.valueR[1][1],textvariable=self.value,increment=0.001)
        self.entry.grid(column=1,row=self.row)
        #Button to save new value
        Button(self.frame,text='Save', command=self.SpinboxAction).grid(column=2,row=self.row)
        
    def SpinboxAction(self):
        value = self.entry.get()
        try:
            value = float(value)
            
        except(ValueError):
            errormsg = 'Input is not a number!'
            popupAlert(errormsg)
            self.value.set(self.valueR[0])
        
        if value == int(value):
                value = int(value)
                
        if value > self.valueR[1][0] and value < self.valueR[1][1]:
            self.value.set(value)
            self.newVal = (value, self.valueR[1])
            self.updateConfig()
        else:
            # Is a number, but not in the range
            errormsg = f"Number not in range! ({self.valueR[1][0]} - {self.valueR[1][1]})"
            popupAlert(errormsg)
            self.value.set(self.valueR[0])
            
    def createCheckboxRow(self):
        self.checkToggle = IntVar()
        self.checkToggle.set(1 if self.valueR == True else 0)
        self.entry = Checkbutton(self.frame,variable=self.checkToggle,command=self.checkboxAction)
        self.entry.grid(column=1,row=self.row,columnspan=2)
        
    def checkboxAction(self):
        self.newVal = True if self.checkToggle.get() == 1 else False
        print(self.newVal)
        self.updateConfig()
        
    def createRadiobuttonRow(self):
        self.radioVar = StringVar()
        self.radioVar.set(self.valueR[0])
        self.entry1 = Radiobutton(self.frame,text=self.valueR[1][0],variable=self.radioVar,value=self.valueR[1][0],command=self.radioAction)
        self.entry1.grid(column=1,row=self.row)
        self.entry2 = Radiobutton(self.frame,text=self.valueR[1][1],variable=self.radioVar,value=self.valueR[1][1],command=self.radioAction)
        self.entry2.grid(column=2,row=self.row)       
    
    def radioAction(self):
        self.newVal = (str(self.radioVar.get()), self.valueR[1])
        self.updateConfig()
    
    def updateConfig(self):
        config.set(f'{self.section}', f'{self.name}', f'{self.newVal}')
        with open('dash_config.ini', 'w') as configfile:
            config.write(configfile)

class createTabStruct:
    def __init__(self,tabFrame,title,row):
        self.title = str(title)
        self.row = int(row)
        self.tabFrame = tabFrame
        # Check for friendlynames of tabs
        try:
            self.fTitle = friendlyNames['Tabs'][self.title]
        except:
            self.fTitle = self.title
    def createTab(self):
        # Create tabs for config items
        topLevelFrame = Frame(self.tabFrame)
        tabChildFrame = Canvas(topLevelFrame,scrollregion=(0,0,10,400))
        innerTabFrame = Frame(tabChildFrame)
        cMenuTabScrollbar = Scrollbar(topLevelFrame,orient="vertical", command=tabChildFrame.yview)
        tabChildFrame.configure(yscrollcommand=cMenuTabScrollbar.set)
        
        cMenuTabScrollbar.pack(side="right", fill="y")
        tabChildFrame.pack(side="left", fill="both", expand=False)
        tabChildFrame.create_window((0,0), window=innerTabFrame, anchor="nw")
        self.tabFrame.add(topLevelFrame,text=self.fTitle)
        
        #Create tab items
        createTabData(innerTabFrame,self.title,self.fTitle)
        
        
def popupAlert(alertText):
    popup = Tk()
    popup.wm_title("Error")
    label = Label(popup,text=alertText,font=("Ariel",10))
    label.pack(side="top", fill="x", pady=10)
    closeButton = ttk.Button(popup, text="Okay", command = popup.destroy)
    closeButton.pack()
    popup.mainloop()

def createTabData(mainFrame,configSection,configSName):
    Label(mainFrame,text=configSName,font=("Font",30,'bold')).grid(column=0,row=0,columnspan=3)
    vertVar=1
    
    for name, value in config[configSection].items():
        try:
            value = eval(value)
        except(SyntaxError,NameError):
            value = value
        # Create class item
        if name in ['obdconnection']:
            # Skip
            continue
        
        lineItem = ConfigActions(mainFrame,configSection,name,value,vertVar)
        
        if configSection in ['Version']:
            # Manually define certain row types
            lineItem.createTextRow()
        
        elif name in ['finaldrive']:
            lineItem.createSpinboxRow()
            # It gets mad idk
        # Figure out item type
        elif type(value) is bool:
            lineItem.createCheckboxRow()
        elif type(value[0]) is int or value[0].isdigit():
            lineItem.createSpinboxRow()
        elif type(value) is tuple:
            lineItem.createRadiobuttonRow()
        else:
            lineItem.createTextRow()
        
        vertVar+=1

titleNum = 0
for title in config:        
    if title in ['DEFAULT']:
        #Do not create row
        continue
    else:
        
        titleItem = createTabStruct(cMenuTabBar,title,titleNum)
        titleItem.createTab()
        titleNum+=1
    print(title)
cMenuTabBar.pack(fill='y',expand=True)

# createTabData(cMenuTabFrame,'General')
cMenuRoot.mainloop()


# Allow config menu to be opened on its own
# if __name__ == '__main__':
#     configMenu()