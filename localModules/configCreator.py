import configparser
import os
"""Config - Will be changeable in the dash as needed"""
configVer = '0.0.22'
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
            'redline': (7700,[100,10000]),
            'coolantMaxC': (130,[60,220]), # Maximum coolant temp in Celcius
            'gears': (6, [1,20]),
            'speed':('MPH',['MPH','KPH']),
            'distance':('Miles', ['Miles','Kilometers']),
            'temperature': ('F', ['F','C']),
        }
        
        # Basic settings that don't have another home
        config['Preferences'] = {
            'dynamicRedline': False, # Lower redline when car is warming up
            'speedWarning': False,
            'speedWarningVal': 150,
            'RPMWarnings': False,
        } 

        config['Integrations'] = {
            'OpenDsh': False, # OpenDash
            'ACC': False, # < Adaptive cruise integration (visual displays)
        }
        
        
        
        config['RPMWarnings'] = {
            # TODO Allow these to be toggled individually too!
            'RPMwarn': 5000,
            'RPMAlert': 6000,
            'RPMAlarm': 7000,
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