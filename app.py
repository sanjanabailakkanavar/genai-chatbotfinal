from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# ------------------------
# APP SETUP
# ------------------------

app = FastAPI()

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🧠 Temporary Memory (simple list)
chat_history = []

# Request schema
class ChatRequest(BaseModel):
    message: str

# ------------------------
# CHAT API
# ------------------------

@app.post("/chat")
def chat(req: ChatRequest):
    # Add user message
    chat_history.append({
        "role": "user",
        "content": req.message
    })

    # Call model
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=chat_history
    )

    reply = response.choices[0].message.content

    # Add bot reply
    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    return {"reply": reply}

# ------------------------
# SERVE FRONTEND (ADDED)
# ------------------------

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")