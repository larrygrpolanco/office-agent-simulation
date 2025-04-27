# Temporary Storage

This directory manages transient data used during active simulations.

## Purpose

The temp_storage directory holds temporary files that support ongoing simulations, testing, and development.

## Key Files

- `curr_sim_code.json` - Identifier for the currently running simulation
- `path_tester_env.json` - Environment data for the path testing tool
- `path_tester_out.json` - Output from path testing operations

## How This Data Is Used

1. Current simulation code is used to track which simulation is active
2. Path tester files support debugging and testing agent navigation
3. These files are typically overwritten during operation

## Transient Nature

Unlike storage and compressed_storage, files in this directory are not meant for long-term preservation. They represent the current state of an active process rather than a complete simulation record.