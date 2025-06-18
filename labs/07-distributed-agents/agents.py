from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any, Optional
import json
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Initialize the model
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
if api_key:
    print("Using Azure OpenAI")
    deployment_name = os.environ.get("AZURE_OPENAI_REASONING_DEPLOYMENT_NAME") 
    llm = init_chat_model(
        deployment_name, 
        model_provider="azure_openai", 
        api_key=api_key, 
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
else:
    print("Using GitHub Inference")
    llm = init_chat_model(
        model=os.environ.get("AZURE_OPENAI_COMPLETION_MODEL"), 
        model_provider="openai", 
        temperature=0.7, 
        api_key=os.getenv("GITHUB_TOKEN"), 
        base_url="https://models.inference.ai.azure.com"
    )

# Create FastAPI app
app = FastAPI(title="Agent Servers", description="Distributed agents for text generation and editing")

# Input models
class WriterInput(BaseModel):
    input: str

class EditorInput(BaseModel):
    text: str

@app.post("/writer_agent")
async def writer_agent(request: WriterInput):
    """
    Writer agent that generates text based on the provided input.
    """
    try:
        # Create prompt for generating stories
        prompt = f"""You are a creative story writer. Write a short, engaging story based on the following prompt.
        Keep it under 300 words and make it interesting.
        
        Prompt: {request.input}
        """
        
        # Get response from language model
        response = await llm.ainvoke([{"role": "system", "content": prompt}])
        content = response.content if hasattr(response, 'content') else str(response)
        
        return JSONResponse(content={"response": content})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/editor_agent")
async def editor_agent(request: EditorInput):
    """
    Editor agent that improves and edits the provided text.
    """
    try:
        # Create prompt for editing text
        prompt = f"""You are a professional text editor. Improve the following text by:
        1. Fixing any grammar or spelling issues
        2. Enhancing the clarity and flow
        3. Improving word choice and sentence structure
        
        Keep the same general meaning and tone, but make the text more polished and professional.
        
        Text to edit: {request.text}
        """
        
        # Get response from language model
        response = await llm.ainvoke([{"role": "system", "content": prompt}])
        content = response.content if hasattr(response, 'content') else str(response)
        
        return JSONResponse(content={"response": content})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
