# Connor Chang
# ENME441 - Lab 5

# Problem 1
import RPi.GPIO as GPIO
import time
import math

t = time.time()
f = 0.2
B = (math.sin(2*math.pi*f*t))**2
p = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)

while True:
	GPIO.output(p, B)
