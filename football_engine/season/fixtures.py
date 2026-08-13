"""
Generowanie terminarza sezonu.

Punkt 24 Game Planu: "Każdy sezon ma prawdziwy terminarz [...] Nie chcemy
losowania 'następnego meczu' bez rzeczywistej struktury sezonu."

Ten moduł buduje pełny, ustalony z góry harmonogram kolejek (metoda
"circle method"), zamiast losować mecze na bieżąco. Dla N klubów
generowana jest runda zasadnicza (N-1 kolejek) i rewanżowa (kolejne
N-1 kolejek, z odwróconymi gospodarzami) — czyli standardowy układ
ligowy "każdy z każdym dwukrotnie".
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Tylko do podpowiedzi typów — patrz analogiczny komentarz w club/squad.py
    # o unikaniu cyklu importów world <-> season.
    from football_engine.world.club import Club


@dataclass(frozen=True)
class Fixture:
    matchday: int
    home: Club
    away: Club
    played: bool = False


def generate_double_round_robin(clubs: list[Club]) -> list[Fixture]:
    """
    Generuje pełny terminarz podwójnego "każdy z każdym".

    Args:
        clubs: lista klubów w lidze (parzysta liczba — dla nieparzystej
            liczby klubów należy dodać "bye"/wolny los, co dojdzie
            w kolejnym etapie razem z obsługą lig o nietypowej wielkości).

    Returns:
        Lista Fixture w kolejności kolejek (matchday 1, 2, 3, ...).
    """
    # Dla nieparzystej liczby klubów dodajemy wirtualny wolny los.
    # Dzięki temu każda kolejka ma dokładnie jednego pauzującego klubowego.
    bye = None
    n = len(clubs)
    rotation = list(clubs)
    if n % 2:
        bye = object()
        rotation.append(bye)
        n += 1
    fixtures: list[Fixture] = []

    rounds_in_half = n - 1
    for round_index in range(rounds_in_half):
        for i in range(n // 2):
            home = rotation[i]
            away = rotation[n - 1 - i]
            if home is bye or away is bye:
                continue
            # Naprzemiennie odwracamy gospodarza w kolejnych kolejkach,
            # żeby jeden klub nie grał wszystkich pierwszych meczów u siebie.
            if round_index % 2 == 1:
                home, away = away, home
            fixtures.append(Fixture(matchday=round_index + 1, home=home, away=away))

        # Rotacja "circle method": pierwszy element stały, reszta się obraca.
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    # Runda rewanżowa: te same pary, odwrócone gospodarstwo.
    second_half = [
        Fixture(matchday=f.matchday + rounds_in_half, home=f.away, away=f.home)
        for f in fixtures
    ]

    return fixtures + second_half
