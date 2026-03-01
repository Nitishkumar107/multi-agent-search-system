from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # validate the structure of the incoming data
from typing import List, Optional
from app.core.ai_agent import get_response_from_ai_agent
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

# initialize the FastAPI app
app = FastAPI(
    title="AI Agent API",
    description="API for the AI Agent",
    version="1.0.0"
)

class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    user_input: List[str]
    allow_search : bool


@app.post("/chat")
async def chat(request:RequestState):
    logger.info(f"Received chat request: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Model {request.model_name} not supported")
        raise HTTPException(status_code=400, detail="Model not supported")

    try:
        response = get_response_from_ai_agent(
            request.model_name,
            request.user_input,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Successfully received response from AI agent{request.model_name}")
        return {"response": response}

    except Exception as e:
        logger.error(f"Error received response from AI agent{request.model_name}")
        raise HTTPException(status_code=500,
                            detail=str(CustomException("Error received response from AI agent", error_detail=str(e))))
    


