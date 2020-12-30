#!/usr/bin/python3

from sense_hat import SenseHat
import datetime
import time
import datetime
import math
import csv
import requests

def compass_to_rgb(h, s=1, v=1):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def sensor_message():
    # Take readings from all three sensors
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()

    # Round the values to one decimal place
    t = round(t, 1)
    p = round(p, 1)
    h = round(h, 1)

    # Create the message
    message = "Temperature: " + str(t) + " Pressure: " + str(p) + " Humidity: " + str(h)
    return message
  
  def rainbow():
    R =  [255, 0, 0] # red
    O =  [255,127,0] # orange
    Y =  [255,255,0] # yellow
    GY = [127,255,0] # green-yellow
    G =  [0, 255, 0] # green
    GC = [0,255,127] # green-cyan
    C  = [0,255,255] # cyan
    BC = [0,127,255] # blue-cyan
    B =  [0, 0, 255] # blue
    BM = [127,0,255] # blue-magenta
    M =  [255,0,255] # magenta
    RM = [255,0,127] # red-magenta

    pixel_list = [
    R,  R,  O,  Y,  GY, G,  GC, C,
    R,  O,  Y,  GY, G,  GC, C,  BC,
    O,  Y,  GY, G,  GC, C,  BC, B,
    Y,  GY, G,  GC, C,  BC, B,  BM,
    GY, G,  GC, C,  BC, B,  BM, M,
    G,  GC, C,  BC, B,  BM, M,  RM,
    GC, C,  BC, B,  BM, M,  RM, R,
    C,  BC, B,  BM, M,  RM, R,  R
    ]                                                                                                                                                                                                                  return pixel_list

sense = SenseHat()
sense.set_rotation(180)
sense.low_light = True
t = str(round(sense.get_temperature(),2))
p = str(round(sense.get_pressure(),2))
h = str(round(sense.get_humidity(),2))

# grab attention by showing the rainbow for a couple of seconds
sense.set_pixels(rainbow())
time.sleep(2.5)

# first message is the Time
now = datetime.datetime.now()
message = now.strftime("%H:%M")

# the background color is a gradient of the rainbow
background = compass_to_rgb(now.minute*6)
sense.show_message(message, back_colour=background, scroll_speed=0.08)
time.sleep(1)

# second message is the sensor readings                                                                                                                                                                            sense.show_message(sensor_message(), scroll_speed=0.08)

# conclude the program with the LED array cleared
sense.clear( (0,0,0))

# The requests are sent to dweet.io and freeboard using the following code and saved to the csv file also. 
while True:
    r = requests.post('https://dweet.io/dweet/for/weather_script?'+'Temperature=' + t + '&Humidity=' + h + '&Pressure=' + p )
    currentTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open('weatherLog.csv', 'a') as file:
        file.write(str("Temperature: "+ " " + t + " " + "Humidity: " + " " +  h + " " + "Pressure: " + " " + p + " " + "Time:" + " " +  currentTime + " \n"))
    time.sleep (3)
