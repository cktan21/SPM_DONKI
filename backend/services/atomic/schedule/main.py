from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from supabaseClient import SupabaseClient
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="Atomic Microservice: Schedule Service")
supabase = SupabaseClient()

@app.get("/")
def read_root():
    return {"message": "Schedule Service is running 🚀😌"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5300)