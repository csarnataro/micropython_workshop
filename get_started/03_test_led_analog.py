# This program was created in Arduino Lab for MicroPython
from machine import Pin, ADC, PWM
from time import sleep_ms

pot_pin = Pin("A0", Pin.OUT)
blue_led_pin = Pin("A1", Pin.OUT)

pot = ADC(pot_pin)
pwm = PWM(blue_led_pin)
pwm.freq(1000)

while True:
  pot_value = pot.read_u16()
  sleep_ms(10)
  if pot_value > 500:
    pwm.duty_u16(pot_value)
  else:
    pwm.duty_u16(0)


