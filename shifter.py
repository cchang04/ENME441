import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

serialPin, latchPin, clockPin = 23, 24, 25

class Shifter:
  def __init__(self, serialPin, clockPin, latchPin):
    self.serialPin = serialPin
    self.clockPin = clockPin
    self.latchPin = latchPin
    
    GPIO.setup(serialPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT, initial=0)
    GPIO.setup(clockPin, GPIO.OUT, initial=0)

  def __ping(self, p):
    GPIO.output(p, 1)
    time.sleep(0)
    GPIO.output(p, 0)

  def shiftByte(self, b):
    for i in range(8):
      bit_value = 1 if (b & (1<<i)) else 0
      """
      the (1<<i) shifts the binary number "1" by i values to the left to create a byte with a singular 1 at the ith position
      b is equal to the byte we are looking at (ex. in class was 01100110)
      if the ith bit in b is 1 AND the left shifted bit is also 1, bit_value returns a 1
      if the ith bit in b is a 0, then we have a 0 and a 1 which results in a 0
      """
      GPIO.output(self.serialPin, b & (1 << i)) #sets the designated serial pin to either 0 or 1 (high/low, on/off for LED)
      self.__ping(self.clockPin)
    self.__ping(self.latchPin)

if __name__ == "__main__":
  shifter = Shifter(serialPin, latchPin, clockPin)
 
  try:
    while 1: 
      shifter.shiftByte(0b11111111)
  
  except KeyboardInterrupt:
    GPIO.cleanup()
