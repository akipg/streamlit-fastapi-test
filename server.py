from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import signal

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, this is the FastAPI server!"}

@app.post("/shutdown")
async def shutdown(request: Request):
    os.kill(os.getpid(), signal.SIGTERM)
    return JSONResponse(content={"message": "Server is shutting down..."})

@app.get("/health")
def health():
    return {"status": "Server is running."}