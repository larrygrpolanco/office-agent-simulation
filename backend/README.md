# Office Agent Simulation Backend

Started the FastAPI backend server using 
`uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload`


## FastAPI Server Overview

This backend provides endpoints for step-by-step simulation control and persona inspection, designed for integration with a frontend UI.

## API Endpoints

### Simulation Control

- **POST /simulation/start**
  - Starts a new simulation.
  - Response: `{ "message": "Simulation started", "step": 0 }`

- **POST /simulation/step**
  - Advances the simulation by one step.
  - Only allowed if not waiting for frontend update.
  - Response: `{ "message": "...", "step": <int>, "waiting_for_frontend": true }`

- **POST /simulation/frontend-updated**
  - Notifies backend that the frontend has processed the latest step and updated any required JSON/state.
  - Response: `{ "message": "...", "step": <int>, "waiting_for_frontend": false }`

- **GET /simulation/state**
  - Returns the current simulation state, including persona info and whether waiting for frontend.

### Persona Inspection

- **GET /persona/thoughts**
  - Returns the current list of persona thoughts.

- **GET /persona/schedule**
  - Returns the persona's schedule.

## Example Frontend Flow

1. **Start Simulation**
   - `POST /simulation/start`
2. **Advance Step**
   - `POST /simulation/step`
   - Backend sets `waiting_for_frontend: true`
3. **Frontend processes new state, updates UI/JSON**
4. **Notify Backend**
   - `POST /simulation/frontend-updated`
   - Backend sets `waiting_for_frontend: false`
5. **Repeat Step 2-4 for each simulation step**

## Notes

- CORS is enabled for all origins for development.
- Only one simulation/persona is supported in this scaffold; extend as needed.
- Persona state is in-memory for now; file-based persistence can be added later.
- More endpoints (e.g., for persona details, map state, etc.) can be added as needed.
