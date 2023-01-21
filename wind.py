from gpiozero import Button

import math
import time

RADIUS_CM = 9.0 # Radius of wind speed sensor
WIND_INTERVAL = 5 # Time gathering counts
CIRCUMFERENCE_CM = (2 * math.pi) * RADIUS_CM
ADJUSTMENT = 1.18 # Compensate for "anemometer factor"
CM_PER_S_TO_KM_PER_HOUR = .036

def spin():
    global wind_count
    wind_count = wind_count + 1

def reset_wind():
    global wind_count
    wind_count = 0

# Calculate speed in km/h
def calculate_speed(time_sec):
    global wind_count

    rotations = wind_count / 2.0
    dist_cm = CIRCUMFERENCE_CM * rotations
    speed = dist_cm / time_sec #Speed in cm/s
    speed = speed * CM_PER_S_TO_KM_PER_HOUR #Convert speed to km/h
    speed = speed * ADJUSTMENT
    return(speed)

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin

while True:
    wind_count = 0
    time.sleep(WIND_INTERVAL)
    print((calculate_speed(WIND_INTERVAL)), "km/h")
