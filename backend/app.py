from fastapi import (
    FastAPI,
    APIRouter,
    HTTPException,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import threading
import os
from backend.global_methods import (
    write_json,
    read_json,
    check_if_file_exists,
    create_folder_if_not_there,
)
from backend.maze import Maze

SIM_DIR = "backend/simulation"

import glob


class SimulationManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.simulation_running = False
        self.current_step = 0
        self.persona_state = {
            "name": "Test Persona",
            "thoughts": [],
            "schedule": [],
            "position": None,
        }
        # Ensure simulation directory exists
        create_folder_if_not_there(f"{SIM_DIR}/dummy.txt")
        if os.path.exists(f"{SIM_DIR}/dummy.txt"):
            os.remove(f"{SIM_DIR}/dummy.txt")
        # Initialize Maze for spawn location
        self.maze = Maze()

    def _step_file(self, step):
        return f"{SIM_DIR}/step_{step}.json"

    def _frontend_file(self, step):
        return f"{SIM_DIR}/frontend_{step}.json"

    def start_simulation(self):
        with self.lock:
            self.simulation_running = True
            self.current_step = 0
            # Clean up old simulation files
            for f in glob.glob(f"{SIM_DIR}/step_*.json"):
                os.remove(f)
            for f in glob.glob(f"{SIM_DIR}/frontend_*.json"):
                os.remove(f)
            create_folder_if_not_there(self._step_file(0))
            # Load initial environment and persona memory
            try:
                import json

                env_path = "backend/simulation/init/environment/0.json"
                persona_mem_path = "backend/simulation/init/personas/Michael Scott/bootstrap_memory/core_memory.json"
                with open(env_path, "r") as f:
                    env = json.load(f)
                with open(persona_mem_path, "r") as f:
                    mem = json.load(f)
                persona_name = "Michael Scott"
                self.persona_state = {
                    "name": persona_name,
                    "thoughts": ["Simulation started."],
                    "schedule": mem.get("schedule", []),
                    "position": [env[persona_name]["x"], env[persona_name]["y"]],
                    "traits": mem.get("traits", []),
                    "current_action": env[persona_name].get("current_action", ""),
                }
            except Exception as e:
                # Fallback to default if files missing
                spawn = self.maze.get_spawn_location()
                self.persona_state = {
                    "name": "Test Persona",
                    "thoughts": ["Simulation started."],
                    "schedule": ["8:00 Arrive at office", "17:00 Leave office"],
                    "position": spawn,
                }
            write_json(self.persona_state, self._step_file(0))
            # Remove any leftover frontend files
            if check_if_file_exists(self._frontend_file(0)):
                os.remove(self._frontend_file(0))

    def advance_step(self):
        with self.lock:
            if not self.simulation_running:
                raise Exception("Simulation not running")
            # Wait for frontend update file before next step
            if check_if_file_exists(self._frontend_file(self.current_step)):
                # Frontend has updated, allow next step
                self.current_step += 1
                # Simulate persona thinking
                self.persona_state["thoughts"].append(
                    f"Step {self.current_step}: Thinking about work."
                )
                write_json(self.persona_state, self._step_file(self.current_step))
                # Remove frontend file for next step
                os.remove(self._frontend_file(self.current_step - 1))
            else:
                raise Exception("Waiting for frontend update before next step")

    def frontend_updated(self):
        with self.lock:
            if not self.simulation_running:
                raise Exception("Simulation not running")
            # Frontend writes its update file to signal backend can proceed
            write_json(
                {"frontend_updated": True}, self._frontend_file(self.current_step)
            )

    def get_state(self):
        with self.lock:
            persona_state = self.persona_state
            if check_if_file_exists(self._step_file(self.current_step)):
                persona_state = read_json(self._step_file(self.current_step))
            waiting_for_frontend = not check_if_file_exists(
                self._frontend_file(self.current_step)
            )
            return {
                "running": self.simulation_running,
                "step": self.current_step,
                "waiting_for_frontend": waiting_for_frontend,
                "persona": persona_state,
            }

    def get_persona_thoughts(self):
        with self.lock:
            if check_if_file_exists(self._step_file(self.current_step)):
                return read_json(self._step_file(self.current_step)).get("thoughts", [])
            return self.persona_state["thoughts"]

    def get_persona_schedule(self):
        with self.lock:
            if check_if_file_exists(self._step_file(self.current_step)):
                return read_json(self._step_file(self.current_step)).get("schedule", [])
            return self.persona_state["schedule"]


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

# --- WebSocket endpoint for simulation updates ---
import json


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Send a valid JSON "connected" message
    await websocket.send_text(json.dumps({"status": "connected"}))
    try:
        while True:
            # Receive environment state from frontend (as JSON)
            data = await websocket.receive_text()
            try:
                env = json.loads(data)
            except Exception:
                # If not valid JSON, ignore
                continue

            # For demo: respond with current persona state as JSON
            # (In a real system, you'd update simulation state here)
            position = sim_manager.persona_state.get("position", None)
            if position is None:
                # Get a default spawn position from the maze
                position = sim_manager.maze.get_spawn_location()
                sim_manager.persona_state["position"] = position
            
            response = {
                "persona": {
                    sim_manager.persona_state["name"]: {
                        "movement": position,
                        "pronunciatio": "💼 Working...",
                        "description": sim_manager.persona_state.get(
                            "current_action", "Starting work day"
                        ),
                        "chat": [],
                    }
                },
                "meta": {"curr_time": "9:00 AM", "status": "running"},
            }
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass
