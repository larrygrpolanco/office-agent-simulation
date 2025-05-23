from fastapi import (
    FastAPI,
    APIRouter,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Optional, List
import datetime
import json
from backend.global_methods import check_if_file_exists
from backend.simulation_manager import SimulationManager

# Create simulation manager instance
sim_manager = SimulationManager()

# FastAPI app and CORS setup
app = FastAPI()

# Allow all origins for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

router = APIRouter()


class StartSimResponse(BaseModel):
    message: str
    step: int


class StepResponse(BaseModel):
    message: str
    step: int
    waiting_for_frontend: bool


class PersonaThoughtsResponse(BaseModel):
    thoughts: List[str]


class PersonaScheduleResponse(BaseModel):
    schedule: List[str]


@router.post("/simulation/start", response_model=StartSimResponse)
def start_simulation():
    sim_manager.start_simulation()
    return {"message": "Simulation started", "step": sim_manager.current_step}


@router.post("/simulation/step", response_model=StepResponse)
def advance_simulation_step():
    try:
        sim_manager.advance_step()
        return {
            "message": "Advanced to next step. Waiting for frontend update.",
            "step": sim_manager.current_step,
            "waiting_for_frontend": not check_if_file_exists(
                sim_manager._frontend_file(sim_manager.current_step)
            ),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/simulation/frontend-updated", response_model=StepResponse)
def frontend_updated():
    try:
        sim_manager.frontend_updated()
        return {
            "message": "Frontend update received. Ready for next step.",
            "step": sim_manager.current_step,
            "waiting_for_frontend": False,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/simulation/state")
def get_simulation_state():
    return sim_manager.get_state()


@router.get("/persona/thoughts", response_model=PersonaThoughtsResponse)
def get_persona_thoughts():
    return {"thoughts": sim_manager.get_persona_thoughts()}


@router.get("/persona/schedule", response_model=PersonaScheduleResponse)
def get_persona_schedule():
    return {"schedule": sim_manager.get_persona_schedule()}


app.include_router(router)

# --- WebSocket endpoint for step-based simulation ---


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Send a valid JSON "connected" message
    await websocket.send_text(json.dumps({"status": "connected"}))
    try:
        while True:
            # Receive step request from frontend (as JSON)
            data = await websocket.receive_text()
            try:
                request = json.loads(data)
            except Exception:
                # If not valid JSON, ignore
                continue

            # Handle different request types
            if request.get("action") == "next_step":
                # Process next simulation step
                start_time = datetime.datetime.now()
                
                # Get environment state from request
                env_data = request.get("environment", {})
                
                # Process agent decision using the cognitive loop
                agent_decision = sim_manager.process_agent_decision(env_data)
                
                # Calculate processing time
                end_time = datetime.datetime.now()
                processing_time = (end_time - start_time).total_seconds()
                
                # Format response for frontend
                response = {
                    "persona": {
                        "Michael Scott": agent_decision
                    },
                    "meta": {
                        "curr_time": datetime.datetime.now().strftime("%B %d, %Y, %H:%M:%S"),
                        "status": "complete",
                        "step_id": request.get("step_id", 0),
                        "processing_time": f"{processing_time:.1f}s"
                    },
                }
                await websocket.send_text(json.dumps(response))
                
            elif request.get("action") == "reset":
                # Reset simulation
                sim_manager.reset_simulation()
                
                response = {
                    "persona": {},
                    "meta": {
                        "curr_time": "Ready",
                        "status": "reset",
                        "step_id": 0
                    },
                }
                await websocket.send_text(json.dumps(response))
                
    except WebSocketDisconnect:
        pass
