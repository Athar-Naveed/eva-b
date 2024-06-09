import network
import time

def connect_to_wifi(ssid, password, max_attempts=20):
    try:
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        attempts = 0
        print("Connecting to Wi-Fi...")
        while not sta.isconnected() and attempts < max_attempts:
            sta.connect(ssid, password)
            attempts += 1
            time.sleep(1)
        if not sta.isconnected():
            raise RuntimeError("Failed to connect to Wi-Fi")
        print("Connected to Wi-Fi:", ssid)
        ip_address = sta.ifconfig()[0]
        print("ESP32-Cam IP Address:", ip_address)  # Print the IP address
        while True:
            pass
            
        
    except OSError as e:
        print("OS error:", e)
    except Exception as e:
        print("Error connecting to Wi-Fi:", e)

# Replace 'YourSSID' and 'YourPassword' with your Wi-Fi network credentials
ssid = "StormFiber"
password = "wlanad696f"
connect_to_wifi(ssid, password)
