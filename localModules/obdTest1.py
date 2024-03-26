import obd
import time
from threading import Thread
from obd import OBDCommand

# Use to test OBD commands quickly

global responseDict,carConnected,queryDict
# Connect to OBD
car = obd.OBD("192.168.0.10", 35000)

    

queryList = ['PIDS_C','STATUS_DRIVE_CYCLE','BAROMETRIC_PRESSURE','RELATIVE_THROTTLE_POS','THROTTLE_POS_B','INTAKE_TEMP','EVAPORATIVE_PURGE','RUN_TIME','COMMANDED_EQUIV_RATIO','ELM_VOLTAGE','CONTROL_MODULE_VOLTAGE','ABSOLUTE_LOAD','INTAKE_PRESSURE','LONG_FUEL_TRIM_1','TIMING_ADVANCE','VIN','STATUS','MAF','FUEL_STATUS','SHORT_FUEL_TRIM_1']
# Create responses dictionary
responseDict = {}
while True:
    # get data
    print('==== START LOOP ====')  
    for command in queryList:
        # Format commands
        queryT = eval(f'obd.commands.{command}')
        
        # Run query (It got mad when I combined this with the line below, idk why)
        responseR = car.query(queryT)
        response = responseR.value
        try:
            responseDict[command] = response.magnitude
            print(f'(mag) {command}: {response.magnitude}')
        except:
            responseDict[command] = response
            print(f'(non) {command}: {response}')
    print('==== END LOOP ====')    
    time.sleep(1)
    

"""     support = {
OBDCommand('DTC_THROTTLE_POS', 'DTC Throttle Position', b'0211', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('PIDS_C', 'Supported PIDs [41-60]', b'0140', 6, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('DTC_DISTANCE_W_MIL', 'DTC Distance Traveled with MIL on', b'0221', 4, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('STATUS_DRIVE_CYCLE', 'Monitor status this drive cycle', b'0141', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('BAROMETRIC_PRESSURE', 'Barometric Pressure', b'0133', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('DTC_TIMING_ADVANCE', 'DTC Timing Advance', b'020E', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('DTC_ACCELERATOR_POS_D', 'DTC Accelerator pedal position D', b'0249', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('COOLANT_TEMP', 'Engine Coolant Temperature', b'0105', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('O2_S1_WR_CURRENT', '02 Sensor 1 WR Lambda Current', b'0134', 6, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('RELATIVE_THROTTLE_POS', 'Relative throttle position', b'0145', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('ELM_VERSION', 'ELM327 version string', b'ATI', 0, raw_string, ecu=1, fast=False), 
OBDCommand('THROTTLE_POS_B', 'Absolute throttle position B', b'0147', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('DTC_FUEL_STATUS', 'DTC Fuel System Status', b'0203', 4, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('THROTTLE_POS', 'Throttle Position', b'0111', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('GET_DTC', 'Get DTCs', b'03', 0, raw_string, ecu=ECU.ALL, fast=False), 


OBDCommand('CALIBRATION_ID', 'Calibration ID', b'0904', 18, raw_string, ecu=ECU.ALL, fast=True), 
OBDCommand('PIDS_9A', 'Supported PIDs [01-20]', b'0900', 7, raw_string, ecu=ECU.ALL, fast=True), 
OBDCommand('DTC_INTAKE_TEMP', 'DTC Intake Air Temp', b'020F', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('DTC_COMMANDED_EQUIV_RATIO', 'DTC Commanded equivalence ratio', b'0244', 4, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('EVAPORATIVE_PURGE', 'Commanded Evaporative Purge', b'012E', 3, raw_string, ecu=ECU.ENGINE, fast=True), 
OBDCommand('WARMUPS_SINCE_DTC_CLEAR', 'Number of warm-ups since codes cleared', b'0130', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('RUN_TIME', 'Engine Run Time', b'011F', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_A', 'Supported MIDs [01-20]', b'0600', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MONITOR_MISFIRE_CYLINDER_1', 'Misfire Cylinder 1 Data', b'06A2', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('COMMANDED_EQUIV_RATIO', 'Commanded equivalence ratio', b'0144', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('OBD_COMPLIANCE', 'OBD Standards Compliance', b'011C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_ACCELERATOR_POS_E', 'DTC Accelerator pedal position E', b'024A', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_CATALYST_B1', 'Catalyst Monitor Bank 1', b'0621', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('DTC_SPEED', 'DTC Vehicle Speed', b'020D', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_CATALYST_TEMP_B1S1', 'DTC Catalyst Temperature: Bank 1 - Sensor 1', b'023C', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('INTAKE_TEMP', 'Intake Air Temp', b'010F', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_ABSOLUTE_LOAD', 'DTC Absolute load value', b'0243', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_DISTANCE_SINCE_DTC_CLEAR', 'DTC Distance traveled since codes cleared', b'0231', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_MISFIRE_CYLINDER_4', 'Misfire Cylinder 4 Data', b'06A5', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('DTC_OBD_COMPLIANCE', 'DTC OBD Standards Compliance', b'021C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('PIDS_A', 'Supported PIDs [01-20]', b'0100', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('GET_CURRENT_DTC', 'Get DTCs from the current/last driving cycle', b'07', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('DTC_RUN_TIME', 'DTC Engine Run Time', b'021F', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('SPEED', 'Vehicle Speed', b'010D', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_O2_B1S2', 'DTC O2: Bank 1 - Sensor 2 Voltage', b'0215', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_BAROMETRIC_PRESSURE', 'DTC Barometric Pressure', b'0233', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_THROTTLE_ACTUATOR', 'DTC Commanded throttle actuator', b'024C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('ACCELERATOR_POS_E', 'Accelerator pedal position E', b'014A', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_SHORT_FUEL_TRIM_1', 'DTC Short Term Fuel Trim - Bank 1', b'0206', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_O2_SENSORS', 'DTC O2 Sensors Present', b'0213', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_THROTTLE_POS_B', 'DTC Absolute throttle position B', b'0247', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_COMMANDED_EGR', 'DTC Commanded EGR', b'022C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('O2_B1S2', 'O2: Bank 1 - Sensor 2 Voltage', b'0115', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_EVAPORATIVE_PURGE', 'DTC Commanded Evaporative Purge', b'022E', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_MISFIRE_CYLINDER_2', 'Misfire Cylinder 2 Data', b'06A3', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MONITOR_O2_B1S2', 'O2 Sensor Monitor Bank 1 - Sensor 2', b'0602', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('DTC_LONG_FUEL_TRIM_1', 'DTC Long Term Fuel Trim - Bank 1', b'0207', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_COOLANT_TEMP', 'DTC Engine Coolant Temperature', b'0205', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('CATALYST_TEMP_B1S1', 'Catalyst Temperature: Bank 1 - Sensor 1', b'013C', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('ACCELERATOR_POS_D', 'Accelerator pedal position D', b'0149', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_STATUS', 'DTC Status since DTCs cleared', b'0201', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_O2_S1_WR_CURRENT', 'DTC 02 Sensor 1 WR Lambda Current', b'0234', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_MAF', 'DTC Air Flow Rate (MAF)', b'0210', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('CONTROL_MODULE_VOLTAGE', 'Control module voltage', b'0142', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('ABSOLUTE_LOAD', 'Absolute load value', b'0143', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('THROTTLE_ACTUATOR', 'Commanded throttle actuator', b'014C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_D', 'Supported MIDs [61-80]', b'0660', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MIDS_C', 'Supported MIDs [41-60]', b'0640', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('ELM_VOLTAGE', 'Voltage detected by OBD-II adapter', b'ATRV', 0, raw_string, ecu=1, fast=False),
OBDCommand('MIDS_B', 'Supported MIDs [21-40]', b'0620', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('DISTANCE_W_MIL', 'Distance Traveled with MIL on', b'0121', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_PIDS_C', 'DTC Supported PIDs [41-60]', b'0240', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('INTAKE_PRESSURE', 'Intake Manifold Pressure', b'010B', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_INTAKE_PRESSURE', 'DTC Intake Manifold Pressure', b'020B', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_ENGINE_LOAD', 'DTC Calculated Engine Load', b'0204', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('LONG_FUEL_TRIM_1', 'Long Term Fuel Trim - Bank 1', b'0107', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('TIMING_ADVANCE', 'Timing Advance', b'010E', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_RELATIVE_THROTTLE_POS', 'DTC Relative throttle position', b'0245', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_STATUS_DRIVE_CYCLE', 'DTC Monitor status this drive cycle', b'0241', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_E', 'Supported MIDs [81-A0]', b'0680', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('VIN', 'Vehicle Identification Number', b'0902', 22, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('STATUS', 'Status since DTCs cleared', b'0101', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DISTANCE_SINCE_DTC_CLEAR', 'Distance traveled since codes cleared', b'0131', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('RPM', 'Engine RPM', b'010C', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_RPM', 'DTC Engine RPM', b'020C', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('CLEAR_DTC', 'Clear DTCs and Freeze data', b'04', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('MAF', 'Air Flow Rate (MAF)', b'0110', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_PIDS_B', 'DTC Supported PIDs [21-40]', b'0220', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('DTC_CONTROL_MODULE_VOLTAGE', 'DTC Control module voltage', b'0242', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('CVN', 'Calibration Verification Numbers', b'0906', 10, raw_string, ecu=ECU.ALL, fast=True),
OBDCommand('O2_SENSORS', 'O2 Sensors Present', b'0113', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_VVT_B1', 'VVT Monitor Bank 1', b'0635', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('ENGINE_LOAD', 'Calculated Engine Load', b'0104', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('FUEL_STATUS', 'Fuel System Status', b'0103', 4, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('COMMANDED_EGR', 'Commanded EGR', b'012C', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_O2_B1S1', 'O2 Sensor Monitor Bank 1 - Sensor 1', b'0601', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('SHORT_FUEL_TRIM_1', 'Short Term Fuel Trim - Bank 1', b'0106', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MONITOR_MISFIRE_CYLINDER_3', 'Misfire Cylinder 3 Data', b'06A4', 0, raw_string, ecu=ECU.ALL, fast=False),
OBDCommand('DTC_WARMUPS_SINCE_DTC_CLEAR', 'DTC Number of warm-ups since codes cleared', b'0230', 3, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('PIDS_B', 'Supported PIDs [21-40]', b'0120', 6, raw_string, ecu=ECU.ENGINE, fast=True),
OBDCommand('MIDS_F', 'Supported MIDs [A1-C0]', b'06A0', 0, raw_string, ecu=ECU.ALL, fast=False)} """