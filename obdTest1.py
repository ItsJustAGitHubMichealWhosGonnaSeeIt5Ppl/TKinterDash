import obd
import time
from threading import Thread
from obd import OBDCommand
from customPIDS.MX5NC2PIDs import *
from customPIDS.MX5NC2PIDs_Untested import *

# Use to test OBD commands quickly

global responseDict,carConnected,queryDict
# Connect to OBD
car = obd.OBD("192.168.0.10", 35000)

queryLists = ['MX5_TIRE_TEMP','MX5_CC_V','MX5_AC_REFRG_SW','MX5_AC_RELAY','MX_5_ACCL_PDL','MX5_BRKCLTCH_PRES_SW','MX5_TIRE_RPM']

queryList = ['MX5_WHL_ANG']
# Create responses dictionary
responseDict = {}
while True:
    # get data
    print('==== START LOOP ====')  
    for command in queryList:
        # Format commands
        car.supported_commands.add(eval(f'{command}'))
        queryT = eval(f'{command}')
        
        # Run query (It got mad when I combined this with the line below, idk why)
        responseR = car.query(queryT)
        response = responseR.value
        try:
            responseDict[command] = response.magnitude
            print(f'(mag) {command}: {response.magnitude}')
        except:
            responseDict[command] = response
            print(f'(non) {command}: {response}',)
    print('==== END LOOP ====')    
    time.sleep(1)
    

"""     support = {
OBDCommand('PIDS_C', 'Supported PIDs [41-60]', b'0140', 6, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('STATUS_DRIVE_CYCLE', 'Monitor status this drive cycle', b'0141', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('BAROMETRIC_PRESSURE', 'Barometric Pressure', b'0133', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('COOLANT_TEMP', 'Engine Coolant Temperature', b'0105', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('O2_S1_WR_CURRENT', '02 Sensor 1 WR Lambda Current', b'0134', 6, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('RELATIVE_THROTTLE_POS', 'Relative throttle position', b'0145', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('ELM_VERSION', 'ELM327 version string', b'ATI', 0, raw_string, ecu=1, fast=False), 
OBDCommand('THROTTLE_POS_B', 'Absolute throttle position B', b'0147', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('THROTTLE_POS', 'Throttle Position', b'0111', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('GET_DTC', 'Get DTCs', b'03', 0, raw_string, ecu=ECU.ALL, fast=False), 


OBDCommand('CALIBRATION_ID', 'Calibration ID', b'0904', 18, raw_string, ecu=ECU.ALL, fast=True), 
OBDCommand('PIDS_9A', 'Supported PIDs [01-20]', b'0900', 7, raw_string, ecu=ECU.ALL, fast=True), 
OBDCommand('EVAPORATIVE_PURGE', 'Commanded Evaporative Purge', b'012E', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('WARMUPS_SINCE_DTC_CLEAR', 'Number of warm-ups since codes cleared', b'0130', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('RUN_TIME', 'Engine Run Time', b'011F', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_A', 'Supported MIDs [01-20]', b'0600', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MONITOR_MISFIRE_CYLINDER_1', 'Misfire Cylinder 1 Data', b'06A2', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('COMMANDED_EQUIV_RATIO', 'Commanded equivalence ratio', b'0144', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('OBD_COMPLIANCE', 'OBD Standards Compliance', b'011C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_CATALYST_B1', 'Catalyst Monitor Bank 1', b'0621', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('INTAKE_TEMP', 'Intake Air Temp', b'010F', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_MISFIRE_CYLINDER_4', 'Misfire Cylinder 4 Data', b'06A5', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('PIDS_A', 'Supported PIDs [01-20]', b'0100', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('SPEED', 'Vehicle Speed', b'010D', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('ACCELERATOR_POS_E', 'Accelerator pedal position E', b'014A', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('O2_B1S2', 'O2: Bank 1 - Sensor 2 Voltage', b'0115', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_MISFIRE_CYLINDER_2', 'Misfire Cylinder 2 Data', b'06A3', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MONITOR_O2_B1S2', 'O2 Sensor Monitor Bank 1 - Sensor 2', b'0602', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('CATALYST_TEMP_B1S1', 'Catalyst Temperature: Bank 1 - Sensor 1', b'013C', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('ACCELERATOR_POS_D', 'Accelerator pedal position D', b'0149', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('CONTROL_MODULE_VOLTAGE', 'Control module voltage', b'0142', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('ABSOLUTE_LOAD', 'Absolute load value', b'0143', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('THROTTLE_ACTUATOR', 'Commanded throttle actuator', b'014C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_D', 'Supported MIDs [61-80]', b'0660', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MIDS_C', 'Supported MIDs [41-60]', b'0640', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('ELM_VOLTAGE', 'Voltage detected by OBD-II adapter', b'ATRV', 0, raw_string, ecu=1, fast=False),
OBDCommand('MIDS_B', 'Supported MIDs [21-40]', b'0620', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('DISTANCE_W_MIL', 'Distance Traveled with MIL on', b'0121', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('INTAKE_PRESSURE', 'Intake Manifold Pressure', b'010B', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('LONG_FUEL_TRIM_1', 'Long Term Fuel Trim - Bank 1', b'0107', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('TIMING_ADVANCE', 'Timing Advance', b'010E', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_E', 'Supported MIDs [81-A0]', b'0680', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('VIN', 'Vehicle Identification Number', b'0902', 22, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('STATUS', 'Status since DTCs cleared', b'0101', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DISTANCE_SINCE_DTC_CLEAR', 'Distance traveled since codes cleared', b'0131', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('RPM', 'Engine RPM', b'010C', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('CLEAR_DTC', 'Clear DTCs and Freeze data', b'04', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MAF', 'Air Flow Rate (MAF)', b'0110', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('CVN', 'Calibration Verification Numbers', b'0906', 10, raw_string, ecu=ECU.ALL, fast=True),
OBDCommand('O2_SENSORS', 'O2 Sensors Present', b'0113', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_VVT_B1', 'VVT Monitor Bank 1', b'0635', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('ENGINE_LOAD', 'Calculated Engine Load', b'0104', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('FUEL_STATUS', 'Fuel System Status', b'0103', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('COMMANDED_EGR', 'Commanded EGR', b'012C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_O2_B1S1', 'O2 Sensor Monitor Bank 1 - Sensor 1', b'0601', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('SHORT_FUEL_TRIM_1', 'Short Term Fuel Trim - Bank 1', b'0106', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_MISFIRE_CYLINDER_3', 'Misfire Cylinder 3 Data', b'06A4', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('PIDS_B', 'Supported PIDs [21-40]', b'0120', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_F', 'Supported MIDs [A1-C0]', b'06A0', 0, raw_string, ecu=ECU.ALL, fast=False)} """