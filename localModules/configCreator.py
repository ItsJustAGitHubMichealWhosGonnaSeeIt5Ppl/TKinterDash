import configparser
import os
"""Config - Will be changeable in the dash as needed"""


# TODO Add user interface to change all this
def configCheck(ForceRecreate=False):
    
    config = configparser.ConfigParser()

    # Check if config already exists, read it if it does.
    if os.path.isfile('dash_config.ini') and ForceRecreate == False: 
        return True
    else:
        # Needed to work at all
        config['Required'] = {
            'redline': 7700, 
            'gears': 6,
            'units': 'USA'
        }
        # Basic settings that don't have another home
        config['Basic'] = {
            'ACCIntegration': False, # < Adaptive cruise integration (visual displays)
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

        with open('dash_config.ini', 'w') as configfile:
            config.write(configfile)
        if os.path.isfile('dash_config.ini'):
            return True
        else:
            return False