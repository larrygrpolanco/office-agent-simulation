import os
import json
import math
from backend.global_methods import (
    read_file_to_list,
    check_if_file_exists,
)

class Maze:
    """
    Feature-complete Maze class, ported and adapted from og_maze.py.
    Loads all maze and block data, builds tile metadata, and provides
    advanced access and event management for agent simulation.
    """

    def __init__(self, maze_dir="backend/office_map"):
        # Load meta info
        meta_path = os.path.join(maze_dir, "maze_meta_info.json")
        with open(meta_path, "r") as f:
            meta_info = json.load(f)
        self.maze_width = int(meta_info["maze_width"])
        self.maze_height = int(meta_info["maze_height"])
        self.sq_tile_size = int(meta_info["sq_tile_size"])
        self.special_constraint = meta_info.get("special_constraint", "")

        # Load special blocks
        blocks_folder = os.path.join(maze_dir, "special_blocks")
        wb_rows = read_file_to_list(os.path.join(blocks_folder, "world_blocks.csv"), header=False)
        wb = wb_rows[0][-1] if wb_rows and wb_rows[0] else ""
        sb_rows = read_file_to_list(os.path.join(blocks_folder, "sector_blocks.csv"), header=False)
        sb_dict = {row[0]: row[-1] for row in sb_rows if row}
        ab_rows = read_file_to_list(os.path.join(blocks_folder, "arena_blocks.csv"), header=False)
        ab_dict = {row[0]: row[-1] for row in ab_rows if row}
        gob_rows = read_file_to_list(os.path.join(blocks_folder, "game_object_blocks.csv"), header=False)
        gob_dict = {row[0]: row[-1] for row in gob_rows if row}
        slb_rows = read_file_to_list(os.path.join(blocks_folder, "spawning_location_blocks.csv"), header=False)
        slb_dict = {row[0]: row[-1] for row in slb_rows if row}

        # Load maze matrices
        maze_folder = os.path.join(maze_dir, "maze")
        collision_maze_raw = sum(read_file_to_list(os.path.join(maze_folder, "collision_maze.csv"), header=False), [])
        sector_maze_raw = sum(read_file_to_list(os.path.join(maze_folder, "sector_maze.csv"), header=False), [])
        arena_maze_raw = sum(read_file_to_list(os.path.join(maze_folder, "arena_maze.csv"), header=False), [])
        game_object_maze_raw = sum(read_file_to_list(os.path.join(maze_folder, "game_object_maze.csv"), header=False), [])
        spawning_location_maze_raw = sum(read_file_to_list(os.path.join(maze_folder, "spawning_location_maze.csv"), header=False), [])

        # Reshape to 2D
        def reshape(flat, width, height):
            return [flat[i*width:(i+1)*width] for i in range(height)]

        self.collision_maze = reshape(collision_maze_raw, self.maze_width, self.maze_height)
        sector_maze = reshape(sector_maze_raw, self.maze_width, self.maze_height)
        arena_maze = reshape(arena_maze_raw, self.maze_width, self.maze_height)
        game_object_maze = reshape(game_object_maze_raw, self.maze_width, self.maze_height)
        spawning_location_maze = reshape(spawning_location_maze_raw, self.maze_width, self.maze_height)

        # Build tiles matrix
        self.tiles = []
        for i in range(self.maze_height):
            row = []
            for j in range(self.maze_width):
                tile_details = dict()
                tile_details["world"] = wb
                tile_details["sector"] = sb_dict.get(sector_maze[i][j], "")
                tile_details["arena"] = ab_dict.get(arena_maze[i][j], "")
                tile_details["game_object"] = gob_dict.get(game_object_maze[i][j], "")
                tile_details["spawning_location"] = slb_dict.get(spawning_location_maze[i][j], "")
                tile_details["collision"] = self.collision_maze[i][j] != "0"
                tile_details["events"] = set()
                row.append(tile_details)
            self.tiles.append(row)

        # Add default game object events
        for i in range(self.maze_height):
            for j in range(self.maze_width):
                if self.tiles[i][j]["game_object"]:
                    object_name = ":".join([
                        self.tiles[i][j]["world"],
                        self.tiles[i][j]["sector"],
                        self.tiles[i][j]["arena"],
                        self.tiles[i][j]["game_object"]
                    ])
                    go_event = (object_name, None, None, None)
                    self.tiles[i][j]["events"].add(go_event)

        # Build reverse address mapping
        self.address_tiles = dict()
        for i in range(self.maze_height):
            for j in range(self.maze_width):
                addresses = []
                t = self.tiles[i][j]
                if t["sector"]:
                    addresses.append(f'{t["world"]}:{t["sector"]}')
                if t["arena"]:
                    addresses.append(f'{t["world"]}:{t["sector"]}:{t["arena"]}')
                if t["game_object"]:
                    addresses.append(f'{t["world"]}:{t["sector"]}:{t["arena"]}:{t["game_object"]}')
                if t["spawning_location"]:
                    addresses.append(f'<spawn_loc>{t["spawning_location"]}')
                for add in addresses:
                    if add in self.address_tiles:
                        self.address_tiles[add].add((j, i))
                    else:
                        self.address_tiles[add] = set([(j, i)])

        # Find the first nonzero spawn tile in spawning_location_maze
        self.spawn_tile = None
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                if spawning_location_maze[y][x] != "0":
                    self.spawn_tile = (x, y)
                    break
            if self.spawn_tile:
                break

    # --- Core Methods ---

    def access_tile(self, tile):
        """Return the tile's metadata dict at (x, y)."""
        x, y = tile
        return self.tiles[y][x]

    def get_tile_path(self, tile, level):
        """
        Get the tile string address given its coordinate and level.
        level: "world", "sector", "arena", or "game_object"
        """
        x, y = tile
        t = self.tiles[y][x]
        path = f"{t['world']}"
        if level == "world":
            return path
        path += f":{t['sector']}"
        if level == "sector":
            return path
        path += f":{t['arena']}"
        if level == "arena":
            return path
        path += f":{t['game_object']}"
        return path

    def get_nearby_tiles(self, tile, vision_r):
        """
        Return a list of (x, y) tiles within a square radius vision_r.
        """
        x, y = tile
        left_end = max(0, x - vision_r)
        right_end = min(self.maze_width, x + vision_r + 1)
        top_end = max(0, y - vision_r)
        bottom_end = min(self.maze_height, y + vision_r + 1)
        nearby_tiles = []
        for i in range(left_end, right_end):
            for j in range(top_end, bottom_end):
                nearby_tiles.append((i, j))
        return nearby_tiles

    def add_event_from_tile(self, curr_event, tile):
        """Add an event tuple to a tile."""
        self.tiles[tile[1]][tile[0]]["events"].add(curr_event)

    def remove_event_from_tile(self, curr_event, tile):
        """Remove an event tuple from a tile."""
        curr_tile_ev_cp = self.tiles[tile[1]][tile[0]]["events"].copy()
        for event in curr_tile_ev_cp:
            if event == curr_event:
                self.tiles[tile[1]][tile[0]]["events"].remove(event)

    def turn_event_from_tile_idle(self, curr_event, tile):
        """Mark an event as idle (set all but first element to None)."""
        curr_tile_ev_cp = self.tiles[tile[1]][tile[0]]["events"].copy()
        for event in curr_tile_ev_cp:
            if event == curr_event:
                self.tiles[tile[1]][tile[0]]["events"].remove(event)
                new_event = (event[0], None, None, None)
                self.tiles[tile[1]][tile[0]]["events"].add(new_event)

    def remove_subject_events_from_tile(self, subject, tile):
        """Remove all events for a subject from a tile."""
        curr_tile_ev_cp = self.tiles[tile[1]][tile[0]]["events"].copy()
        for event in curr_tile_ev_cp:
            if event[0] == subject:
                self.tiles[tile[1]][tile[0]]["events"].remove(event)

    def turn_coordinate_to_tile(self, px_coordinate):
        """
        Convert a pixel coordinate (x, y) to a tile coordinate (x, y).
        """
        x = math.ceil(px_coordinate[0] / self.sq_tile_size)
        y = math.ceil(px_coordinate[1] / self.sq_tile_size)
        return (x, y)

    def is_collision(self, x, y):
        """Return True if the tile at (x, y) is a collision block."""
        if 0 <= y < self.maze_height and 0 <= x < self.maze_width:
            return self.collision_maze[y][x] != "0"
        return True  # Out of bounds is treated as collision

    def get_spawn_location(self):
        """Return the first spawn tile found, or None."""
        return self.spawn_tile

    def get_width(self):
        return self.maze_width

    def get_height(self):
        return self.maze_height
