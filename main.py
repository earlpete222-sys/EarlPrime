import asyncio
import json
import logging
import os
import re
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Web and AI Stack
import ollama
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

# =====================================================================
# 1. CORE DIRECTORY & GIT CONFIG
# =====================================================================
ROOT_DIR = Path("C:/EarlPrime").resolve()
TOOLS_DIR = ROOT_DIR / "learned_tools"
TOOLS_DIR.mkdir(exist_ok=True)

# FIX: Swapped out non-standard '%(node)s' with '%(levelname)s' to prevent internal formatting crashes
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("JarvisV8")

app = FastAPI(title="Jarvis Git-Host v8.0")

# =====================================================================
# 2. GIT AGENCY TOOL (The Persistence Layer)
# =====================================================================
class GitHost:
    @staticmethod
    def save_and_commit_tool(file_name: str, code: str, commit_msg: str):
        """Writes a .py file and commits it to the Git repository."""
        try:
            # 1. Write the file to the 'learned_tools' folder
            file_path = TOOLS_DIR / file_name
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # 2. Execute Git Lifecycle
            subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
            subprocess.run(["git", "commit", "-m", f"AUTO-EVOLUTION: {commit_msg}"], cwd=ROOT_DIR, check=True)
            
            return f"✅ SUCCESS: {file_name} hosted and committed to Git."
        except Exception as e:
            return f"❌ GIT_ERROR: {str(e)}"

# =====================================================================
# 3. RECURSIVE EVOLUTION LOGIC
# =====================================================================
class JarvisEngine:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def log(self, phase: str, detail: str = ""):
        await self.websocket.send_json({"phase": phase, "detail": detail})
        logger.info(f"{phase}: {detail}")

    async def evolve(self, objective: str):
        await self.log("Reasoning", "Strategizing Git Evolution...")
        
        # System prompt forcing JSON output for tool creation
        sys_prompt = (
            "You are Jarvis. You create Python tools. "
            "You MUST respond with a JSON block: "
            "```json\n{\"file_name\": \"name.py\", \"code\": \"code here\", \"summary\": \"description\"}\n
```"
        )
        
        try:
            # 1. AI Logic
            resp = ollama.chat(model="llama3.2:3b", messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": objective}
            ])
            content = resp['message']['content']

            # 2. Regex Extraction
            match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                await self.log("Action", f"Hosting {data['file_name']} via Git")
                
                # 3. Git Persistence
                result = GitHost.save_and_commit_tool(
                    data['file_name'], 
                    data['code'], 
                    data['summary']
                )
                await self.log("Result", result)
            else:
                await self.log("Error", "AI failed to produce a valid Git-hostable JSON block.")

        except Exception as e:
            await self.log("Crash", str(e))

# =====================================================================
# 4. WEB INTERFACE (iPhone Dashboard)
# =====================================================================
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html><head><title>Jarvis Git-Host</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 20px; }
        #console { border: 1px solid #222; padding: 10px; height: 60vh; overflow-y: auto; background: #050505; }
        input { width: 100%; padding: 15px; background: #111; border: 1px solid #0f0; color: #0f0; margin-top: 10px; }
        .phase { color: #fff; font-weight: bold; }
    </style></head>
    <body>
        <h2>🚀 JARVIS GIT-HOST v8.0</h2>
        <div id="console"></div>
        <input type="text" id="cmd" placeholder="Request new tool evolution..." onkeypress="if(event.key==='Enter') send()">
        <script>
            let ws = new WebSocket(`ws://${location.host}/ws`);
            ws.onmessage = (e) => {
                let d = JSON.parse(e.data);
                let c = document.getElementById('console');
                c.innerHTML += `<div><span class="phase">[${d.phase}]</span> ${d.detail}</div>`;
                c.scrollTop = c.scrollHeight;
            };
            function send() {
                let i = document.getElementById('cmd');
                ws.send(i.value); i.value = '';
            }
        </script>
    </body></html>
    """

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    engine = JarvisEngine(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            asyncio.create_task(engine.evolve(msg))
    except WebSocketDisconnect:
        pass

# =====================================================================
# 5. SERVER LAUNCHER (The Blocking Loop)
# =====================================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  JARVIS GIT-OPERATOR IS STARTING")
    print("="*50)
    print("  PC: http://localhost:8000")
    print("  IPHONE: http://192.168.1.160:8000")
    print("="*50)
    
    # FIX: Pass the app as an explicit module string target ("main:app") to guarantee process binding on Windows loopbacks
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
