# TKinterDash
Minimalist dash/gauge display) that displays data from your OBD reader (right now using Python-OBD, plan to tweak for external data later)

Currently only setup to display on an RPi 7" display, this will be changed too!

Still extremely WIP!!!

# Features (WIP)
- WIP configuration app/panel for tweaking all settings
- 6 "sections", will allow tweaking these later.
- RPM bar with 3 configurable zones (Warn, alert, and alarm)
- Coolant temp bar and value readout (currently only in C, will add F)
- Throttle position display
- Speed display that can be swapped between MPH and KPH
- Gear display (calculated from ratios, needs tweaking to work with other cars)
- Shift suggestions (I called it SmartShift, its extremely annoying, ill make it optional)
- Connection status (bottom left)
- ProShift:  Shows all gears and what their current RPM would be, allows for easy revmatching + helps pick the right gear (needs work)

# Sections

## Outside
- RPM Bar across the top
- Coolant temp up the right side (closest to driver in RHD car, will add LHD mode)

## Top left
- Unused
  
## Top centre
- Speed in MPH or KPH
  
## Top right
- Throttle position bar
[NOT YET IMPLEMENTED]
- Brake position bar
- clutch position bar
- steering position bar
- Car voltage(?)
  
## Bottom left
- Connection status

## Bottom centre
- Current gear
- SmartShift gear suggestion (will allow this to be disabled)
![image](https://github.com/ItsJustAGitHubMichealWhosGonnaSeeIt5Ppl/TKinterDash/assets/85679034/291460a9-9d7c-489e-b04b-d572af2f4805)

## Bottom right
- ProShift gear and RPM information (will allow this to be disabled)

# Example screenshot (does not contain all features)

![image](https://github.com/ItsJustAGitHubMichealWhosGonnaSeeIt5Ppl/TKinterDash/assets/85679034/131a7065-632e-4775-9b8b-2ca400bceeb6)

