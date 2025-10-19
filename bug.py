import RPi.GPIO as GPIO
import time
import random
from shifter import Shifter

GPIO.setmode(GPIO.BCM)

serialPin, latchPin, clockPin = 23, 24, 25

GPIO.setup(serialPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial = 0)
GPIO.setup(clockPin, GPIO.OUT, initial = 0)

shifter = Shifter(serialPin, latchPin, clockPin)
initialPosition = random.randint(0, 7)
min = 0
max = 7

try:
  while True:
    step = [-1, 1]
    walk = random.choice(step)
    newPosition = initialPosition + walk

    if newPositon >= min && newPosition <= max: #if the new position is within the boundaries, update the initial position otherwise the initial stays the same
      initialPosition = newPosition

    ledPattern = 1 << initialPosition #creates a byte with binary number "1" at the initialPosition index
    shifter.shiftByte(ledPattern) #checks which index is 1 and turns on the corresponding index's LED

    time.sleep(0.05)

try:
 while 1: pass
except:
 GPIO.cleanup()
