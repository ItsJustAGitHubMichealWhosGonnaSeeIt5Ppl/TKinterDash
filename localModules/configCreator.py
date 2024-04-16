import configparser
import os


""" 
######  CHANGELOG ######
## 0.0.24 
- Added gear section and gear ratios 
## 0.0.25
- Removed individual gear rations, these will need to be added by the config menu tool or the whole thing will be a mess
- Set max gears to 9
- Added toggles for smartShift and proShift.
## 0.0.26
- Added OBD connection config item under General to allow connection type/line to be set during the initial launch
- Added text and background colour config options
"""


"""Config - Will be changeable in the dash as needed"""
configVer = '0.0.26'

# TODO make use of config settings
# TODO Add user interface to change all this
def configCheck(ForceRecreate=False):
    config = configparser.ConfigParser()

    # Check if config already exists, read it if it does.
    if os.path.isfile('dash_config.ini') and ForceRecreate == False: 
        return True
    else:
        # Allow for prompting if something has updated
        config['Version'] = {
            'HUDVer': '?',
            'ConfigVer': configVer,
            'PythonOBDVer': '?'
        }
        
        # Needed to work at all
        config['General'] = {
            'obdConnection': '',
            'redline': (7700,[100,10000]),
            'coolantMaxC': (130,[60,220]), # Maximum coolant temp in Celcius
            'gears': (6, [1,9]),
            'speed':('MPH',['MPH','KPH']),
            'distance':('Miles', ['Miles','Kilometers']),
            'temperature': ('F', ['F','C']),
            'background': 'black',
            'text': 'white',
        }
        
        # Basic settings that don't have another home
        config['Preferences'] = {
            'dynamicRedline': False, # Lower redline when car is warming up
            'speedWarning': False,
            'speedWarningVal': (150,[0,300]),
            'smartShift': False,
            'proShift':False,
            'RPMWarnings': False,
        } 

        config['Integrations'] = {
            'OpenDsh': False, # OpenDash
            'ACC': False, # < Adaptive cruise integration (visual displays)
        }
        
        
        
        config['RPMWarnings'] = {
            # TODO Allow these to be toggled individually too!
            'RPMwarn': (5000,[100,10000]),
            'RPMAlert': (6000,[100,10000]),
            'RPMAlarm': (7000,[100,10000]),
        }
        

        config['GearInfo'] = {
            'finalDrive': 1,
        }
        
        config['useCustomData'] = {
            # Req
            'speed': False,
            'rpm': False,
            # Rec
            'coolant': False,
            'eBrake': False,
            'fuel': False,
            'oilTemp': False,
            'checkEngine':False,
            'inGear': False,
            # Opt
            'selectedGear': False,
            'tireTemp': False,
            'tirePressure': False,
            'throttlePos':False,
            'throttlePosDesired':False,
            'brakePos': False,
            'clutchPos':False,
            'intakeTemp': False,
            'ambientTemp': False,
            'steeringPos': False,
            'AirCon':False,
            'CruiseControl':False
        }

        with open('dash_config.ini', 'w') as configfile:
            config.write(configfile)
        if os.path.isfile('dash_config.ini'):
            return True
        else:
            return False