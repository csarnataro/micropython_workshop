import network
import logging

from machine import Pin, PWM, ADC
from time import sleep_ms

from arduino_iot_cloud import ArduinoCloudClient
from arduino_iot_cloud import Task
from arduino_iot_cloud import async_wifi_connection

# WIFI_SSID and WIFI_PASS are loaded automatically by async_wifi_connection function
from secrets import WIFI_SSID
from secrets import WIFI_PASS
from secrets import DEVICE_ID
from secrets import CLOUD_PASSWORD

### PINS ###
# See https://docs.arduino.cc/micropython/basics/board-examples/#gpio-map for PIN numbers
ONBOARD_LED = 6  # GPIO6 => PIN 13
TEMPERATURE_SENSOR_LEVEL_PIN = "A0" # 26?
RED_LED_PIN = 46
GREEN_LED_PIN = 0
BLUE_LED_PIN = 45

TEMPERATURE_CHECK_DELAY_SECONDS = 2
DRY_LEVEL = 59000
WET_LEVEL = 20000
LED_ON = 0
LED_OFF = 1


builtin_led = Pin(ONBOARD_LED, Pin.OUT)
red_led = Pin(RED_LED_PIN, Pin.OUT)
green_led = Pin(GREEN_LED_PIN, Pin.OUT)
blue_led = Pin(BLUE_LED_PIN, Pin.OUT)
level_pin = Pin(TEMPERATURE_SENSOR_LEVEL_PIN, Pin.IN)
analog_level_pin = ADC(level_pin, atten=ADC.ATTN_11DB)

is_connected_to_wifi = False
is_connected_to_cloud = False

def red_led_on():
  red_led.value(LED_ON)
  blue_led.value(LED_OFF)
  green_led.value(LED_OFF)

def green_led_on():
  red_led.value(LED_OFF)
  blue_led.value(LED_OFF)
  green_led.value(LED_ON)

def blue_led_on():
  red_led.value(LED_OFF)
  blue_led.value(LED_ON)
  green_led.value(LED_OFF)

def all_leds_off():  
  red_led.value(LED_OFF)
  blue_led.value(LED_OFF)
  green_led.value(LED_OFF)

def wifi_connect():
    global is_connected_to_wifi
    if not WIFI_SSID or not WIFI_PASS:
        raise (Exception("Network is not configured. Set SSID and passwords in secrets.py"))
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        logging.info("Trying to connect. Note this may take a while...")
        sleep_ms(500)
    logging.info(f"WiFi Connected {wlan.ifconfig()}")
    builtin_led.value(0)
    blue_led_on()
    is_connected_to_wifi = True
  

def arduino_client_start():
    red_led_on()
    wifi_connect()
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=CLOUD_PASSWORD
    )
    # Register Cloud objects.
    # Note: The following objects must be created first in the dashboard and linked to the device.
    # This Cloud object is initialized with its last known value from the Cloud. When this object is updated
    # from the dashboard, the on_switch_changed function is called with the client object and the new value.

    client.register("pool_Temp", value=0.0)

    client.register(Task("loop", on_run=loop, interval=TEMPERATURE_CHECK_DELAY_SECONDS))
    client.register(Task("check_connection", on_run=check_connection, interval=1.0))

    # This function is registered as a background task to reconnect to WiFi if it ever gets
    # disconnected. Note, it can also be used for the initial WiFi connection, in synchronous
    # mode, if it's called without any args (i.e, async_wifi_connection()) at the beginning of
    # this script.
    # client.register(
    #     Task("wifi_connection", on_run=async_wifi_connection, interval=10.0)
    # )
    # Start the Arduino Cloud client.
    client.start()


# mimicing setup
def setup():
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s %(message)s",
        level=logging.DEBUG,
    )
    all_leds_off()
    builtin_led.value(1)
    logging.info("end of setup")

def check_connection(client): 
  global is_connected_to_cloud
  if not is_connected_to_cloud:
    thing_id = client.thing_id
    logging.info(f"******* CLIENT: {client.thing_id}")
    if thing_id is not None:
      logging.info(f"******* Thing ID: {thing_id}")
      green_led_on()
      is_connected_to_cloud = True

## TOTALLY NOT SURE ABOUT THESE CALCULATIONS
def convert_to_celsius(read_value):
    voltage = read_value / 2**10
    temperatureC = (voltage - 0.5) * 100
    return temperatureC


def loop(client):  
    # mimicing loop
    global is_connected_to_cloud
    logging.info(f"*** In loop, is connected? {is_connected_to_cloud}")
    if is_connected_to_cloud:
      read_value = analog_level_pin.read()
      temperature = convert_to_celsius(read_value)
      print("Temperature: ", temperature)
      client["pool_Temp"] = temperature
    

if __name__ == "__main__":
    setup()
    arduino_client_start()