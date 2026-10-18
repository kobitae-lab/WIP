from dataclasses import dataclass, field
from typing import List

@dataclass
class Player:
    puuid: str
    team: str
    agent_id: str
    is_me: bool

@dataclass
class GameState:
    match_id: str
    map: str
    state: str
    my_team: str
    game_mode: str
    players: List[Player] = field(default_factory=list)

MAP_NAMES = {
    "Ascent": "Ascent",
    "Bonsai": "Split",
    "Canyon": "Fracture",
    "Duality": "Bind",
    "Foxtrot": "Breeze",
    "Haven": "Haven",
    "Infinity": "Icebox",
    "Juliett": "Pearl",
    "Pitt": "Pearl",
    "Port": "Icebox",
    "Range": "The Range",
    "Triad": "Haven",
    "HURM_Alley": "Drift",
    "HURM_Bball": "Glitchpop",
    "Jam": "Sunset",
    "Poveglia": "Abyss",
    "Leviathan": "Lotus",
}

def parse_match(raw, my_puuid):
    PlayerList = []
    my_team = ""
    for p in raw.get("Players", []): # [] for error handling
        player = Player(puuid=p.get("Subject"), team=p.get("TeamID") , agent_id=p.get("CharacterID"), is_me=p.get("Subject") == my_puuid)
        PlayerList.append(player)
        if p.get("Subject") == my_puuid:
            my_team = p.get("TeamID")
    
    mapID = raw.get("MapID").split("/")[-1]

    gs = GameState(match_id=raw.get("MatchID"), 
                   map=MAP_NAMES.get(mapID, mapID),
                   state=raw.get("State"),
                   game_mode=raw.get("ModeID"),
                   players=PlayerList,
                   my_team = my_team)

    return gs