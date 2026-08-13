"""FPS Football Player — kompletny silnik kariery."""
from .cup import CupCompetition, CupType, run_domestic_cup, run_european_qualification
from .national import NationalTeam, NationalLevel, InternationalTournament
from .savegame import save_world, load_world, serialize_world
__version__="6.0.0"
