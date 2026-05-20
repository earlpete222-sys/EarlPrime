import asyncio
import json
import logging
import os
import re
import sqlite3
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Core Stack
import ollama
import chromadb
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from chromadb.utils import embedding_functions

print("DEBUG: [1] Imports successful.")

# =====================================================================
# INITIALIZATION
# =====================================================================
ROOT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = ROOT_DIR / "jarvis_output"
CHROMA_PATH = ROOT_DIR / "earl_prime_vector_memory"
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"DEBUG: [2] Root directory set to {ROOT_DIR}")

app = FastAPI(title="Earl Prime v7.5 Diagnostic")

# =====================================================================
# CRITICAL CHECK: ChromaDB
# =====================================================================
try:
    print("DEBUG: [3] Attempting to connect to ChromaDB...")
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="earl_prime_longterm", embedding_function=embed_fn)
    print("DEBUG: [4] ChromaDB connection successful.")
except Exception as e:
    print(f"DEBUG: [!] ChromaDB Error: {e}")

# =====================================================================
# DASHBOARD HTML (Simplified for testing)
# =====================================================================
@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h1>Jarvis Diagnostic Page</h1><p>If you see this, the server is ALIVE.</p>"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"phase": "Connected", "detail": "Jarvis is listening."})
    await websocket.close()

# =====================================================================
# THE STARTER (REWRITTEN)
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 STARTING JARVIS SERVER ON PORT 8000")
    print("="*50)
    
    # Check if Ollama is running first
    try:
        ollama.list()
        print("DEBUG: [5] Ollama Service detected.")
    except Exception:
        print("DEBUG: [!] WARNING: Ollama is not running. AI features will fail.")

    print(f"IP: 192.168.1.160")
    print(f"Connect your iPhone to: http://192.168.1.160:8000")
    print("="*50)
    print("Waiting for Uvicorn to take over...")

    try:
        # We pass 'app' directly to avoid the 'main:app' import loop issue
        uvicorn.run(app, host="0.0.0.0", port=8000, access_log=True)
    except Exception as e:
        print(f"❌ CRITICAL SERVER CRASH: {e}")
        input("Press Enter to close...")
