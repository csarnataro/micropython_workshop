from machine import Pin, I2C
from time import sleep_ms, sleep
from lsm6dsox import LSM6DSOX  
import ssd1306

display = None
lsm = None

# mimicing setup
def setup():
    global display
    global lsm
    print("**** SETUP ****")
    i2c = I2C(id=0, sda=Pin(12), scl=Pin(13))
    lsm = LSM6DSOX(I2C(id=0, scl=Pin(13), sda=Pin(12)))
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.text('Ciao!', 0, 16, 2)
    display.show()

def loop():
  global lsm

  display.fill(0)
  # display.show()
  print("**** LOOP ****")
  display.text('Accelerometer:', 0, 0)
  display.text('x:{:>4.3f} y:{:>4.3f}'.format(*lsm.accel()), 0, 8, 2)
  display.text('z:{:>4.3f}'.format(*lsm.accel()), 0, 16, 2)
  display.text('Gyroscope:', 0, 32, 2)
  display.text('x:{:>4.3f} y:{:>4.3f}'.format(*lsm.gyro()), 0, 40, 2)
  display.text('z:{:>4.3f}'.format(*lsm.gyro()), 0, 48, 2)
  display.show()
  sleep(0.2)


if __name__ == "__main__":
    setup()
    while True:
      loop()
      sleep_ms(50)

