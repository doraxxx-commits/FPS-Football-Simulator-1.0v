"""Reprezentacja: U19 -> U21 -> senior, powołania, mecze, EURO i MŚ."""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from enum import Enum
from football_engine.career.player import Player
from football_engine.match.simulation import simulate_match

class NationalLevel(str, Enum): U19="U19"; U21="U21"; SENIOR="Senior"

@dataclass
class InternationalTournament:
    name:str
    host:str
    teams:list[str]
    matches:list[tuple[str,str,int,int]]=field(default_factory=list)
    champion:str|None=None

@dataclass
class NationalTeam:
    country:str
    rng:random.Random=field(default_factory=random.Random)
    squads:dict[NationalLevel,list[Player]]=field(default_factory=dict)
    caps:dict[str,int]=field(default_factory=dict)
    tournament_wins:list[str]=field(default_factory=list)

    def eligible(self, players:list[Player], level:NationalLevel)->list[Player]:
        limits={NationalLevel.U19:(16,19),NationalLevel.U21:(19,21),NationalLevel.SENIOR:(21,99)}
        lo,hi=limits[level]; return [p for p in players if lo<=p.age<=hi and p.country==self.country]

    def select(self, players:list[Player], level:NationalLevel, size:int=23)->list[Player]:
        pool=sorted(self.eligible(players,level),key=lambda p:(p.ovr,p.form),reverse=True)[:size]
        self.squads[level]=pool
        return pool

    def play_match(self, opponent: "NationalTeam", level:NationalLevel=NationalLevel.SENIOR)->tuple[int,int]:
        a=self.squads.get(level,[]); b=opponent.squads.get(level,[])
        class Team:
            def __init__(self,name,strength): self.name=name; self.strength=strength
        ta=Team(self.country, max(35, sum(p.ovr for p in a)/max(1,len(a))))
        tb=Team(opponent.country, max(35, sum(p.ovr for p in b)/max(1,len(b))))
        r=simulate_match(ta,tb,self.rng)
        for p in a[:11]: self.caps[p.id]=self.caps.get(p.id,0)+1
        return r.home_goals,r.away_goals

    def qualify_tournament(self, name:str, opponents:list["NationalTeam"], level=NationalLevel.SENIOR)->InternationalTournament:
        self.select([p for ps in self.squads.values() for p in ps],level)
        tournament=InternationalTournament(name,"—",[self.country]+[o.country for o in opponents])
        score=0
        for opp in opponents:
            opp.select([p for ps in opp.squads.values() for p in ps],level)
            gf,ga=self.play_match(opp,level); tournament.matches.append((self.country,opp.country,gf,ga)); score += gf-ga
        if score>=0:
            tournament.champion=self.country; self.tournament_wins.append(name)
        return tournament
