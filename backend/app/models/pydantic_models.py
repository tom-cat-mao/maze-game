from pydantic import BaseModel, Field
from typing import List, Dict, Any

class MazeGenerationRequest(BaseModel):
    size: int = Field(..., gt=4, le=50, description="The size (width and height) of the maze.")

class MazeSchema(BaseModel):
    maze: List[List[str]]

from typing import Optional

class PathfindingRequest(BaseModel):
    maze: List[List[str]]
    main_path: Optional[List[List[int]]] = None

class PathfindingResponse(BaseModel):
    path: List[List[int]]
    value: int

class PuzzleRequest(BaseModel):
    password_hash: str
    constraints: List[Any]

class PuzzleResponse(BaseModel):
    solution: List[int]
    tries: int

class BossBattleRequest(BaseModel):
    boss_hps: List[int]
    skills: List[Dict[str, Any]]

class BossBattleResponse(BaseModel):
    sequence: List[str]
    turns: int
