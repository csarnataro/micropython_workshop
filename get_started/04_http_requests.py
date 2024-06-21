import network
import requests
import ssd1306
from machine import I2C
from time import sleep, sleep_ms

from secrets import WIFI_SSID
from secrets import WIFI_PASS
net_if = None
is_connected = False
display = None

def do_connect(ssid = WIFI_SSID, key = WIFI_PASS):
    import network
    global is_connected
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, key)
        while not sta_if.isconnected():
            pass
    is_connected = True
    print('network config:', sta_if.ifconfig())

# Main starts here
i2c = I2C(id=0, sda=Pin(12), scl=Pin(13))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.text('Connecting...', 0, 16, 2)
display.show()

do_connect(WIFI_SSID, WIFI_PASS)

while True and is_connected:
  rq = requests.get('https://raw.githubusercontent.com/csarnataro/micropython_workshop/main/quotes.txt')
  quotes = rq.content
  quote = quotes.splitlines()[random(70)].decode("latin-1")
  print(quote)
  display.fill(0)
  quote = '{:<12} {}'.format(24* " ", quote)
  for x in range(len(quote) + 1):
    display.fill(0)
    display.text(quote[x:24+x], 0, 16)
    sleep_ms(100)
    display.show()
