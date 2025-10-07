# Connor Chang
# ENME441 - Lab 5

import RPi.GPIO as GPIO
import time
import math

p = [17, 27, 22, 10, 9, 11, 5, 6, 13, 19] #GPIO pin numbers

GPIO.setmode(GPIO.BCM) #Set up GPIO pin numbers to match BCM numbers
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pwm_array = [] #Create array for pwm outputs

for pin in p: #For every pin number assign to "pin" each loop
	GPIO.setup(p, GPIO.OUT) #Set pin number to output pin
	pwm = GPIO.PWM(pin, 500) #Create pwm object at 500Hz
	pwm.start(0) #Start duty cycle at 0
	pwm_array.append(pwm) #Add each pwm code into the array

def myCallback():
	phi = -1*(math.pi/11)

try:
	GPIO.add_event_detect(26, GPIO.RISING, callback=myCallback(), bouncetime=100)

	while True:
		for (i, value) in enumerate(pwm_array): #Assigns the index of the array to "i" and the value of the array to "value"
			phi = math.pi/11
			updated_phi = i*phi #Increases phi value based on index/pin number
			f = 0.2
			t = time.time()
			B = (math.sin((2*math.pi*f*t) - updated_phi))**2
			dc = B*100
			value.ChangeDutyCycle(dc)

except KeyboardInterrupt:
	print('\nExiting')

pwm.stop()
GPIO.cleanup()
