import threading
import os
import datetime
import glob
import json
from backend.global_methods import (
    write_json,
    read_json,
    check_if_file_exists,
    create_folder_if_not_there,
)
from backend.maze import Maze
from backend.persona.persona import Persona

SIM_DIR = "backend/simulation"


class SimulationManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.simulation_running = False
        self.current_step = 0
        self.persona = None
        self.persona_state = {
            "name": "Michael Scott",
            "thoughts": [],
            "schedule": [],
            "position": [25, 25],  # Default position to avoid null
        }
        # Ensure simulation directory exists
        create_folder_if_not_there(f"{SIM_DIR}/dummy.txt")
        if os.path.exists(f"{SIM_DIR}/dummy.txt"):
            os.remove(f"{SIM_DIR}/dummy.txt")
        # Initialize Maze for spawn location
        self.maze = Maze()
        
        # Initialize persona immediately for step-based architecture
        self._initialize_persona()

    def _initialize_persona(self):
        """Initialize the persona object"""
        try:
            persona_folder = "backend/simulation/init/personas/Michael Scott"
            self.persona = Persona("Michael Scott", persona_folder)
            
            # Load initial environment state
            env_path = "backend/simulation/init/environment/0.json"
            with open(env_path, "r") as f:
                env = json.load(f)
            
            # Set initial position from environment or spawn location
            if "Michael Scott" in env:
                initial_position = [env["Michael Scott"]["x"], env["Michael Scott"]["y"]]
            else:
                spawn = self.maze.get_spawn_location()
                initial_position = list(spawn) if spawn else [25, 25]
            
            self.persona_state = {
                "name": "Michael Scott",
                "thoughts": ["Ready to manage the office!"],
                "schedule": ["8:00 AM - Arrive at office", "9:00 AM - Morning announcements", "5:00 PM - Leave office"],
                "position": initial_position,
                "traits": ["enthusiastic", "well-meaning", "attention-seeking"],
                "current_action": "Ready to start work",
            }
            
            print(f"✅ Persona initialized successfully: {self.persona.name}")
            
        except Exception as e:
            print(f"❌ Error initializing Persona: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to default if files missing
            spawn = self.maze.get_spawn_location()
            self.persona_state = {
                "name": "Michael Scott",
                "thoughts": ["Ready to work (fallback mode)."],
                "schedule": ["8:00 Arrive at office", "17:00 Leave office"],
                "position": list(spawn) if spawn else [25, 25],
            }
            self.persona = None

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
            
            # Persona is already initialized in __init__, just update state
            if not self.persona:
                self._initialize_persona()
                
            write_json(self.persona_state, self._step_file(0))
            # Remove any leftover frontend files
            if check_if_file_exists(self._frontend_file(0)):
                os.remove(self._frontend_file(0))

    def reset_simulation(self):
        """Reset the simulation to initial state"""
        with self.lock:
            self.simulation_running = False
            self.current_step = 0
            
            # Clean up simulation files
            for f in glob.glob(f"{SIM_DIR}/step_*.json"):
                os.remove(f)
            for f in glob.glob(f"{SIM_DIR}/frontend_*.json"):
                os.remove(f)
            
            # Reinitialize persona
            self._initialize_persona()

    def process_agent_decision(self, env_data):
        """Process agent cognitive loop and return movement decision"""
        print(f"🔄 Starting cognitive loop for Michael Scott...")
        
        # Ensure we always have a valid position
        current_position = self.persona_state.get("position")
        if not current_position or current_position is None:
            spawn = self.maze.get_spawn_location()
            current_position = list(spawn) if spawn else [25, 25]
            self.persona_state["position"] = current_position
        
        print(f"📍 Current position: {current_position}")
        
        if not self.persona:
            print("❌ No persona initialized - trying to reinitialize...")
            self._initialize_persona()
            if not self.persona:
                print("❌ Persona initialization failed - using fallback")
                return {
                    "movement": current_position,
                    "pronunciatio": "💼",
                    "description": "Working at the office (persona not initialized)",
                    "chat": []
                }
        
        try:
            # Get current position from environment data
            agent_data = env_data.get("Michael Scott", {})
            curr_tile = (agent_data.get("x", current_position[0]), agent_data.get("y", current_position[1]))
            curr_time = datetime.datetime.now()
            
            print(f"🎯 Input to persona.move(): curr_tile={curr_tile}, curr_time={curr_time}")
            
            # Call the actual cognitive loop
            print("🧠 Calling persona.move() - starting AI cognitive loop...")
            next_tile, pronunciatio, description = self.persona.move(
                self.maze, 
                {"Michael Scott": self.persona}, 
                curr_tile, 
                curr_time
            )
            
            print(f"✅ persona.move() returned: next_tile={next_tile}, pronunciatio={pronunciatio}, description={description}")
            
            # Ensure next_tile is valid
            if next_tile is None or not isinstance(next_tile, (list, tuple)) or len(next_tile) != 2:
                print(f"⚠️ Invalid next_tile from persona.move(): {next_tile}, using current position")
                next_tile = current_position
            
            # Update persona state
            self.persona_state["position"] = list(next_tile)
            self.persona_state["current_action"] = description
            
            result = {
                "movement": list(next_tile),
                "pronunciatio": pronunciatio if pronunciatio else "💼",
                "description": description if description else "Working at the office",
                "chat": getattr(self.persona.scratch, 'chat', [])
            }
            
            print(f"📤 Returning result: {result}")
            return result
            
        except Exception as e:
            print(f"❌ Error in cognitive loop: {e}")
            import traceback
            traceback.print_exc()
            # Fallback behavior with guaranteed valid position
            return {
                "movement": current_position,
                "pronunciatio": "💼",
                "description": f"Working at the office (error: {str(e)[:50]}...)",
                "chat": []
            }

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
