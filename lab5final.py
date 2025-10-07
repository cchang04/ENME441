# Connor Chang
# ENME441 - Lab 5

import RPi.GPIO as GPIO
import time
import math

p = [17, 27, 22, 10, 9, 11, 5, 6, 13, 19]

GPIO.setmode(GPIO.BCM)

pwm_array = []

for pin in p:
	GPIO.setup(p, GPIO.OUT)
	pwm = GPIO.PWM(pin, 500)
	pwm.start(0)
	pwm_array.append(pwm)

try:
	while True:
		for (i, value) in enumerate(pwm_array):
			phi = math.pi/11
			updated_phi = i*phi
			f = 0.2
			t = time.time()
			B = (math.sin((2*math.pi*f*t) - updated_phi))**2
			dc = B*100
			pwm_array.ChangeDutyCycle(dc)

except KeyboardInterrupt:
	print('\nExiting')

pwm.stop()
GPIO.cleanup()
