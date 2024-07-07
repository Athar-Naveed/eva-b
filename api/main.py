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
            return {"message": "Hello FAST API"}
        else:
            return {"message": "Math Error", "status": 404}   
    except Exception as e:
        return {"message": str(e), "status": 404}

#--------------------------
# simple post request
#--------------------------
@app.post("/api/text_message")
def submit(message: dict):
    from bot_convo import AIML
    msg = message['message']
    aiml = AIML()
    resp = aiml.response_to_user(msg)
    print(f"resp:{resp}")
    try:
        # URL of the ESP32 server endpoint
        esp32_url = "http://192.168.1.17:80/api/text_message_display"
        
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
    uvicorn.run("main:app", host="192.168.1.15",port=8000, reload=True)