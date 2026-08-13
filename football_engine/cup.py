"""Puchary krajowe i europejskie: faza ligowa + pucharowa, losowania i awanse."""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING
from football_engine.match.simulation import MatchResult, simulate_match
if TYPE_CHECKING:
    from football_engine.world.club import Club

class CupType(str, Enum):
    POLISH_CUP="Puchar Polski"; CONFERENCE="Liga Konferencji"; EUROPA="Liga Europy"; CHAMPIONS="Liga Mistrzów"

@dataclass
class CupTie:
    home: "Club"; away: "Club"; leg: int=1
    result: MatchResult|None=None
    winner: "Club"|None=None

@dataclass
class CupCompetition:
    name: str
    cup_type: CupType
    teams: list["Club"]
    rng: random.Random = field(default_factory=random.Random)
    ties: list[CupTie] = field(default_factory=list)
    champion: "Club"|None = None
    round_name: str = "start"

    def _play_tie(self, home, away, leg=1) -> CupTie:
        result=simulate_match(home,away,rng=self.rng)
        winner=result.winner
        if winner is None:
            winner=home if self.rng.random()<.5 else away
        tie=CupTie(home,away,leg,result,winner); self.ties.append(tie); return tie

    def _knockout_round(self, teams, name):
        self.round_name=name; self.rng.shuffle(teams); winners=[]
        while len(teams)>=2:
            a,b=teams.pop(),teams.pop()
            winners.append(self._play_tie(a,b).winner)
        if teams: winners.append(teams[0]) # bye
        return winners

    def run(self) -> "Club":
        teams=list(dict.fromkeys(self.teams))
        if len(teams)<2: raise ValueError("Puchar wymaga co najmniej 2 drużyn.")
        # Europejskie rozgrywki mają fazę ligową dla 36 ekip; pozostałe
        # rozgrywki korzystają z klasycznego systemu pucharowego.
        if self.cup_type in (CupType.CHAMPIONS,CupType.EUROPA,CupType.CONFERENCE) and len(teams)>=8:
            self.round_name="faza ligowa"
            self.rng.shuffle(teams)
            ranked=sorted(teams, key=lambda c:(c.strength+self.rng.random()*20), reverse=True)
            teams=ranked[:min(16,len(ranked))]
        round_no=1
        while len(teams)>1:
            teams=self._knockout_round(teams, f"1/{2**round_no} finału" if len(teams)>2 else "finał")
            round_no+=1
        self.champion=teams[0]; self.round_name="zakończony"; return teams[0]

def run_domestic_cup(clubs:list["Club"], rng=None)->CupCompetition:
    cup=CupCompetition("Puchar Polski",CupType.POLISH_CUP,clubs,rng or random.Random()); cup.run(); return cup

def run_european_qualification(champions:list["Club"], cup_winner:"Club"|None, league_top:list["Club"], rng=None)->dict[str,CupCompetition]:
    """Przydziela polskie kluby do LM/LE/LK według wyników sezonu."""
    pool=list(dict.fromkeys(champions+([cup_winner] if cup_winner else [])+league_top))
    while len(pool)<6 and league_top: pool.append(league_top[len(pool)%len(league_top)])
    rng=rng or random.Random()
    return {
        "Liga Mistrzów":CupCompetition("Liga Mistrzów",CupType.CHAMPIONS,pool[:2],rng),
        "Liga Europy":CupCompetition("Liga Europy",CupType.EUROPA,pool[2:4],rng),
        "Liga Konferencji":CupCompetition("Liga Konferencji",CupType.CONFERENCE,pool[4:6],rng),
    }
