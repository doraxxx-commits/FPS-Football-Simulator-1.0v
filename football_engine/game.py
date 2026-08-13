"""Wysokopoziomowy kontroler kariery łączący etapy 1-10."""
from __future__ import annotations
import random
from .world.world_engine import WorldEngine
from .cup import run_domestic_cup
from .polish import generate_news
from .savegame import save_world, load_world

class CareerGame:
    def __init__(self, world:WorldEngine, player=None, rng=None):
        self.world=world; self.player=player; self.rng=rng or random.Random()
        self.news=[]; self.cups={}
    @property
    def calendar(self): return self.world.calendar
    def play_season(self):
        self.world.run_transfer_window()
        events=self.world.simulate_full_season()
        self.cups["Puchar Polski"]=run_domestic_cup(self.world.league_system.all_clubs(),self.rng)
        self.news=generate_news(self.world,events,self.rng)
        return self.news
    def save(self,path,extra=None): return save_world(path,self.world.league_system,self.world.calendar,extra)
    @classmethod
    def load(cls,path):
        ls,cal,extra=load_world(path); return cls(WorldEngine(ls,cal),rng=random.Random()),extra
    def snapshot(self):
        return {"season":self.calendar.season,"date":self.calendar.current_date.isoformat(),"matchday":self.calendar.matchday,
          "leagues":[{"name":l.name,"table":[{"club":r.club.name,"pts":r.club.points,"gd":r.club.goal_difference} for r in self.world.get_last_table(i)]} for i,l in enumerate(self.world.league_system.leagues)],
          "news":[n.__dict__ for n in self.news]}
