# Compressed Storage

This directory contains optimized versions of simulation data for efficient loading and replay.

## Purpose

The compressed_storage directory stores consolidated simulation data that reduces file count and optimizes loading times for simulation replays.

## Directory Structure

Each simulation run is stored in a separate folder with naming pattern:
- `[Date]_the_ville_[AgentNames]-step-[StepSize]-[RunNumber]/`
  - Example: `July1_the_ville_isabella_maria_klaus-step-3-20/`

Within each simulation folder:
- `master_movement.json` - Consolidated movement data for all timesteps
- `meta.json` - Simulation parameters and metadata
- `personas/` - Agent identity and memory data

## How This Data Is Used

1. The frontend loads these optimized files instead of individual timestep files
2. `master_movement.json` combines all movement data into a single file
3. This consolidated format enables faster loading and more efficient replay

## When Compressed Storage Is Used

Compressed storage is used for:
- Completed simulation replays
- Demo mode
- Sharing simulations between systems

## Relationship with Regular Storage

- Regular storage contains full-detail, timestep-by-timestep data
- Compressed storage contains the same data in a more efficient format
- Simulations may be converted from regular to compressed format for optimization