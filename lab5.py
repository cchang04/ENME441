# Connor Chang
# ENME441 - Lab 5

# Problem 1
import RPi.GPIO as GPIO
import time
import math

t = time.time()
f = 0.2
B = (math.sin(2*math.pi*f*t))**2

GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)
p = 17

while True:
	GPIO.output(p, B)
