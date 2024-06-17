# This program was created in Arduino Lab for MicroPython
from machine import Pin, ADC
from time import sleep_ms

pot_pin = Pin("A0", Pin.OUT) # ON RP2040 you can use "A0", otherwise refer to right GPIO number, e.g. 26
pot = ADC(pot_pin)

while True:
  pot_value = pot.read_u16()
  print(pot_value)
  sleep_ms(100)

# from REPL
# p = pot.read_u16()
# print(p)