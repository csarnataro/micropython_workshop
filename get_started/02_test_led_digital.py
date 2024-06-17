# This program was created in Arduino Lab for MicroPython
from machine import Pin
from time import sleep

led = Pin("D12", Pin.OUT)

while True:
  led.on() # OR led.value(1)
  sleep(1)
  led.off()
  sleep(1)
