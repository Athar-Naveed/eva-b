from machine import Pin, SoftI2C
import ssd1306
import time

# Initialize I2C interface
i2c = SoftI2C(scl=Pin(14), sda=Pin(15))

# Initialize the OLED display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Clear the display
oled.fill(0)
oled.show()

# Main loop
while True:
    oled.fill(0)
    oled.text('Hi!', 0, 0)
    oled.text('ESP32 with OLED', 0, 10)
    
    oled.show()
    