from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
import os
from camel.typing import ModelType

from chatdev.chat_chain import ChatChain

app = FastAPI()

# Retrieve your personal API key from an environment variable
PERSONAL_API_KEY = os.environ.get("PERSONAL_OPENAI_KEY")

class ChatDevTask(BaseModel):
    task: str
    name: str
    org: str = "DefaultOrganization"
    config: str = "Default"
    model: str = "gpt-4-1106-preview"  # Default model
    path: str = ""

@app.post("/start_chat_chain/")
async def start_chat_chain(task: ChatDevTask, request: Request):
    api_key = request.headers.get("OpenAI-API-Key")

    if api_key == PERSONAL_API_KEY:
        allowed_models = ["gpt-4-1106-preview", "gpt-4", "gpt-4-32k"]
    else:
        allowed_models = ["gpt-4", "gpt-4-32k"]

    if task.model not in allowed_models:
        raise HTTPException(status_code=400, detail="Model not allowed")

    model_type = ModelType.GPT_4_TURBO if task.model == "gpt-4" else ModelType.GPT_4_32K
    if task.model == "gpt-4-1106-preview":
        model_type = ModelType.GPT_4_TURBO_V

    # Initialize ChatChain with the specified model type and paths
    chat_chain = ChatChain(
        config_path="CompanyConfig/Default/ChatChainConfig.json",
        config_phase_path="CompanyConfig/Default/PhaseConfig.json",
        config_role_path="CompanyConfig/Default/RoleConfig.json",
        task_prompt=task.task,
        project_name=task.name,
        org_name=task.org,
        model_type=model_type,
        code_path=task.path
    )

    # Run ChatChain processes
    chat_chain.pre_processing()
    chat_chain.make_recruitment()
    chat_chain.execute_chain()
    chat_chain.post_processing()

    return {"message": "Chat chain completed", "details": task.dict()}

@app.get("/")
async def read_root():
    return {"message": "Welcome to ChatDev FastAPI"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
