import obd
import time


# Use to test OBD commands quickly
car = obd.OBD("192.168.0.10", 35000)

speed = obd.commands.SPEED
rpm = obd.commands.RPM

rpmNow = car.query(rpm)
while True:
    rpmNow = car.query(rpm)
    print(rpmNow.value)
    time.sleep(.5)