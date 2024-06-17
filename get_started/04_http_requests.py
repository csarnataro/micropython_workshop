import network
import requests
from time import sleep

ssid = b'--ssid--'
key = b'--key--'
net_if = None
is_connected = False

def do_connect(ssid = ssid, key = key):
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

do_connect(ssid, key)

while True and is_connected:
  rq = requests.get('https://raw.githubusercontent.com/csarnataro/programmer_excuses_flutter/master/assets/translations/italian.txt')
  quotes = rq.content
  quote = quotes.splitlines()[random(70)]
  print(quote)
  sleep(20)  