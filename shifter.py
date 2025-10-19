import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

serialPin, latchPin, clockPin = 23, 24, 25

class Shifter:
  def __init__(self, serialPin, latchPin, clockPin):
    self.serialPin = serialPin
    self.latchPin = latchPin
    self.clockPin = clockPin
    
    GPIO.setup(serialPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT, initial=0)
    GPIO.setup(clockPin, GPIO.OUT, initial=0)

  def __ping(self, p):
    GPIO.output(p, 1)
    time.sleep(0)
    GPIO.output(p, 0)

  def shiftByte(self, b):
    for i in range(8):
      GPIO.output(self.serialPin, b & (1 << i)) #sets the designated serial pin to either 0 or 1 (high/low, on/off for LED)
      self.__ping(self.clockPin)
    self.__ping(self.latchPin)

if __name__ == "__main__": #only run the following code when shifter.py is directly run (used to test code)
  shifter = Shifter(serialPin, latchPin, clockPin)
 
  try:
    while 1: 
      shifter.shiftByte(0b01010101)
  
  except KeyboardInterrupt:
    GPIO.cleanup()
