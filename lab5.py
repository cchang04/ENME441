# Connor Chang
# ENME441 - Lab 5

# Problem 1
import RPi.GPIO as GPIO
import time
import math


f = 0.2
t = time.time()
B = (math.sin(2*math.pi*f*t))**2
p = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)

pwm = GPIO.PWM(p, 500)

try:
	pwm.start(0)
	while True:
		pwm.ChangeDutyCycle(B)

except KeyboardInterrupt:
	print('\nExiting')

pwm.stop()
GPIO.cleanup()
