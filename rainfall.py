from gpiozero import Button

BUCKET = 0.2794 # The amount of water (in mm) that has fallen for the bucket to tip once

rain_sensor = Button(6)
count = 0

def bucket_tipped():
    global count
    count += 1
    print(count * BUCKET)

def reset_rainfall():
    global count
    count = 0

while True:
    rain_sensor.when_pressed = bucket_tipped
