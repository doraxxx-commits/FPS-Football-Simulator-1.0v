"""
Club — reprezentuje klub w świecie gry.

Etap 1 dał klubowi tożsamość, siłę drużyny (do symulacji meczów) i
statystyki tabelowe. Etap 3 dokłada prawdziwy skład zawodników i trenera
(punkty 12-14, 58-59) — `strength` może być teraz wyliczane ze składu
zamiast być ustawianym ręcznie na sztywno, jak zapowiadał komentarz
w Etapie 1. Finanse, infrastruktura itd. wciąż czekają na dalsze etapy.
"""

from __future__ import annotations

import uuid

from football_engine.career.player import Player
from football_engine.club.manager import Manager


class Club:
    """Pojedynczy klub piłkarski."""

    def __init__(self, name: str, country: str, strength: int, transfer_budget: float = 0.0) -> None:
        """
        Args:
            name: nazwa klubu, np. "Legia Warszawa".
            country: kraj klubu, np. "Polska".
            strength: siła drużyny w skali 1-100, używana do symulacji
                meczów. Jeśli klub ma przypisany skład, można ją zastąpić
                wyliczoną wartością przez `recalculate_strength_from_squad()`.
            transfer_budget: dostępny budżet transferowy (punkty 19, 29).
                Pełne finanse klubu (przychody, pensje, sponsorzy) czekają
                na dalszy etap — tu potrzebny jest tylko budżet do AI transferów.
        """
        if not (1 <= strength <= 100):
            raise ValueError("strength musi być w zakresie 1-100")

        self.id: str = str(uuid.uuid4())
        self.name = name
        self.country = country
        self.strength = strength
        self.transfer_budget = transfer_budget

        self.squad: list[Player] = []
        self.manager: Manager | None = None

        # Reset na początku każdego sezonu przez SeasonEngine.
        self.reset_season_stats()

    def add_player(self, player: Player) -> None:
        """Dodaje zawodnika do składu klubu."""
        self.squad.append(player)

    def remove_player(self, player_id: str) -> Player | None:
        """Usuwa zawodnika ze składu (np. przy transferze) i go zwraca."""
        for i, player in enumerate(self.squad):
            if player.id == player_id:
                return self.squad.pop(i)
        return None

    def set_manager(self, manager: Manager) -> None:
        self.manager = manager

    def players_at_position(self, position) -> list[Player]:
        """Zwraca zawodników ze składu grających na danej pozycji (punkt 12)."""
        return [p for p in self.squad if p.position == position]

    def recalculate_strength_from_squad(self, top_n: int = 18) -> None:
        """
        Przelicza `strength` klubu jako średnie OVR najlepszych `top_n`
        zawodników w składzie (przybliżenie kadry meczowej). Klub bez
        przypisanego składu zachowuje swoją dotychczasową, ręcznie ustawioną
        wartość — to nadal jest przydatne np. do szybkich demo bez pełnych składów.
        """
        if not self.squad:
            return
        best = sorted(self.squad, key=lambda p: p.ovr, reverse=True)[:top_n]
        avg_ovr = sum(p.ovr for p in best) / len(best)
        self.strength = round(max(1, min(100, avg_ovr)))

    def reset_season_stats(self) -> None:
        """Zeruje statystyki tabelowe — wywoływane na starcie nowego sezonu."""
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def points(self) -> int:
        return self.wins * 3 + self.draws

    def register_result(self, goals_for: int, goals_against: int) -> None:
        """Aktualizuje statystyki klubu po rozegranym meczu."""
        self.played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against

        if goals_for > goals_against:
            self.wins += 1
        elif goals_for == goals_against:
            self.draws += 1
        else:
            self.losses += 1

    def __repr__(self) -> str:
        return f"<Club {self.name} ({self.country}), siła={self.strength}>"
