from time import ticks_ms, sleep_ms

from machine import Pin, ADC

HUMIDITY_SENSOR_DELAY = 1 * 1000

# see https://docs.arduino.cc/tutorials/nano-esp32/pin-setup/#nano-esp32-pin-map

HUMIDITY_SENSOR_POWER = "D3"
HUMIDITY_SENSOR_LEVEL_PIN = "A1"
RED_LED_PIN = 46
GREEN_LED_PIN = 0
BLUE_LED_PIN = 45


DRY_LEVEL = 59000
WET_LEVEL = 20000

power_pin = Pin(HUMIDITY_SENSOR_POWER, Pin.OUT)
level_pin = Pin(HUMIDITY_SENSOR_LEVEL_PIN, Pin.IN)
red_led_pin = Pin(RED_LED_PIN, Pin.OUT)

analog_level_pin = ADC(level_pin, atten=ADC.ATTN_11DB)

power_pin.on()
sleep_ms(100)

measurement_time = 0

def map (x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def convert_to_percent(value):
  perc = map(value, DRY_LEVEL, WET_LEVEL, 0, 100)
  if perc > 100:
    perc = 100
  if perc < 0:
    perc = 0
  return perc;

while True:
  now = ticks_ms()
  if now - measurement_time > HUMIDITY_SENSOR_DELAY:
    power_pin.on() # corresponds to HIGH. turns the sensor on
    sleep_ms(10)  # allow power to settle
    read_value = analog_level_pin.read_u16()
    # volt = analog_level_pin.read_uv() / 1000000
    humidity = convert_to_percent(read_value)
    power_pin.off()
    # print("Analog Value: ", read_value)
    # print("VOLT: ", volt)
    print("Humidity: ", humidity)
    measurement_time = now


