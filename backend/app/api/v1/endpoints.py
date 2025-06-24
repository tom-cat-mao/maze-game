from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
from app.models.pydantic_models import (
    MazeGenerationRequest, PathfindingRequest, PathfindingResponse,
    PuzzleRequest, PuzzleResponse, BossBattleRequest, BossBattleResponse
)
from app.algorithms.maze_generator import generate_maze as maze_gen_algo
from app.algorithms.pathfinder_dp import solve_with_dp
from app.algorithms.pathfinder_greedy import solve_with_greedy
from app.algorithms.puzzle_solver import solve_puzzle
from app.algorithms.boss_battle import solve_boss_battle

router = APIRouter()

@router.post("/maze/generate")
async def generate_maze_endpoint(request: MazeGenerationRequest):
    """
    Generates a new maze based on the provided size, streaming the generation process.
    """
    async def event_stream():
        maze_generator = maze_gen_algo(request.size, request.size)
        for maze_state in maze_generator:
            yield f"data: {json.dumps({'maze': maze_state})}\n\n"
            await asyncio.sleep(0.02)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/solve/dp", response_model=PathfindingResponse)
def solve_dp_endpoint(request: PathfindingRequest):
    """
    Solves the maze using Dynamic Programming.
    """
    try:
        path, value = solve_with_dp(request.maze)
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
    Solves a puzzle based on given constraints.
    """
    try:
        solution = solve_puzzle(request.constraints)
        if solution is None:
            raise HTTPException(status_code=404, detail="No solution found for the puzzle.")
        return {"solution": solution}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/solve/boss", response_model=BossBattleResponse)
def solve_boss_endpoint(request: BossBattleRequest):
    """
    Finds the optimal skill sequence for a boss battle.
    """
    try:
        sequence, turns = solve_boss_battle(request.boss_hp, request.skills)
        if sequence is None:
            raise HTTPException(status_code=404, detail="No solution found for the boss battle.")
        return {"sequence": sequence, "turns": turns}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
