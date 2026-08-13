"""
Symulacja meczu — Etap 1.

UWAGA co do zakresu: to NIE jest jeszcze "Mecz jako najlepsza część gry"
z punktu 30-32 Game Planu (decyzje akcja-po-akcji, kontekst minuty,
oceny meczowe zawodnika). To dopiero fundament: statystyczna symulacja
wyniku między dwoma klubami, oparta o ich `strength`, żeby tabela i
sezon miały sens matematyczny zanim dojdzie warstwa zawodnika/decyzji
(Etap 2 i dalej). Interaktywny match engine zastąpi/rozszerzy to w
Etapie 6, korzystając z tego samego modelu klubów i lig.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from football_engine.world.club import Club


@dataclass(frozen=True)
class MatchResult:
    home: Club
    away: Club
    home_goals: int
    away_goals: int

    @property
    def winner(self) -> Club | None:
        if self.home_goals > self.away_goals:
            return self.home
        if self.away_goals > self.home_goals:
            return self.away
        return None

    def __repr__(self) -> str:
        return f"{self.home.name} {self.home_goals}-{self.away_goals} {self.away.name}"


# Bazowa liczba oczekiwanych goli dla drużyny o "przeciętnej" sile (~50),
# grającej u siebie. Modyfikowana przez różnicę sił i przewagę gospodarza.
_BASE_EXPECTED_GOALS = 1.3
_HOME_ADVANTAGE = 0.25
_STRENGTH_SCALING = 0.035  # ile expected goals dodaje/odejmuje 1 pkt różnicy siły


def _expected_goals(attacker: Club, defender: Club, is_home: bool) -> float:
    strength_diff = attacker.strength - defender.strength
    expected = _BASE_EXPECTED_GOALS + strength_diff * _STRENGTH_SCALING
    if is_home:
        expected += _HOME_ADVANTAGE
    return max(0.15, expected)  # nawet najsłabsza drużyna ma szansę na gola


def simulate_match(home: Club, away: Club, rng: random.Random | None = None) -> MatchResult:
    """
    Symuluje jeden mecz między dwoma klubami metodą Poissona:
    liczba goli każdej drużyny jest losowana z rozkładu Poissona,
    którego średnia (lambda) zależy od siły obu drużyn i przewagi
    własnego boiska.

    Args:
        home: klub gospodarzy.
        away: klub gości.
        rng: opcjonalny generator liczb losowych (do testów deterministycznych).

    Returns:
        MatchResult z wynikiem meczu.
    """
    rng = rng or random.Random()

    home_lambda = _expected_goals(home, away, is_home=True)
    away_lambda = _expected_goals(away, home, is_home=False)

    home_goals = _poisson_sample(home_lambda, rng)
    away_goals = _poisson_sample(away_lambda, rng)

    return MatchResult(home=home, away=away, home_goals=home_goals, away_goals=away_goals)


def _poisson_sample(lam: float, rng: random.Random) -> int:
    """Prosta implementacja losowania z rozkładu Poissona (algorytm Knutha)."""
    l_threshold = 2.718281828459045 ** -lam  # e^-lambda
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= rng.random()
        if p <= l_threshold:
            return k - 1
