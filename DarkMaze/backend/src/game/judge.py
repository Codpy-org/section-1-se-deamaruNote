import numpy as np
import re
import json

# 用來快取已載入的迷宮資料
maze_cache = {}

def _parse_map(map_string, map_size, reversal_nodes=[]):
    width, height = map_size
    filtered_chars = re.sub(r'[^a-zA-Z]', '', map_string)
    
    QQ = [bin(ord(c))[2:].zfill(8) for c in filtered_chars]
    
    Dora_friend = []
    for Q in QQ:
        first_half = int(Q[:4], 2)
        second_half = int(Q[4:], 2)
        Dora_friend.extend([first_half % 2, second_half % 2])
    
    while len(Dora_friend) < width * height:
        Dora_friend.append(0)
    
    Dora_friend = Dora_friend[:width * height]
    
    swiper = np.array(Dora_friend).reshape((height, width))
    
    for x, y in reversal_nodes:
        if 0 <= x < height and 0 <= y < width:
            swiper[y, x] = 1 - swiper[y, x]
    
    return swiper

def _load_maze_from_json(maze_level_name):
    # 若迷宮已經載入過，直接返回快取資料
    if maze_level_name in maze_cache:
        return maze_cache[maze_level_name]

    try:
        with open(f"./src/game/maze_level/{maze_level_name}.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        maze_level_name = data.get("maze_level_name", "Unknown Level")
        map_size = tuple(data.get("map_size", [10, 10]))
        starting_position = tuple(data.get("starting_position", [0, 0]))
        end_position = tuple(data.get("end_position", [0, 0]))
        map_string = data.get("map", "")
        reversal_nodes = data.get("reversal_node", [])
        
        parsed_map = _parse_map(map_string, map_size, reversal_nodes)
        
        maze_data = {
            "maze_level_name": maze_level_name,
            "map_size": map_size,
            "starting_position": starting_position,
            "end_position": end_position,
            "map": parsed_map
        }
        
        # 將迷宮資料快取
        maze_cache[maze_level_name] = maze_data
        
        return maze_data
    except Exception as e:
        print(f"載入迷宮 '{maze_level_name}' 時發生錯誤: {e}")
        return None

def hit_obstacle(position, maze_level_name):
    x, y = position
    maze_data = _load_maze_from_json(maze_level_name)
    
    if maze_data:
        grid = maze_data["map"]
        
        if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
            return grid[y, x] == 1
        else:
            return True
    else:
        return True

def game_over(health):
    return health == 0 or health == 666

def arrive_at_destination(maze_level_name, current_position):
    maze_data = _load_maze_from_json(maze_level_name)
    
    if maze_data:
        end_position = tuple(maze_data.get("end_position", [0, 0]))
        return tuple(current_position) == end_position
    
    return False
