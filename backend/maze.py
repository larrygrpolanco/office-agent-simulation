import csv
import os

class Maze:
    def __init__(self, maze_dir="backend/office_map"):
        """
        Loads maze and block data from CSVs in the given directory.
        Expects:
            - maze_meta_info.json (for width, height, tile size, etc.)
            - maze/collision_maze.csv
            - maze/sector_maze.csv
            - maze/arena_maze.csv
            - maze/game_object_maze.csv
            - maze/spawning_location_maze.csv
            - special_blocks/spawning_location_blocks.csv
        """
        import json

        # Load meta info
        meta_path = os.path.join(maze_dir, "maze_meta_info.json")
        with open(meta_path, "r") as f:
            meta_info = json.load(f)
        self.maze_width = int(meta_info["maze_width"])
        self.maze_height = int(meta_info["maze_height"])
        self.sq_tile_size = int(meta_info["sq_tile_size"])
        self.special_constraint = meta_info.get("special_constraint", "")

        # Load collision maze
        self.collision_maze = self._load_flat_csv(os.path.join(maze_dir, "maze/collision_maze.csv"))
        # Convert to 2D
        self.collision_maze = [
            self.collision_maze[i:i+self.maze_width]
            for i in range(0, len(self.collision_maze), self.maze_width)
        ]

        # Load spawn locations (assume only one for now)
        spawn_blocks_path = os.path.join(maze_dir, "special_blocks/spawning_location_blocks.csv")
        self.spawn_locations = []
        if os.path.exists(spawn_blocks_path):
            with open(spawn_blocks_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    # Format: color, world, sector, arena, spawn_name
                    if len(row) >= 5:
                        self.spawn_locations.append({
                            "color": row[0],
                            "world": row[1],
                            "sector": row[2],
                            "arena": row[3],
                            "spawn_name": row[4]
                        })

        # Find the first nonzero spawn tile in spawning_location_maze.csv
        spawn_maze_path = os.path.join(maze_dir, "maze/spawning_location_maze.csv")
        self.spawn_tile = None
        if os.path.exists(spawn_maze_path):
            spawn_maze_flat = self._load_flat_csv(spawn_maze_path)
            for idx, val in enumerate(spawn_maze_flat):
                if val != "0":
                    x = idx % self.maze_width
                    y = idx // self.maze_width
                    self.spawn_tile = (x, y)
                    break

    def _load_flat_csv(self, path):
        with open(path, "r") as f:
            reader = csv.reader(f)
            flat = []
            for row in reader:
                flat.extend([cell.strip() for cell in row])
        return flat

    def is_collision(self, x, y):
        if 0 <= y < len(self.collision_maze) and 0 <= x < len(self.collision_maze[0]):
            return self.collision_maze[y][x] != "0"
        return True  # Out of bounds is treated as collision

    def get_spawn_location(self):
        return self.spawn_tile

    def get_width(self):
        return self.maze_width

    def get_height(self):
        return self.maze_height
