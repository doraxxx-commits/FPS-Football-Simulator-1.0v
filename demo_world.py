import random
from football_engine.season.standings import print_table
from football_engine.time_engine import GameCalendar
from football_engine.world.club import Club
from football_engine.world.league import League
from football_engine.world.league_system import LeagueSystem
from football_engine.world.world_engine import WorldEngine

def build_demo_world():
    ekstraklasa=League("Ekstraklasa","Polska",[Club("Legia Warszawa","Polska",78),Club("Lech Poznań","Polska",76),Club("Raków Częstochowa","Polska",74),Club("Jagiellonia Białystok","Polska",70),Club("Pogoń Szczecin","Polska",68),Club("Cracovia","Polska",60)])
    pierwsza=League("1 Liga","Polska",[Club("GKS Katowice","Polska",64),Club("Widzew Łódź","Polska",62),Club("Chrobry Głogów","Polska",55),Club("Stal Mielec","Polska",53),Club("Odra Opole","Polska",50),Club("Górnik Łęczna","Polska",48)])
    return WorldEngine(LeagueSystem("Polska",[ekstraklasa,pierwsza],1,1),GameCalendar("2026/27"),random.Random(11))

if __name__=="__main__":
    w=build_demo_world(); print(w); [print_table(l) for l in w.league_system.leagues]; print(*w.simulate_full_season(),sep="\n")
