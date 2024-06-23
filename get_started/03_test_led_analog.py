# This program was created in Arduino Lab for MicroPython
from machine import Pin, ADC, PWM
from time import sleep_ms

pot_pin = Pin("A0", Pin.IN)
blue_led_pin = Pin("A1", Pin.OUT)
green_led_pin = Pin("D12", Pin.OUT) #USE D12 for testing

pot = ADC(pot_pin)
pwm = PWM(blue_led_pin)
pwm_green = PWM(green_led_pin)
pwm.freq(1000)
pwm_green.freq(1000)

while True:
  pot_value = pot.read_u16()
  sleep_ms(10)
  if pot_value > 500:
    print(pot_value)
    pwm.duty_u16(pot_value)
    pwm_green.duty_u16(2^16 - pot_value)
  else:
    pwm.duty_u16(0)
    pwm_green.duty_u16(65000)


