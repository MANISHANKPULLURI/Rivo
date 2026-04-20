# backend/server.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.agents.graph import app as agent_app
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🆕 NEW: This tells Open WebUI that "finance-agent" exists
@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "finance-agent",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "custom"
            }
        ]
    }

@app.post("/v1/chat/completions")
async def chat_endpoint(raw_request: Request):
    body = await raw_request.json()
    user_msg = body["messages"][-1]["content"]
    print(f"📥 Received from WebUI: {user_msg}")
    
    initial_state = {"messages": [{"role": "user", "content": user_msg}]}
    final_state = await agent_app.ainvoke(initial_state)
    
    report = final_state.get("final_report", "Agent failed to generate a report.")
    
    return {
        "id": f"chatcmpl-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "finance-agent", 
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": report
            },
            "finish_reason": "stop"
        }]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)