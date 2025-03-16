import sqlite3
import json
import logging

# 設定日誌記錄
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """獲取資料庫連接，使用上下文管理器"""
    conn = sqlite3.connect("game.db")
    return conn

def create_user(username):
    """Create user and initialize game state"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                INSERT INTO game_state (username, current_level_name, map_size, health, path, current_position)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, "maze-level-1", json.dumps([10, 10]), 3, json.dumps([[1, 0]]), json.dumps([1, 0])))
            conn.commit()
            logger.info(f"User {username} has been created and game state initialized!")
    except sqlite3.IntegrityError:
        logger.warning(f"User {username} already exists, no need to create!")

def reset_game_state(username):
    """Reset game state (if user exists, reset their state)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM game_state WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                # User exists, update data
                cursor.execute("""
                    UPDATE game_state 
                    SET current_level_name = ?, map_size = ?, health = ?, path = ?, current_position = ?
                    WHERE username = ?
                """, ("maze-level-1", json.dumps([10, 10]), 3, json.dumps([[1, 0]]), json.dumps([1, 0]), username))
                conn.commit()
                logger.info(f"Game state reset! (User: {username})")
            else:
                logger.warning(f"User {username} does not exist, please create an account first!")
    except Exception as e:
        logger.error(f"Error resetting game state for {username}: {e}")

def save_game_state(username, current_level_name, map_size, health, path, current_position):
    """Update game state (if user exists, update their state)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM game_state WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                # User exists, update data
                cursor.execute("""
                    UPDATE game_state 
                    SET current_level_name = ?, map_size = ?, health = ?, path = ?, current_position = ?
                    WHERE username = ?
                """, (current_level_name, json.dumps(map_size), health, json.dumps(path), json.dumps(current_position), username))
                conn.commit()
                logger.info(f"Game state updated! (User: {username})")
            else:
                logger.warning(f"User {username} does not exist, please create an account first!")
    except Exception as e:
        logger.error(f"Error saving game state for {username}: {e}")

def get_latest_game_state(username):
    """Query the latest game state for the given username"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM game_state WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                game_state = {
                    "username": result[1],
                    "current_level_name": result[2],
                    "map_size": json.loads(result[3]),
                    "health": result[4],
                    "path": json.loads(result[5]),
                    "current_position": json.loads(result[6]),
                    "message": "Load successful",
                    "cookies": [],
                    "status": 1
                }
                return game_state
            else:
                logger.warning(f"Cannot find game state for user {username}!")
                return None
    except Exception as e:
        logger.error(f"Error getting game state for {username}: {e}")
        return None
