# Connor Chang
# ENME441 - Lab 5

# Problem 1
import RPi.GPIO as GPIO
import time
import math

p = [17, 27]

GPIO.setmode(GPIO.BCM)

for i in range(2):
	GPIO.setup(p, GPIO.OUT)

pwm1 = GPIO.PWM(p[0], 500)
pwm2 = GPIO.PWM(p[1], 500)

pwm1.start(0)
pwm2.start(0)

try:
	while True:
		f = 0.2
		t = time.time()
		B1 = (math.sin(2*math.pi*f*t))**2
		phi = math.pi/11
		B2 = (math.sin((2*math.pi*f*t) - phi))**2
		dc1 = B*100
		dc2 = B2*100

		pwm1.ChangeDutyCycle(dc1)
		pwm2.ChangeDutyCycle(dc2)

except KeyboardInterrupt:
	print('\nExiting')

pwm.stop()
GPIO.cleanup()
