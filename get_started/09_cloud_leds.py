import network
import logging

from machine import Pin, PWM, ADC
from time import sleep_ms

from arduino_iot_cloud import ArduinoCloudClient, Color, Task

# WIFI_SSID and WIFI_PASS are loaded automatically by async_wifi_connection function
from secrets import WIFI_SSID, WIFI_PASS, DEVICE_ID, CLOUD_PASSWORD

POTENTIOMETER_DELAY_SECONDS = 0.5

builtin_led = Pin("D13", Pin.OUT)
green_led = Pin("D12", Pin.OUT)
pot_pin = Pin("A0", Pin.OUT) # ON RP2040 you can use "A0", otherwise refer to right GPIO number, e.g. 26
pot = ADC(pot_pin)

is_connected_to_wifi = False
is_connected_to_cloud = False

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
        builtin_led.toggle()
    logging.info(f"WiFi Connected {wlan.ifconfig()}")
    is_connected_to_wifi = True
    builtin_led.off()
  

def arduino_client_start():
    wifi_connect()
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=CLOUD_PASSWORD
    )
    client.register("led", value=False, on_write=on_led_changed)
    client.register(Color("blue_led", value={'bri': 50, 'sat': 50, 'hue': 50}))
    client.register(Task("loop", on_run=loop, interval=POTENTIOMETER_DELAY_SECONDS))
    client.register(Task("check_connection", on_run=check_connection, interval=1.0))

    client.start()


def on_led_changed(client, value):
    green_led.value(value)
  

# mimicing setup
def setup():
    builtin_led.on()
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s %(message)s",
        level=logging.DEBUG,
    )
    logging.info("end of setup")

def check_connection(client): 
  global is_connected_to_cloud
  if not is_connected_to_cloud:
    thing_id = client.thing_id
    logging.info(f"******* CLIENT: {client.thing_id}")
    if thing_id is not None:
      logging.info(f"******* Thing ID: {thing_id}")
      is_connected_to_cloud = True

def loop(client):  
    # mimicing loop
    global is_connected_to_cloud
    logging.info(f"*** In loop, is connected? {is_connected_to_cloud}")
    if is_connected_to_cloud:
      pot_value = pot.read_u16()
      client["blue_led"].bri = pot_value / 65000 * 100
      client["blue_led"].hue = 207
      client["blue_led"].sat = 90
      print("Potentiometer Value: ", pot_value)

if __name__ == "__main__":
    setup()
    arduino_client_start()
