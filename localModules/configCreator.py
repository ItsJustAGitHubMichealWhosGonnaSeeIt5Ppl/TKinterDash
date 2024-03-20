import configparser
import os
"""Config - Will be changeable in the dash as needed"""

# TODO make use of config settings
# TODO Add user interface to change all this
def configCheck(ForceRecreate=False):
    
    config = configparser.ConfigParser()

    # Check if config already exists, read it if it does.
    if os.path.isfile('dash_config.ini') and ForceRecreate == False: 
        return True
    else:
        # Allow for prompting if something has updated
        config['Versions'] = {
            'HUDVer': '?',
            'ConfigVer': '0.0.21',
            'PythonOBDVer': '?'
        }
        
        # Needed to work at all
        config['Required'] = {
            'redline': 7700,
            'coolantMaxC': 130, # Maximum coolant temp in Celcius
            'gears': 6,
            'speedUnits': 'MPH' # Alt would be KPH
        }
        
        # Available sensors/datapoints Yes(True), partial, No(False)
        # TODO find a way to change polling rate or log polling rate
        config['AvailableData'] = {
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
        

        # Basic settings that don't have another home
        config['Basic'] = {
            'dynamicRedline': False # Lower redline when car is warming up
            
        } 
            


        config['RPM'] = {
            # TODO Allow these to be toggled individually too!
            'enableRPMWarnings': False, # Disabled by default
            'RPMwarn': 5000,
            'RPMAlert': 6000,
            'RPMAlarm': 7000,
        }


        config['speed'] = {
            'speedWarningEnabled': False, # < Disabled by default but these should all be in a config file that it creates on first one
            'speedWarningVal': 150,
        }
        
        config['Integrations'] = {
            'OpenDsh': False, # OpenDash
            'ACC': False, # < Adaptive cruise integration (visual displays)
        }

        with open('dash_config.ini', 'w') as configfile:
            config.write(configfile)
        if os.path.isfile('dash_config.ini'):
            return True
        else:
            return False