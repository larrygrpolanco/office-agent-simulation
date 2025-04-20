# Prompt Template

## Overview
This directory contains prompt templates used to generate agent behaviors through large language models. These templates structure the inputs to language models, enabling them to produce specific types of outputs for different cognitive functions.

## Structure

### Main Files
- **gpt_structure.py**: Core functionality for generating embeddings and structuring prompts
- **run_gpt_prompt.py**: Orchestrates prompt execution for different cognitive functions
- **print_prompt.py**: Utilities for printing and debugging prompts
- **defunct_run_gpt_prompt.py**: Deprecated prompt systems (maintained for reference)

### Version Directories
The templates are organized into version directories:

#### v1/
Early prompt templates focusing on basic actions and planning:
- Action selection (location, object interaction)
- Daily planning and scheduling
- Basic action sequencing
- Initial conversation capabilities

#### v2/
Improved prompt templates with enhanced cognitive abilities:
- Detailed daily planning
- Conversation generation
- Thought processing
- Task decomposition
- Reaction and interaction capabilities
- Poignancy (emotional importance) calculation
- Memory summarization
- Reflection and insight generation

#### v3_ChatGPT/
Templates optimized for the ChatGPT model:
- Adapted v2 prompts for ChatGPT's input format
- Additional conversation capabilities
- Improved interaction and reaction models
- Enhanced memory and reflection prompts

### Safety
- **safety/anthromorphosization_v1.txt**: Guidelines for appropriate agent personification

## How Prompts Work

Each prompt template follows a similar structure:
1. **Context setup**: Information about the agent (identity, memory)
2. **Task description**: What the language model should generate
3. **Examples**: Few-shot examples showing expected outputs
4. **Current situation**: Specific details about the current state
5. **Output format**: Instructions for how to format the response

### Key Prompt Types

- **Planning prompts**: Generate daily schedules and decompose tasks
- **Action prompts**: Select locations, objects, and specific actions
- **Conversation prompts**: Generate dialogue and process conversations
- **Reflection prompts**: Create insights and process experiences
- **Memory prompts**: Summarize and interpret events and memories

## Example Workflow

1. A cognitive module (e.g., `plan.py`) needs to generate a specific output
2. It calls a function from `run_gpt_prompt.py` (e.g., `run_gpt_prompt_daily_plan`)
3. That function loads the appropriate template (e.g., `daily_planning_v6.txt`)
4. The template is filled with agent-specific information
5. The completed prompt is sent to the language model
6. The response is processed and returned to the cognitive module

The prompt templates are the "bridge" between the agent's internal state and the language model's capabilities, allowing structured generation of human-like behavior.