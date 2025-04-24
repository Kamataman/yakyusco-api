from .team import Team, TeamBase, TeamCreate, TeamRead, TeamUpdate
from .player import  Player, PlayerBase, PlayerCreate, PlayerRead, PlayerReadWithTeam, PlayerUpdate

# __all__ = [
#     "Team",
#     "TeamBase",
#     "TeamCreate",
#     "TeamRead",
#     "TeamUpdate",
#     "Player",
#     "PlayerBase",
#     "PlayerCreate",
#     "PlayerRead",
#     "PlayerReadWithTeam",
#     "PlayerUpdate",
# ]

# PlayerReadWithTeam.model_rebuild()
Player.model_rebuild()
Team.model_rebuild()