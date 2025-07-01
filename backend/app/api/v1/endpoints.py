from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import random
import math
from app.models.pydantic_models import (
    MazeGenerationRequest, PathfindingRequest, PathfindingResponse,
    PuzzleRequest, PuzzleResponse, BossBattleRequest, BossBattleResponse
)
from app.algorithms.maze_generator import generate_maze as maze_gen_algo
from app.algorithms.pathfinder_dp import solve_with_dp
from app.algorithms.pathfinder_greedy import solve_with_greedy
from app.services.api_helpers import (
    prepare_and_solve_puzzle,
    prepare_and_solve_boss_battle,
)

router = APIRouter()

@router.post("/maze/generate")
async def generate_maze_endpoint(request: MazeGenerationRequest):
    """
    Generates a new maze based on the provided size, streaming the generation process.
    The final event in the stream includes dynamic boss data.
    """
    async def event_stream():
        maze_generator = maze_gen_algo(request.size, request.size)
        for data_payload in maze_generator:
            yield f"data: {json.dumps(data_payload)}\n\n"
            await asyncio.sleep(0.02)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/solve/dp", response_model=PathfindingResponse)
def solve_dp_endpoint(request: PathfindingRequest):
    """
    Solves the maze using Dynamic Programming.
    It can accept a pre-calculated main_path to optimize performance.
    """
    try:
        # Pass the main_path to the solver if it exists in the request
        path, value = solve_with_dp(request.maze, request.main_path)
        return {"path": path, "value": value}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/solve/greedy", response_model=PathfindingResponse)
def solve_greedy_endpoint(request: PathfindingRequest):
    """
    Solves the maze using a Greedy algorithm.
    """
    try:
        path, value = solve_with_greedy(request.maze)
        return {"path": path, "value": value}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/solve/puzzle", response_model=PuzzleResponse)
def solve_puzzle_endpoint(request: PuzzleRequest):
    """
    Solves a puzzle by calling the puzzle helper service.
    """
    try:
        solution, tries = prepare_and_solve_puzzle(request.password_hash, request.constraints)
        # The solver now returns an empty list on failure, which is a valid response.
        return {"solution": solution, "tries": tries}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in puzzle endpoint: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred in puzzle solving.")

@router.post("/solve/boss", response_model=BossBattleResponse)
def solve_boss_endpoint(request: BossBattleRequest):
    """
    Finds the optimal skill sequence for a boss battle by calling the boss battle helper service.
    """
    try:
        result = prepare_and_solve_boss_battle(request.boss_hps, request.skills)
        if result is None:
            raise HTTPException(status_code=404, detail="No solution found for the boss battle.")
        return result
    except Exception as e:
        print(f"Error in boss battle endpoint: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred in boss battle.")
