"""
Connor Chang
ENME441 - Lab 6
"""

import RPi.GPIO as GPIO
import time
import random
from shifter import Shifter

GPIO.setmode(GPIO.BCM)
serialPin, clockPin, latchPin = 23, 25, 24

class Bug:
  def __init__(self, shifter, timestep = 0.1, x = 3, isWrapOn = False):
    self.__shifter = shifter
    self.timestep = timestep
    self.x = x
    self.isWrapOn = isWrapOn
    self.min = 0
    self.max = 7

  def move(self):
    walk = random.choice([-1, 1]) #chooses randomly between -1 and 1
    new_x = self.x + walk

    if self.isWrapOn == True #conditions for wrapping
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
    try:
      while True:
        self.move() #initiates the bug movement
        ledPattern = 1 << self.x #creates a byte, shifting the binary number "1" left to the "x" index
        self.__shifter.shiftByte(ledPattern) #checks which index in the led byte is 1, turns the corresponding led on
        time.sleep(self.timestep)
    except KeyboardInterrupt: # when keyboard interrupt detected, initiate stop
      self.stop()

  def stop(self):
    self.__shifter.shiftByte(0b00000000) #makes all led indexes 0 (turns off all leds)
    GPIO.cleanup()
 
shifter = Shifter(serialPin, latchPin, clockPin)
trapBug = Bug(shifter)
wrapBug = Bug(shifter, timestep = 0.05, isWrapOn = True)

try:
  trapBug.start()
  #wrapBug.start()
    
