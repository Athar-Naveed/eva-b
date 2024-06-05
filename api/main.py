from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    message: str

@app.get("/")
def index():
    try:
        if 2 + 2 == 5:
            return {"message": "Hello FAST API"}
        else:
            return {"message": "Error", "status": 404}   
    except Exception as e:
        return {"message": str(e), "status": 404}

@app.post("/api/submit")
def getdisplay(item: Item):
    print(f"Received input from user: {item}")
    return {"status": "success", "input_received": item}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=1000, host="192.168.43.226")
