# Connor Chang
# ENME441 - Lab 5

# Problem 1
import RPi.GPIO as GPIO
import time
import math



p = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(p, GPIO.OUT)

pwm = GPIO.PWM(p, 500)

pwm.start(0)

try:
	while True:
		f = 0.2
		t = time.time()
		B = (math.sin(2*math.pi*f*t))**2
		dc = B*100

		pwm.ChangeDutyCycle(dc)

except KeyboardInterrupt:
	print('\nExiting')

pwm.stop()
GPIO.cleanup()
