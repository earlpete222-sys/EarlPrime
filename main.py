import asyncio
import json
import logging
import re
import os
import sys
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Web and AI Stack
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import ollama

# --- 1. CONFIGURATION ---
print("--- JARVIS BOOT SEQUENCE STARTING ---")
ROOT_DIR = Path(__file__).parent.resolve()
app = FastAPI(title="Earl Prime v7.0")

# --- 2. THE DASHBOARD ---
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html><body style='background:#000;color:#0f0;font-family:monospace;padding:50px;'>
    <h1>JARVIS SYSTEM ONLINE</h1>
    <p>Status: Listening for iPhone Connection...</p>
    </body></html>
    """

# --- 3. THE ENGINE STARTER ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 STEP 1: INITIALIZING ENGINE")
    
    try:
        # Check if Port 8000 is busy
        print("🚀 STEP 2: CHECKING NETWORK PORTS")
        
        # This is the line that keeps the script alive
        print("🚀 STEP 3: STARTING WEB SERVER (BLOCKING MODE)")
        print("="*50)
        print("🔗 PC TEST: http://localhost:8000")
        print("📱 IPHONE TEST: http://192.168.1.160:8000")
        print("="*50)
        print("Waiting for connections...\n")

        # Running uvicorn directly on the 'app' object
        #
