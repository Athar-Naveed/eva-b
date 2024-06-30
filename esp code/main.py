# ----------------------
# imports
# ----------------------

import socket,network,time,camera
# ----------------------
# main code for esp32-cam 
# ----------------------


class ESP32MainCode:
    def __init__(self) -> None:
        self.checks()
        self.greet_disp()
        
    
    def greet_disp(self)->bool:
        display_check = self.display_code("Hi from EVA!")
        return display_check
        
    def checks(self):
        print("Running checks...")
        # --------------------
        # check_variables
        # --------------------
        call_disp = 0
        call_temp = 0
        # --------------------
        # checking display
        # --------------------
        print("Checking Display...")
        while call_disp < 4:
            call_disp += 1
            check_disp = self.greet_disp()
            if check_disp:
                print("Display Check Okay!")
                time.sleep(2)
                break
        else:
            print("Can't connect to display!")
            time.sleep(2)
        # --------------------
        # checking esp32-cam temp
        # --------------------
        print("Checking ESP32-cam temp...")
        self.display_code(f"Checking ESP32-cam temp...")
        time.sleep(2)
        while call_temp < 4:
            call_temp += 1
            check_temp = self.esp_temp()
            if check_temp and check_temp < 58:
                print("Temp. Check Okay!")
                self.display_code(f"Temp. Check Okay! {check_temp}C")
                time.sleep(2)
                break
        else:
            print("Too hot to run esp32-cam!")
            self.display_code("Too hot to run esp32-cam!")
            time.sleep(2)
        print("Running checks completed!")
        self.display_code("Running checks completed!")
        time.sleep(2)
        
    
    def esp_temp(self)->None:
        """
        Print the temperature of the ESP32-CAM.

        params:
        None

        return:
        None
        """
        # ----------------------
        # imports
        # ----------------------
        import esp32
        
        # ----------------------
        # print the temperature in celsius
        # ----------------------
        temperature = round((esp32.raw_temperature() - 32) * (5 / 9),2)
        print(f"ESP32-cam temperature: {temperature}°C")
        return temperature
    
    def wifi_access_point(self, ssid="ESP32-CAM", password="12345678"):
        """
        Start the ESP32-CAM as an access point.

        Parameters:
        ssid (str): The SSID (name) of the Wi-Fi network.
        password (str): The password for the Wi-Fi network.

        Returns:
        ip_address (str): The IP address of the ESP32-CAM access point.
        """
        # ----------------------
        # ----------------------
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid, password=password)
        print("Access Point started with SSID:", ssid)
        while not ap.active():
            pass
        ip_address = ap.ifconfig()[0]
        print("ESP32-CAM IP Address:", ip_address)
        return ip_address

    def blink_code(self) -> None:
        """
        blink led code: blinks a "white led" if pin is '4', if pin is "33", a red led will blink

        params:
        no receiving params

        return:
        this function returns None
        """
        # ----------------------
        # imports
        # ----------------------
        from machine import Pin
        import time
        
        # ----------------------
        # setting pin for led
        # ----------------------
        led = Pin(4, Pin.OUT)
        
        # ----------------------
        # blinking the LED
        # ----------------------
        while True:
            led.value(1)
            time.sleep(1)
            led.value(0)
            time.sleep(1)
            
    def getting_usermessage(self) -> str:
        """
        Get user message and display response.

        params:
        no receiving params

        return:
        bot_resp: str - the response from AIML/MLLM
        """
        # ----------------------
        # ----------------------
        bot_resp = self.display_code("Hi")
        # ----------------------
        # Return bot response for further processing if needed
        # ----------------------
        return bot_resp

    def display_code(self, user_input: str) -> bool:
        """
        Display code: this code will display output text on the oled display 

        params:
        user_input: str - the text to be send to the AIML (currently) and MLLM (future) for response

        return:
        bool - True if display device is found and text is shown, False otherwise
        """
        # ----------------------
        # imports
        # ----------------------
        from machine import Pin, SoftI2C
        import ssd1306
        
        
        # ----------------------
        # initialize I2C interface
        # ----------------------
        i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
        devices = i2c.scan()
        if not devices:
            return False
        
        # ----------------------
        # initialize the OLED display
        # ----------------------
        oled_width = 128
        oled_height = 64
        oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

        # ----------------------
        # clear the display
        # ----------------------
        oled.fill(0)
        oled.show()

        # ----------------------
        # split the text into lines that fit the display width
        # ----------------------
        max_chars_per_line = 15  # This value depends on the font size, adjust as needed
        lines = []
        while user_input:
            if len(user_input) > max_chars_per_line:
                line = user_input[:max_chars_per_line]
                user_input = user_input[max_chars_per_line:]
            else:
                line = user_input
                user_input = ""
            lines.append(line)
        
        # ----------------------
        # showing the text
        # ----------------------
        oled.fill(0)
        y = 0
        for line in lines:
            oled.text(line, 0, y)
            y += 10  # Adjust this value based on the font height
            if y >= oled_height:
                break
        oled.show()
        return True
            
    def connect_to_wifi(self, ssid: str, password: str, max_attempts: int = 20) -> str:
        """
        Connect to a Wi-Fi network.

        params:
        ssid: str - The SSID of the Wi-Fi network.
        password: str - The password for the Wi-Fi network.
        max_attempts: int - Maximum number of attempts to connect.

        return:
        ip_address: str - The IP address assigned to the ESP32-CAM.
        """
        # ----------------------
        # imports
        # ----------------------
        import network
        import time
        
        # ----------------------
        # ----------------------
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        attempts = 0
        # ----------------------
        # ----------------------
        print("Connecting to Wi-Fi...")
        while not sta.isconnected() and attempts < max_attempts:
            sta.connect(ssid, password)
            attempts += 1
            time.sleep(1)
        # ----------------------
        # ----------------------
        if not sta.isconnected():
            raise RuntimeError("Failed to connect to Wi-Fi")
        # ----------------------
        # ----------------------
        print("Connected to Wi-Fi:", ssid)
        time.sleep(1)  # Ensure the print statement completes
        ip_address = sta.ifconfig()[0]
        print("ESP32-Cam Snapshot API:", "http://" + str(ip_address) + "/snapshot")
        # ----------------------
        # ----------------------
        time.sleep(1)  # Ensure the print statement completes
        print("ESP32-Cam Stream API:", "http://" + str(ip_address) + "/stream")
        time.sleep(1)  # Ensure the print statement completes
        # ----------------------
        # ----------------------
        return ip_address
    
    def initialize_camera(self, uart_port=1, tx_pin=3, rx_pin=1):
        """
        Initialize the camera with specified UART port and pins.

        params:
        uart_port: int - The UART port number.
        tx_pin: int - The TX pin number.
        rx_pin: int - The RX pin number.

        return:
        None
        """
        # ----------------------
        # imports
        # ----------------------
        from machine import UART
        import camera
        
        # ----------------------
        # ----------------------
        uart = UART(uart_port, baudrate=115200, tx=tx_pin, rx=rx_pin)
        camera.init(0, format=camera.JPEG)
        camera.framesize(camera.FRAME_QVGA)  # Set resolution to QVGA (320x240)
        camera.quality(10)  # Set JPEG quality (lower value means higher compression)
        camera.speffect(camera.EFFECT_BW)  # Set effect to black and white


    def handle_stream_request(self, client_socket):
        """
        Handle stream request from the client.

        params:
        client_socket: socket - The client socket.

        return:
        None
        """
        # ----------------------
        # ----------------------
        try:
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n"
                "Connection: keep-alive\r\n\r\n"
            )
            client_socket.send(response)
            while True:
                snapshot = camera.capture()
                if snapshot:
                    frame_header = (
                        "--frame\r\n"
                        "Content-Type: image/jpeg\r\n"
                        "Content-Length: {}\r\n\r\n".format(len(snapshot))
                    )
                    client_socket.send(frame_header)
                    client_socket.send(snapshot)
                    client_socket.send("\r\n")
                    time.sleep(0.05)  # Adjust the delay as needed for frame rate
                else:
                    client_socket.send("HTTP/1.1 500 Internal Server Error\r\n\r\n")
                    break
        except Exception as e:
            print("Error streaming video:", e)
        finally:
            client_socket.close()

    def start_server(self, ip_address, port=80):
        """
        Start an HTTP server on the ESP32-CAM.

        params:
        ip_address: str - The IP address of the server.
        port: int - The port number for the server.

        return:
        server_socket: socket - The server socket.
        """

        # ----------------------
        # imports
        # ----------------------
        import socket
        
        # ----------------------
        # ----------------------
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(2)
        server_socket.bind((ip_address, port))
        time.sleep(1)
        server_socket.listen(5)  # Queue up to 5 connections
        print("Server started at {}:{}".format(ip_address, port))
        # ----------------------
        # ----------------------
        return server_socket
    
    def handle_client(self, client_socket):
        import json
        try:
            request = client_socket.recv(1024)
            request_str = request.decode('utf-8')
            print("Request received:", request_str)
            
            if "POST /api/text_message_display" in request_str:
                content_length = int(request_str.split('Content-Length: ')[1].split('\r\n')[0])
                body = request_str.split('\r\n\r\n')[1]
                while len(body) < content_length:
                    body += client_socket.recv(content_length - len(body)).decode('utf-8')
                print("Body received:", body)
                
                # Convert the JSON string to a dictionary
                message = json.loads(body)['data']
                
                
                self.display_code(message)
                
                response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"success\"}"
                client_socket.send(response.encode())
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
                client_socket.send(response.encode())
        except Exception as e:
            print("Error handling request:", e)
        finally:
            client_socket.close()
        



if __name__ == "__main__":
    esp = ESP32MainCode()
    ip = esp.connect_to_wifi("StormFiber","wlanad696f")
    server_socket = esp.start_server(ip)
    while True:
        client_socket,_ = server_socket.accept()
        time.sleep(2)
        esp.handle_client(client_socket)
    


