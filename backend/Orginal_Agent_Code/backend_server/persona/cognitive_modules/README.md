# Cognitive Modules

## Overview
This directory contains the core cognitive functions that power agent behavior in the Reverie simulation. Each module represents a different aspect of human-like cognition, allowing agents to perceive, plan, execute actions, reflect, and converse with others.

## Modules

### perceive.py
Handles how agents observe and interpret their environment.

**Key Functions:**
- `perceive()`: Main function that takes the agent's current state and returns relevant observed events
- `generate_poig_score()`: Assigns "poignancy" (importance) scores to events

**How It Works:**
1. Processes nearby tiles within the agent's vision range
2. Updates the agent's spatial memory with new observations
3. Filters events based on attention bandwidth
4. Checks for new events not already in memory
5. Assigns poignancy scores to important events
6. Adds events to associative memory with relevant metadata

### retrieve.py
Manages memory retrieval based on current context and importance.

**Key Functions:**
- `new_retrieve()`: Main function that takes focal points and returns relevant memories
- `get_most_recent_meeting_with()`: Finds when the agent last interacted with a specific person
- `retrieve()`: Legacy retrieval based on perceived events

**How It Works:**
1. Balances recency, importance, and relevance when retrieving memories
2. Uses semantic similarity (embeddings) to find related memories
3. Extracts different types of memories (events, thoughts, chats)
4. Normalizes and combines scores to prioritize the most useful memories
5. Returns a dictionary of memories organized by relevance

### plan.py
Orchestrates both long-term and short-term planning for agents.

**Key Functions:**
- `plan()`: Main function that generates the agent's next action plan
- `_long_term_planning()`: Creates daily schedules
- `_determine_action()`: Selects the next specific action
- `generate_task_decomp()`: Breaks down high-level activities into smaller tasks
- `generate_convo()`: Creates conversations between agents

**How It Works:**
1. Generates wake-up times and daily schedules at the start of each day
2. Decomposes activities into specific tasks with durations
3. Selects appropriate locations and objects for actions
4. Handles interactions with other agents (conversations, reactions)
5. Manages interruptions and schedule revisions

### execute.py
Translates plans into physical movements in the simulation.

**Key Functions:**
- `execute()`: Main function that takes a plan and returns movement coordinates
- `_get_paths()`: Finds paths to target locations

**How It Works:**
1. Converts action addresses (e.g., "double studio:bedroom:bed") to physical coordinates
2. Implements pathfinding to navigate the environment
3. Handles special cases like persona-persona interactions and waiting
4. Returns next tile coordinates, emoji representation, and action description
5. Manages movement constraints and boundaries

### reflect.py
Enables agents to process experiences and generate insights.

**Key Functions:**
- `reflect()`: Main function that triggers reflection processes
- `_generate_insights_and_evidence()`: Creates insights with supporting memories
- `_generate_focal_points()`: Identifies important topics to reflect on

**How It Works:**
1. Triggers reflection based on importance thresholds
2. Generates focal points from important memories
3. Creates insights with supporting evidence
4. Processes conversations to extract relationship information
5. Creates planning thoughts based on interactions

### converse.py
Manages conversations between agents.

**Key Functions:**
- `agent_chat_v1()` and `agent_chat_v2()`: Generate multi-turn conversations
- `generate_agent_chat_summarize_ideas()`: Creates summaries of conversations
- `open_convo_session()`: Initializes conversation state

**How It Works:**
1. Generates realistic, contextually-appropriate dialogue
2. Creates inner thoughts for agents during conversations
3. Manages turn-taking and context in multi-agent discussions
4. Summarizes conversations for memory storage
5. Extracts relationship insights from dialogue

## Interaction Pattern
These modules work together in a cycle:
1. **perceive.py** observes the environment
2. **retrieve.py** accesses relevant memories
3. **plan.py** decides what to do next
4. **execute.py** translates plans into actions
5. **reflect.py** processes experiences into insights
6. **converse.py** handles interactions with other agents

This cycle repeats continuously, creating emergent complex behavior from these simpler cognitive components.