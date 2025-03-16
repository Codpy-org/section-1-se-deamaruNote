import pytest
import httpx

USERNAME = "TestUser"
RESET_URL = f"http://127.0.0.1:8000/api/v1/reset?username={USERNAME}"
LOGIN_URL = f"http://127.0.0.1:8000/api/v1/login"
MOVE_URL = "http://127.0.0.1:8000/api/v1/move"
game_state = {}

async def login_request():
    """Simulates a frontend login."""
    payload = {"username": USERNAME}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(LOGIN_URL, json=payload)
    
    assert response.status_code == 200  # Ensure the request was successful

async def reset_request():
    """Reset Game state."""
    global game_state  # Make sure to modify the global game_state variable
    
    async with httpx.AsyncClient() as client:
        response = await client.get(RESET_URL)
    
    assert response.status_code == 200  # Ensure the request was successful
    game_state = response.json()
    assert game_state["current_position"] == [1, 0]  # Check the initial position

async def move_request(dir):
    """Simulates a frontend move request."""
    global game_state  # Make sure to modify the global game_state variable
    
    payload = {"username": USERNAME, "direction": dir}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(MOVE_URL, json=payload)
    
    assert response.status_code == 200  # Ensure the request was successful
    game_state = response.json()  # Update the game_state after the move
    assert game_state["health"] >= 3  # Ensure health is correct

@pytest.mark.asyncio
async def test_integration():
    await login_request()
    await reset_request()
    
    # Move down 5 times
    for i in range(5):
        await move_request("down")
    
    assert game_state["current_position"] == [1, 5]  # Ensure the position is correct after 5 moves

@pytest.mark.asyncio
async def test_solver():
    await login_request()
    await reset_request()
    
    # Move down 5 times
    for i in range(5):
        await move_request("down")
    
    assert game_state["health"] == 666  # Ensure health is correct
