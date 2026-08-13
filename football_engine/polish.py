"""Warstwa prezentacji: newsy, balans i manifest efektów UI/audio."""

from __future__ import annotations
import random
from dataclasses import dataclass

@dataclass(frozen=True)
class NewsItem:
    title:str; body:str; category:str="Świat"; priority:int=50

def generate_news(world, events:list[str], rng=None)->list[NewsItem]:
    rng=rng or random.Random()
    news=[NewsItem("Wiadomości ze świata",e,"Świat",rng.randint(40,80)) for e in events]
    for league in world.league_system.leagues:
        table=world.get_last_table(world.league_system.leagues.index(league))
        if table:
            news.append(NewsItem(f"Lider {league.name}",f"{table[0].club.name} prowadzi z {table[0].club.points} pkt.","Liga",70))
    return sorted(news,key=lambda n:n.priority,reverse=True)

def balance_strength(strength:float)->int:
    """Łagodne ograniczenie ekstremów, zachowujące różnice między klubami."""
    return max(1,min(100,round(50+(strength-50)*0.92)))

UI_EFFECTS={"goal":"goal","transfer":"transfer","injury":"injury","promotion":"promotion","notification":"notification"}
