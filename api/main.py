# -------------------------
# import libraries
# -------------------------
from fastapi import FastAPI
import uvicorn
app: FastAPI=FastAPI()
#--------------------------
# simple get request
#--------------------------
@app.get("/")
def index():
    try:
        if 2+2 == 5:
            return {"message": "Hello FAST API"}
        else:
            return {"message":e,"status":404}   
    except Exception as e:
        return {"message":e,"status":404}
@app.post("/api/submit")
def submit(item):
    print(f"Received input from user: {item}")
    return {"status": "success", "input_received": item}
if __name__ == "__main__":
   uvicorn.run("main:app",reload=True,port=1000,host="192.168.43.226") 

