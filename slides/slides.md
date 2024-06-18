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

# What is MicroPython

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
        
      (works with any board)

4. Write your code

5. Have fun!

---

# Blinking a LED
<div/>
No need to upload a "sketch". It can be done interactively from the REPL (Read, Evaluate, Print Loop)


1. Open Arduino Lab for MicroPython
2. Connect the board using the `Connect` button <img class="h-8 inline" src="/connect-to-board.png"> 
3. Write to the REPL (i.e. the console window)

```python {1,2|4,5|6-10|all}
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

# Useful hints when using the Micropython IDE

1. The board has a file system from which it will read the files to be executed, namely `boot.py` and `main.py`.

    Anyway, while developing, **there's no need to save any files on the board**, everything will executed directly on the board, reading the source code from the host machine file system

2. The "Soft reset" button will erase `imports` and `variables` and will start executing the main file from scratch

3. Libraries can be imported directly from the REPL on WiFi capable boards, using the following command

    ```python
    import mip
    mip.install('<library name>')
    ```

---

# How to install libraries (1)
- Libraries can be installed from the host machine using `mpremote`, which in turn requires `pip`, the python package manger.

  ```shellscript
  $ pip install mpremote
  $ mpremote mip install <your library >
  ```
  Or, if you have multiple boards installed:

  ```sh
  $ mpremote connect list
  $ mpremote connect id:<board_id > mip install <your library >
  ```


- In addition, from WiFi capable boards, they can be installed directly from the REPL using the following command

  ```python
  import mip
  mip.install('<library name>')
  ```


---

# How to install libraries (2)

- Most libraries are available on micropython.org, meaning that you can install them **just by  name**:

  ```python
  mip.install('ssd1306')
  ```

- Contributed libraries are available elsewhere (e.g. on github) and can be installed using this format: 

  ```python
  mip.install('github:jposada202020/MicroPython_LSM6DSOX')
  ```

- Installed libraries are installed in the `/lib` folder on the board
  
---

# A more interesting example (1)
```python {1|2|6-9|all}
mip.install('ssd1306')
mip.install('github:jposada202020/MicroPython_LSM6DSOX')

# ...

from machine import Pin, I2C
from time import sleep_ms, sleep
from lsm6dsox import LSM6DSOX  
import ssd1306

display = None
lsm = None

if __name__ == "__main__":
    setup()
    while True:
      loop()

```

---

# A more complex example (2)

```python

# mimicing setup
def setup():
    global display
    global lsm
    i2c = I2C(id=0, sda=Pin(12), scl=Pin(13))
    lsm = LSM6DSOX(I2C(id=0, scl=Pin(13), sda=Pin(12)))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)

# mimicing loop
def loop():
  global lsm
  display.fill(0)
  display.text('Accelerometer:', 0, 0)
  display.text('x:{:>4.3f} y:{:>4.3f}'.format(*lsm.accel()), 0, 8, 2)
  display.text('z:{:>4.3f}'.format(*lsm.accel()), 0, 16, 2)
  display.show()
  sleep(0.2)


```
---

# Arduino-like runtime 
<div />
A module to simplify and help writing MicroPython programs using the setup()/loop() paradigm.

This module also wraps common constants and machine functions in easy-to-use methods. 

  - `setup`, `loop`, `HIGH`, `LOW`, `INPUT`, `OUTPUT`
  - `pinMode`, `digitalRead`, `digitalWrite`, `delay`, `map`
  - ... and more, check https://github.com/arduino/arduino-runtime-mpy

```python
from arduino import *

def setup():
  print('starting my program')

def loop():
  print('loop')
  delay(1000)

def cleanup():
  print('cleanup')

start(setup, loop, cleanup)
```
---

# Connecting to Arduino Cloud

---

# Conclusion

- Super fast development cycle
- Ideal for education, very early prototyping
- Ideal for Python developers
- A lot of available libraries
- Since it's an interpreted language, there's no need to compile and store your binaries before executing it on the board => Fast development directly from the host machine
- Programs should work like the regular C++ (no known issues)
- <img src="/warning.png" class="mr-2 h-4 inline" />Probably not ideal for time-sensitive tasks

---
layout: 'end'
---

# This is a wrap

Thank you!