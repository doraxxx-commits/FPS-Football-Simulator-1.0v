import tempfile
import unittest
from pathlib import Path
from football_engine.world.club import Club
from football_engine.world.league import League
from football_engine.world.league_system import LeagueSystem
from football_engine.time_engine import GameCalendar
from football_engine.world.world_engine import WorldEngine
from football_engine.season.fixtures import generate_double_round_robin
from football_engine.cup import run_domestic_cup
from football_engine.savegame import save_world, load_world

class CompletionTests(unittest.TestCase):
 def test_odd_fixture_schedule(self):
  clubs=[Club(str(i),"PL",50) for i in range(5)]
  f=generate_double_round_robin(clubs)
  self.assertEqual(len(f),20); self.assertEqual(len(set((x.home.id,x.away.id) for x in f)),20)

 def test_world_season(self):
  ls=LeagueSystem("PL",[League("A","PL",[Club(str(i),"PL",50+i) for i in range(4)])],1,1)
  w=WorldEngine(ls,GameCalendar("2026/27"))
  w.simulate_full_season(); self.assertEqual(w.calendar.season,"2027/28")

 def test_cup(self):
  clubs=[Club(str(i),"PL",50+i) for i in range(5)]
  self.assertIn(run_domestic_cup(clubs).champion,clubs)

 def test_save_load(self):
  ls=LeagueSystem("PL",[League("A","PL",[Club("A","PL",60),Club("B","PL",55)])])
  c=GameCalendar(); p=Path(tempfile.mktemp(suffix=".json")); save_world(p,ls,c,{"x":1}); ls2,cal,extra=load_world(p); self.assertEqual(ls2.leagues[0].clubs[0].name,"A"); self.assertEqual(extra["x"],1)
