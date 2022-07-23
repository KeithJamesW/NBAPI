from unicodedata import decimal
from pydantic import BaseModel
from datetime import date
from typing import List



class nba_teams(BaseModel):
    id: int
    name: str
    full_name: str
    abbreviation: str
    city: str
    conference: str
    division: str


class nba_players(BaseModel):
    id: int
    player_firstname: str
    player_lastname: str
    height_feet: int
    height_inches: int
    weight: int
    position: str
    
    

class nba_player_stats(BaseModel):
    id: int
    nba_player_id: int 
    points_per_game: int
    assists_per_game: int
    rebounds_per_game: int
    blocks_per_game: int
    field_goal_percentage: int

class Config:
        orm_mode = True



