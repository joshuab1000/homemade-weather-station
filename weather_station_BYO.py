from gpiozero import Button

import math
import time
import statistics

import bme280_sensor
import wind_direction_BYO
import ds18b20_therm
#import rainfall

RADIUS_CM = 9.0 # Radius of wind speed sensor
WIND_INTERVAL = 5 # Time gathering counts
INTERVAL = 300 # Time for recording wind gusts
CIRCUMFERENCE_CM = (2 * math.pi) * RADIUS_CM
ADJUSTMENT = 1.18 # Compensate for "anemometer factor"
CM_PER_S_TO_KM_PER_HOUR = .036
BUCKET = 0.2794 # Amount of water it takes to tip bucket in mm

temp_probe = ds18b20_therm.DS18B20()

store_speeds = []
store_directions = []

wind_count = 0
gust = 0

rain_count = 0

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
    speed = dist_cm / time_sec # Speed in cm/s
    speed = speed * CM_PER_S_TO_KM_PER_HOUR # Convert speed to km/h
    speed = speed * ADJUSTMENT
    return(speed)

def bucket_tipped():
    global rain_count
    rain_count
    rain_count += 1

def reset_rainfall():
    global rain_count
    rain_count = 0

wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin

rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped

while True:
    start_time = time.time()
    while time.time() - start_time <= INTERVAL:
        wind_start_time = time.time()
        reset_wind()
        while time.time() - wind_start_time <= WIND_INTERVAL:
            store_directions.append(wind_direction_BYO.get_value())
        final_speed = calculate_speed(WIND_INTERVAL) # Overall wind speed
        store_speeds.append(final_speed) # Add wind speed to list of wind speeds
    wind_average = wind_direction_BYO.get_average(store_directions)

    wind_gust = max(store_speeds) # Wind gust top speed
    wind_speed = statistics.mean(store_speeds) # Average wind speed

    rainfall = rain_count * BUCKET # Rainfall
    reset_rainfall()

    humidity, pressure, ambient_temp = bme280_sensor.read_all() # Humidity, Pressure, Air Temperature

    ground_temp = temp_probe.read_temp()
    print(ambient_temp, ground_temp, 0, pressure, humidity, wind_average, wind_speed, wind_gust, rainfall)

    store_speeds = []
    store_directions = []
