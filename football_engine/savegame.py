"""Pełny, JSON-owy zapis/odczyt kariery. Wersjonowany i odporny na nowe pola."""

from __future__ import annotations
import json, pathlib, datetime
from dataclasses import asdict, is_dataclass
from enum import Enum
from football_engine.career.player import Player
from football_engine.career.attributes import Attributes
from football_engine.career.position import Position
from football_engine.career.injury import Injury, InjuryType
from football_engine.world.club import Club
from football_engine.world.league import League
from football_engine.world.league_system import LeagueSystem
from football_engine.time_engine import GameCalendar

SAVE_VERSION=1

def _player(p):
    return {"id":p.id,"first_name":p.first_name,"last_name":p.last_name,"age":p.age,"country":p.country,
            "position":p.position.value,"attributes":p.attributes.as_dict(),"potential":p.potential,
            "preferred_foot":p.preferred_foot,"height_cm":p.height_cm,"weight_kg":p.weight_kg,
            "form":p.form,"condition":p.condition}

def _club(c):
    return {"id":c.id,"name":c.name,"country":c.country,"strength":c.strength,"transfer_budget":c.transfer_budget,
            "players":[_player(p) for p in c.squad]}

def serialize_world(league_system:LeagueSystem, calendar:GameCalendar, extra=None):
    return {"save_version":SAVE_VERSION,"saved_at":datetime.datetime.now(datetime.UTC).isoformat(),
            "calendar":{"season":calendar.season,"matchday":calendar.matchday,"current_date":calendar.current_date.isoformat()},
            "country":league_system.country,"promotion_count":league_system.promotion_count,"relegation_count":league_system.relegation_count,
            "leagues":[{"name":l.name,"country":l.country,"clubs":[_club(c) for c in l.clubs]} for l in league_system.leagues],
            "extra":extra or {}}

def save_world(path, league_system, calendar, extra=None):
    path=pathlib.Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(serialize_world(league_system,calendar,extra),ensure_ascii=False,indent=2),encoding="utf-8")
    return path

def _restore_player(d):
    p=Player(d["first_name"],d["last_name"],d["age"],d["country"],Position(d["position"]),Attributes(**d["attributes"]),d["potential"],d.get("preferred_foot","prawa"),d.get("height_cm",180),d.get("weight_kg",75))
    p.id=d.get("id",p.id); p.form=d.get("form",70); p.condition=d.get("condition",100); return p

def load_world(path):
    d=json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    if d.get("save_version",0)>SAVE_VERSION: raise ValueError("Zapis pochodzi z nowszej wersji gry.")
    leagues=[]
    for ld in d["leagues"]:
        clubs=[]
        for cd in ld["clubs"]:
            c=Club(cd["name"],cd["country"],cd["strength"],cd.get("transfer_budget",0)); c.id=cd.get("id",c.id)
            for pd in cd.get("players",[]): c.add_player(_restore_player(pd))
            clubs.append(c)
        leagues.append(League(ld["name"],ld["country"],clubs))
    ls=LeagueSystem(d["country"],leagues,d.get("promotion_count",2),d.get("relegation_count",2))
    cal=GameCalendar(d["calendar"]["season"],datetime.date.fromisoformat(d["calendar"]["current_date"])); cal.matchday=d["calendar"]["matchday"]
    return ls,cal,d.get("extra",{})
