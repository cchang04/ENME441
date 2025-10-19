"""
Connor Chang
ENME441 - Lab 6
"""

import RPi.GPIO as GPIO
import time
import random
from shifter import Shifter #import Shifter class from shifter.py

GPIO.setmode(GPIO.BCM)
serialPin, latchPin, clockPin = 23, 24, 25

s1_pin = 17 #for on/off
s2_pin = 27 #to change wrap
s3_pin = 22 #change speed

initial_timestep = 0.1
fast_timestep = initial_timestep/3.0

#sets the s1-3 pins as pulldown resistors (off when not conencted)
GPIO.setup(s1_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(s2_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(s3_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

class Bug:
  def __init__(self, shifter, timestep = initial_timestep, x = 3, isWrapOn = False): #initialize attributes of bug class
    self.__shifter = shifter
    self.timestep = timestep
    self.x = x
    self.isWrapOn = isWrapOn
    self.min = 0
    self.max = 7

  def move(self):
    walk = random.choice([-1, 1]) #chooses randomly between -1 and 1
    new_x = self.x + walk #adds the walk number to the initial position

    if self.isWrapOn == True: #conditions for wrapping
      if new_x > self.max:
        self.x = self.min
      elif new_x < self.min:
        self.x = self.max
      else:
        self.x = new_x
    else: #condition for not wrapping (bug stops at edges)
      if self.min <= new_x <= self.max: #if the new position is within the boundaries, update the initial position otherwise the initial stays the same
        self.x = new_x

  def start(self):
    self.move() #initiates the bug movement
    ledPattern = 1 << self.x #creates a byte, shifting the binary number "1" left to the "x" index
    self.__shifter.shiftByte(ledPattern) #checks which index in the led byte is 1, turns the corresponding led on
    
  def stop(self):
    self.__shifter.shiftByte(0b00000000) #makes all led indexes 0 (turns off all leds)
 
shifter = Shifter(serialPin, latchPin, clockPin) #creates shifter object from Shifter class
bug = Bug(shifter, timestep = initial_timestep, x = 3, isWrapOn = False)
current_timestep = initial_timestep

try:
  while True:
    s1 = GPIO.input(s1_pin)
    s2 = GPIO.input(s2_pin)
    s3 = GPIO.input(s3_pin)

    if s2 == GPIO.HIGH: #if s2 pin is high, wraps, when false, does not wrap
      bug.isWrapOn = True #changes the isWrapOn attribute to true
    else:
      bug.isWrapOn = False

    if s3 == GPIO.HIGH:
      current_timestep = fast_timestep
    else:
      current_timestep = initial_timestep
    
    if s1 == GPIO.HIGH: #start when power is applied and stop when no power in s1 pin
      bug.start()
    else:
      bug.stop()

    time.sleep(current_timestep)

except KeyboardInterrupt:
  bug.stop()
  GPIO.cleanup()
