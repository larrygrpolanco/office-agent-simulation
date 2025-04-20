"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: maze.py
Description: Defines the Maze class, which represents the map of the simulated
world in a 2-dimensional matrix. 
"""
import json
import numpy
import datetime
import pickle
import time
import math

from .global_methods import *
from .utils import *

class Maze: 
  def __init__(self, maze_name, env_matrix): 
    # READING IN THE BASIC META INFORMATION ABOUT THE MAP
    self.maze_name = maze_name
    # Reading in the meta information about the world. If you want tp see the
    # example variables, check out the maze_meta_info.json file. 
    meta_info = json.load(open(f"{env_matrix}/maze_meta_info.json"))
    self.maze_width = int(meta_info["maze_width"])
    self.maze_height = int(meta_info["maze_height"])
    self.sq_tile_size = int(meta_info["sq_tile_size"])
    self.special_constraint = meta_info["special_constraint"]

    # READING IN SPECIAL BLOCKS
    blocks_folder = f"{env_matrix}/special_blocks"

    _wb = blocks_folder + "/world_blocks.csv"
    wb_rows = read_file_to_list(_wb, header=False)
    wb = wb_rows[0][-1]
   
    _sb = blocks_folder + "/sector_blocks.csv"
    sb_rows = read_file_to_list(_sb, header=False)
    sb_dict = dict()
    for i in sb_rows: sb_dict[i[0]] = i[-1]
    
    _ab = blocks_folder + "/arena_blocks.csv"
    ab_rows = read_file_to_list(_ab, header=False)
    ab_dict = dict()
    for i in ab_rows: ab_dict[i[0]] = i[-1]
    
    _gob = blocks_folder + "/game_object_blocks.csv"
    gob_rows = read_file_to_list(_gob, header=False)
    gob_dict = dict()
    for i in gob_rows: gob_dict[i[0]] = i[-1]
    
    _slb = blocks_folder + "/spawning_location_blocks.csv"
    slb_rows = read_file_to_list(_slb, header=False)
    slb_dict = dict()
    for i in slb_rows: slb_dict[i[0]] = i[-1]

    # [SECTION 3] Reading in the matrices 
    maze_folder = f"{env_matrix}/maze"

    _cm = maze_folder + "/collision_maze.csv"
    collision_maze_raw = read_file_to_list(_cm, header=False)[0]
    _sm = maze_folder + "/sector_maze.csv"
    sector_maze_raw = read_file_to_list(_sm, header=False)[0]
    _am = maze_folder + "/arena_maze.csv"
    arena_maze_raw = read_file_to_list(_am, header=False)[0]
    _gom = maze_folder + "/game_object_maze.csv"
    game_object_maze_raw = read_file_to_list(_gom, header=False)[0]
    _slm = maze_folder + "/spawning_location_maze.csv"
    spawning_location_maze_raw = read_file_to_list(_slm, header=False)[0]

    self.collision_maze = []
    sector_maze = []
    arena_maze = []
    game_object_maze = []
    spawning_location_maze = []
    for i in range(0, len(collision_maze_raw), meta_info["maze_width"]): 
      tw = meta_info["maze_width"]
      self.collision_maze += [collision_maze_raw[i:i+tw]]
      sector_maze += [sector_maze_raw[i:i+tw]]
      arena_maze += [arena_maze_raw[i:i+tw]]
      game_object_maze += [game_object_maze_raw[i:i+tw]]
      spawning_location_maze += [spawning_location_maze_raw[i:i+tw]]

    self.tiles = []
    for i in range(self.maze_height): 
      row = []
      for j in range(self.maze_width):
        tile_details = dict()
        tile_details["world"] = wb
        
        tile_details["sector"] = ""
        if sector_maze[i][j] in sb_dict: 
          tile_details["sector"] = sb_dict[sector_maze[i][j]]
        
        tile_details["arena"] = ""
        if arena_maze[i][j] in ab_dict: 
          tile_details["arena"] = ab_dict[arena_maze[i][j]]
        
        tile_details["game_object"] = ""
        if game_object_maze[i][j] in gob_dict: 
          tile_details["game_object"] = gob_dict[game_object_maze[i][j]]
        
        tile_details["spawning_location"] = ""
        if spawning_location_maze[i][j] in slb_dict: 
          tile_details["spawning_location"] = slb_dict[spawning_location_maze[i][j]]
        
        tile_details["collision"] = False
        if self.collision_maze[i][j] != "0": 
          tile_details["collision"] = True

        tile_details["events"] = set()
        
        row += [tile_details]
      self.tiles += [row]
    for i in range(self.maze_height):
      for j in range(self.maze_width): 
        if self.tiles[i][j]["game_object"]:
          object_name = ":".join([self.tiles[i][j]["world"], 
                                  self.tiles[i][j]["sector"], 
                                  self.tiles[i][j]["arena"], 
                                  self.tiles[i][j]["game_object"]])
          go_event = (object_name, None, None, None)
          self.tiles[i][j]["events"].add(go_event)

    self.address_tiles = dict()
    for i in range(self.maze_height):
      for j in range(self.maze_width): 
        addresses = []
        if self.tiles[i][j]["sector"]: 
          add = f'{self.tiles[i][j]["world"]}:'
          add += f'{self.tiles[i][j]["sector"]}'
          addresses += [add]
        if self.tiles[i][j]["arena"]: 
          add = f'{self.tiles[i][j]["world"]}:'
          add += f'{self.tiles[i][j]["sector"]}:'
          add += f'{self.tiles[i][j]["arena"]}'
          addresses += [add]
        if self.tiles[i][j]["game_object"]: 
          add = f'{self.tiles[i][j]["world"]}:'
          add += f'{self.tiles[i][j]["sector"]}:'
          add += f'{self.tiles[i][j]["arena"]}:'
          add += f'{self.tiles[i][j]["game_object"]}'
          addresses += [add]
        if self.tiles[i][j]["spawning_location"]: 
          add = f'<spawn_loc>{self.tiles[i][j]["spawning_location"]}'
          addresses += [add]

        for add in addresses: 
          if add in self.address_tiles: 
            self.address_tiles[add].add((j, i))
          else: 
            self.address_tiles[add] = set([(j, i)])

  def turn_coordinate_to_tile(self, px_coordinate): 
    x = math.ceil(px_coordinate[0]/self.sq_tile_size)
    y = math.ceil(px_coordinate[1]/self.sq_tile_size)
    return (x, y)

  def access_tile(self, tile): 
    x = tile[0]
    y = tile[1]
    return self.tiles[y][x]

  def get_tile_path(self, tile, level): 
    x = tile[0]
    y = tile[1]
    tile = self.tiles[y][x]
    path = f"{tile['world']}"
    if level == "world": 
      return path
    else: 
      path += f":{tile['sector']}"
    if level == "sector": 
      return path
    else: 
      path += f":{tile['arena']}"
    if level == "arena": 
      return path
    else: 
      path += f":{tile['game_object']}"
    return path

  def get_nearby_tiles(self, tile, vision_r): 
    left_end = 0
    if tile[0] - vision_r > left_end: 
      left_end = tile[0] - vision_r
    right_end = self.maze_width - 1
    if tile[0] + vision_r + 1 < right_end: 
      right_end = tile[0] + vision_r + 1
    bottom_end = self.maze_height - 1
    if tile[1] + vision_r + 1 < bottom_end: 
      bottom_end = tile[1] + vision_r + 1
    top_end = 0
    if tile[1] - vision_r > top_end: 
      top_end = tile[1] - vision_r 
    nearby_tiles = []
    for i in range(left_end, right_end): 
      for j in range(top_end, bottom_end): 
        nearby_tiles += [(i, j)]
    return nearby_tiles

  def add_event_from_tile(self, curr_event, tile): 
    self.tiles[tile[1]][tile[0]]["events"].add(curr_event)

  def remove_event_from_tile(self, curr_event, tile):
    curr_tile_ev_cp = self.tiles[tile[1]][tile[0]]["events"].copy()
    for event in curr_tile_ev_cp: 
      if event == curr_event:  
        self.tiles[tile[1]][tile[0]]["events"].remove(event)

  def turn_event_from_tile_idle(self, curr_event, tile):
    curr_tile_ev_cp = self.tiles[tile[1]][tile[0]]["events"].copy()
    for event in curr_tile_ev_cp: 
      if event == curr_event:  
        self.tiles[tile[1]][tile[0]]["events"].remove(event)
        new_event = (event[0], None, None, None)
        self.tiles[tile[1]][tile[0]]["events"].add(new_event)

  def remove_subject_events_from_tile(self, subject, tile):
    curr_tile_ev_cp = self.tiles[tile[1]][tile[0]]["events"].copy()
    for event in curr_tile_ev_cp: 
      if event[0] == subject:  
        self.tiles[tile[1]][tile[0]]["events"].remove(event)
