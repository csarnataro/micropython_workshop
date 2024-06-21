# This program was created in Arduino Lab for MicroPython
from machine import Pin, ADC
from time import sleep

TEMPERATURE_SENSOR_LEVEL_PIN = "A0"

def tmp36_temperature_C(read_value):
    print("Raw value: ", read_value)
    # // converting that reading to voltage, for 3.3v arduino use 3.3
    # voltage = read_value #  * 3.3
    voltage = read_value / 2**10 # 1024.0
    temperatureC = (voltage - 0.5) * 100
    
    print("Temperature: ", temperatureC)
  
    # millivolts = read_value * (3.3 * 1000 / 65535)
    # return (millivolts - 500) / 10
    return temperatureC
  
if __name__ == "__main__":
  level_pin = Pin(TEMPERATURE_SENSOR_LEVEL_PIN, Pin.IN)
  analog_level_pin = ADC(level_pin, atten=ADC.ATTN_11DB)

  while True:
    read_value = analog_level_pin.read()
    temperature = tmp36_temperature_C(read_value)
    print("**** Final temperature: ", temperature)
    sleep(2)
