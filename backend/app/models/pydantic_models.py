from pydantic import BaseModel, Field
from typing import List, Dict, Any

class MazeGenerationRequest(BaseModel):
    size: int = Field(..., gt=4, le=50, description="The size (width and height) of the maze.")

class MazeSchema(BaseModel):
    maze: List[List[str]]

class PathfindingRequest(BaseModel):
    maze: List[List[str]]

class PathfindingResponse(BaseModel):
    path: List[List[int]]
    value: int

class PuzzleRequest(BaseModel):
    constraints: Dict[str, Any]

class PuzzleResponse(BaseModel):
    solution: List[int]

class BossBattleRequest(BaseModel):
    boss_hp: int
    skills: List[Dict[str, Any]]

class BossBattleResponse(BaseModel):
    sequence: List[str]
    turns: int
