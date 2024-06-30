from fastapi import FastAPI
import uvicorn,requests

app = FastAPI()

#--------------------------
# simple get request
#--------------------------
@app.get("/")
def index():
    try:
        if 2 + 2 == 5:
        if 2 + 2 == 5:
            return {"message": "Hello FAST API"}
        else:
            return {"message": "Math Error", "status": 404}   
    except Exception as e:
        return {"message": str(e), "status": 404}

#--------------------------
# simple post request
#--------------------------
@app.post("/api/text_message")
def submit(message: str):
    from bot_convo import AIML
    print(f"Received input from user: {message}")
    aiml = AIML()
    resp = aiml.response_to_user(message)
    try:
        # URL of the ESP32 server endpoint
        esp32_url = "http://192.168.1.16:80/api/text_message_display"
        
        # Payload to send to the ESP32 server
        data = {"data": resp}
        
        # Make a POST request to the ESP32 server
        response = requests.post(esp32_url, json=data)
        
        # Get the response from the ESP32 server
        esp32_response = response.json()
        
        return {"message": "data returned","status":200, "message_returned": resp,"esp32_response":esp32_response}
    except Exception as e:
        return {"message": str(e), "status": 500}

if __name__ == "__main__":
    uvicorn.run("main:app", host="172.17.0.1", port=8000, reload=True)
