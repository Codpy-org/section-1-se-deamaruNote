from ..database.operation import save_game_state
from .judge import hit_obstacle, game_over, arrive_at_destination

def move_location(game_state, direction):
    if game_over(game_state["health"]):
        return game_state
    
    x, y = game_state["current_position"]
    width, height = game_state["map_size"]
    
    # Define movement mapping
    move_map = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0)
    }
    
    # Check if the direction is valid
    if direction in move_map:
        dx, dy = move_map[direction]
        new_x = x + dx
        new_y = y + dy
        
        # Ensure new position is within bounds
        if 0 <= new_x < width and 0 <= new_y < height:
            new_position = [new_x, new_y]
        else:
            return game_state  # Out of bounds, no movement
    else:
        return game_state  # Invalid direction, no movement

    # Check if the new position hits an obstacle
    if hit_obstacle(new_position, game_state["current_level_name"]):
        # Update health if there's an obstacle
        game_state["health"] -= 1
    else:
        # Update path if the new position is not an obstacle
        if new_position not in game_state["path"]:
            game_state["path"].append(new_position)
        
        # Update position
        game_state["current_position"] = new_position

    # Check if the player has arrived at the destination
    if arrive_at_destination(game_state["current_level_name"], game_state["current_position"]):
        game_state["health"] = 666  # Game won, set health to 666

    # Update database with the new game state
    save_game_state(game_state['username'], game_state["current_level_name"], game_state["map_size"],
                    game_state["health"], game_state["path"], game_state["current_position"])

    return game_state
