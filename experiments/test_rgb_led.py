# This program was created in Arduino Lab for MicroPython

from time import sleep

from machine import Pin, ADC

RED_LED_PIN = 46
GREEN_LED_PIN = 0
BLUE_LED_PIN = 45

red_led_pin = Pin(RED_LED_PIN, Pin.OUT)
green_led_pin = Pin(GREEN_LED_PIN, Pin.OUT)
blue_led_pin = Pin(BLUE_LED_PIN, Pin.OUT)

LED_ON = 0
LED_OFF = 1

red_led_pin.value(LED_OFF)
green_led_pin.value(LED_OFF)
blue_led_pin.value(LED_OFF)


while True:
  red_led_pin.value(LED_ON)
  green_led_pin.value(LED_OFF)
  blue_led_pin.value(LED_OFF)
  sleep(1)
  red_led_pin.value(LED_OFF)
  green_led_pin.value(LED_OFF)
  blue_led_pin.value(LED_ON)
  sleep(1)
  red_led_pin.value(LED_OFF)
  green_led_pin.value(LED_ON)
  blue_led_pin.value(LED_OFF)
  sleep(1)


