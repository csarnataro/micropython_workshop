---
theme: default
layout: cover
background: /bg-cover.jpg
transition: slide-left
colorSchema: light

# theme: light-icons
# layout: center
# image: /bg-cover.jpg
---

# Arduino <img src="/arduino-friend.png" class="ml-24 my-4 h-16 rounded" > Micropython

Christian Sarnataro

WeMake Milan, Jun 22nd, 2024

---

# Why MicroPython

> ... aims to be as compatible with normal Python
> 
> ... it is compact enough to fit and run within just 256k of code space and 16k of RAM

It's supported on a lot of boards, and a handful of Arduino boards.

- Arduino Nano Rp2040 Connect
- Arduino Nano ESP32
- Arduino Giga
- Arduino Nano BLE (and BLE Sense)
- ...


See: 

https://micropython.org/download/

https://docs.arduino.cc/micropython/

---

# Required steps

1. Connect your compatible Arduino board to your machine

2. Install the Micropython firmware
    - It can be done manually from the Micropython download page
    - For Arduino boards, we can use https://labs.arduino.cc/en/labs/micropython-installer

3. Install an IDE
    - Arduino Lab for MicroPython https://labs.arduino.cc/en/labs/micropython

4. Have fun!

---

# Blinking a LED
<div/>
No need to upload a "sketch". It can be done interactively from the REPL (Read, Evaluate, Print Loop)


1. Open Arduino Lab for MicroPython
2. Connect the board using the `Connect` button <img class="h-8 inline" src="/connect-to-board.png"> 
3. Write to the REPL (i.e. the console window)

```python {all|1,2|4,5|all}
from machine import Pin
from time import sleep

led = Pin("D13", Pin.OUT) # "D13" is available on RP2040, for ESP32 use 48

while True:
  led.on() # OR led.value(1) OR led.toggle()
  sleep(1) # sleep uses seconds. sleep_ms() uses milliseconds instead
  led.off()
  sleep(1)
```

---

# A few more complex examples

---

# Install libraries 

---

# Arduino-like runtime 

---

# Connecting to Arduino Cloud


---
layout: 'end'
---

# This is a wrap

Thank you!