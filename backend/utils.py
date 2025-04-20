# backend/utils.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API Key from environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Put your name
key_owner = "<Lawrence>"

# Asset and environment paths (adapted for new project structure)
maze_assets_loc = "../frontend/assets"
env_matrix = f"{maze_assets_loc}/the_office/matrix"
env_visuals = f"{maze_assets_loc}/the_office/visuals"

fs_storage = "../frontend/storage"
fs_temp_storage = "../frontend/temp_storage"

collision_block_id = "1"

# Verbose
debug = True
