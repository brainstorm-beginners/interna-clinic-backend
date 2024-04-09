import uvicorn
from fastapi import FastAPI

app = FastAPI()


# TODO: Delete or change this endpoint (it's for testing only)
@app.get("/")
async def home():
    return {"data": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
