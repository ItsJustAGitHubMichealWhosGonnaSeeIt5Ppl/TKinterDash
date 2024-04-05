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
friendlyNames['Version'] = {
    'hudver': 'HUD Version',
    'configver': 'Config File Version',
    'pythonobdver': 'Python OBD Version'
}



def configMenu(config=False):

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
    cMenuInfo = Canvas(cMenuRoot,height=110, width=400)

    cMenuInfo.create_text(200,20,text='About',anchor='center',font=("Roboto",30,'bold'))
    posY = 20
    for name,value in config['Version'].items():
        posY +=25
        if friendlyNames['Version'][name] != None:
            name = friendlyNames['Version'][name]
        
        cMenuInfo.create_text(200,posY,text=f'{name}: {value}',anchor='center',font=("Roboto",15,))
    cMenuInfo.pack()
    
    
    # Settings tab creation
    
    cMenuTabCanvas = Canvas(cMenuRoot,scrollregion=(0,0,1000,1000))
    cMenuTabFrame = Frame(cMenuTabCanvas)
    cMenuTabScrollbar = Scrollbar(cMenuRoot,orient="vertical", command=cMenuTabCanvas.yview)
    cMenuTabCanvas.configure(yscrollcommand=cMenuTabScrollbar.set)
    
    cMenuTabScrollbar.pack(side="right", fill="y")
    cMenuTabCanvas.pack(side="left", fill="both", expand=True)
    cMenuTabCanvas.create_window((4,4), window=cMenuTabFrame, anchor="nw")
    
    
    
    class ConfigActions:
        def __init__(self,mainFrame,sectionName,name,value,row):
            self.value = StringVar()
            self.valueR = value
            self.name = name
            self.frame = mainFrame
            self.section = sectionName
            self.row = row
            #Create item name
            Label(self.frame,text=self.name,font=("Font",15)).grid(column=0,row=self.row)
            
        def createSpinboxRow(self):
            #Create value
            self.value.set(self.valueR[0])
            print(self.valueR[0])
            self.entry = Spinbox(self.frame,width=4,from_=self.valueR[1][0],to=self.valueR[1][1],textvariable=self.value)
            self.entry.grid(column=1,row=self.row)
            #Button to save new value
            Button(self.frame,text='Save', command=self.SpinboxAction).grid(column=2,row=self.row)
            
        def SpinboxAction(self):
            newValueRaw = self.entry.get()
            self.value.set(self.entry.get())
            #Check if new value is a number
            if newValueRaw.isdigit():
                newValueRaw = int(newValueRaw)
            self.newVal = (newValueRaw, self.valueR[1])
            self.updateConfig()
            
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
        
        def validate(self):
            pass
        
        def updateConfig(self):
            config.set(f'{self.section}', f'{self.name}', f'{self.newVal}')
            with open('dash_config.ini', 'w') as configfile:
                config.write(configfile)
            
            

    def createTabData(mainFrame,configSection):
        Label(mainFrame,text=configSection,font=("Font",30,'bold')).grid(column=0,row=0,columnspan=3)
        vertVar=1
        
        for name, value in config[configSection].items():
            value = eval(value)
            # Create class item
            lineItem = ConfigActions(mainFrame,configSection,name,value,vertVar)
            # Figure out item type
            if type(value) is bool:
                lineItem.createCheckboxRow()
            elif type(value[0]) is int or value[0].isdigit():
                lineItem.createSpinboxRow()
            elif type(value) is tuple:
                lineItem.createRadiobuttonRow()
            
            vertVar+=1
    
    createTabData(cMenuTabFrame,'General')
    cMenuRoot.mainloop()


# Allow config menu to be opened on its own
if __name__ == '__main__':
    configMenu()