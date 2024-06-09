# ------------------
# Imports
# ------------------
import time

# ------------------
# Actual code starts here
# ------------------

class ESP32MainCode:
    def __init__(self)->None:
        pass
    def blink_code(self)->None:
        """
        blink led code: blinks a "white led" if pin is '4', if pin is "33", a red led will blink

        params:
        no receiving params

        return:
        this function returns None

        """
        from machine import Pin
        # ------------------
        # Setting pin for led
        # ------------------
        
        led = Pin(4, Pin.OUT)
        
        # ------------------
        # ------------------
        while True:
            led.value(1)
            time.sleep(1)
            
            led.value(0)
            time.sleep(1)

    def display_code(self,user_input:str)->str:
        """
        display code: this code will display output text on the oled display 

        params:
        user_input: str - the text to be send to the AIML (currently) and MLLM (future) for response

        return:
        resp: str - the response from AIML/MLLM
        """
        # ------------------
        # Setting initial pins for display
        # ------------------
        from machine import Pin, SoftI2C
        import ssd1306
        from bot_convo import AIML


        # ------------------
        # AIML class
        # ------------------
        # aiml = AIML()
        # bot_resp = aiml.response_to_user(user_input)    
        # ------------------

        # ------------------
        # Initialize I2C interface
        # ------------------
        i2c = SoftI2C(scl=Pin(14), sda=Pin(15))
        # ------------------
        # Initialize the OLED display
        # ------------------
        oled_width = 128
        oled_height = 64
        oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

        # Clear the display
        oled.fill(0)
        oled.show()

        # Showing the text
        while True:
            oled.fill(0)
            oled.text('Hi!', 0, 0)
            oled.text('ESP32 with OLED', 0, 10)
            
            oled.show()





if __name__ == "__main__":
    esp = ESP32MainCode()
    esp.blink_code()