"""
Player — zawodnik, którym gracz przeżywa karierę (punkt 1 i 6 Game Planu).

Zakres Etapu 2: OVR + atrybuty + potencjał + forma + kondycja + kontuzje.
Celowo NIE ma tu jeszcze: kontraktu, pensji, wartości rynkowej, klubu,
reputacji ani morale — to wiąże się z klubem/rynkiem transferowym i
trafi do Etapu 3 (Klub) i Etapu 4 (Transfery), żeby Player nie stał się
przedwcześnie klasą odpowiedzialną za wszystko.
"""

from __future__ import annotations

import uuid

from football_engine.career.attributes import Attributes, calculate_ovr
from football_engine.career.injury import Injury
from football_engine.career.position import Position

_MIN_STAT = 0
_MAX_STAT = 100


def _clamp(value: int) -> int:
    return max(_MIN_STAT, min(_MAX_STAT, value))


class Player:
    """Zawodnik — postać gracza (lub dowolny NPC-zawodnik w świecie)."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        age: int,
        country: str,
        position: Position,
        attributes: Attributes,
        potential: int,
        preferred_foot: str = "prawa",
        height_cm: int = 180,
        weight_kg: int = 75,
    ) -> None:
        if not (1 <= potential <= 99):
            raise ValueError("potential musi być w zakresie 1-99")

        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.country = country
        self.position = position
        self.attributes = attributes
        self.potential = potential
        self.preferred_foot = preferred_foot
        self.height_cm = height_cm
        self.weight_kg = weight_kg

        # Punkt 33: forma zmienia się mecz do meczu.
        self.form = 70
        # Punkt 10: kondycja spada z meczami/treningiem, wpływa na ryzyko kontuzji.
        self.condition = 100
        # Punkt 11: aktualna kontuzja (None = zdrowy).
        self.current_injury: Injury | None = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def ovr(self) -> int:
        """OVR liczone na bieżąco z atrybutów — nigdy nie jest przechowywane
        jako osobna, niezsynchronizowana liczba."""
        return calculate_ovr(self.attributes, self.position)

    @property
    def is_injured(self) -> bool:
        return self.current_injury is not None and not self.current_injury.is_healed

    def play_match(self, minutes: int) -> None:
        """
        Rejestruje udział w meczu — obniża kondycję proporcjonalnie do
        rozegranych minut (punkt 10 Game Planu).
        """
        if self.is_injured:
            raise RuntimeError(f"{self.full_name} jest kontuzjowany i nie może grać")

        fatigue_cost = round((minutes / 90) * 18)
        self.condition = _clamp(self.condition - fatigue_cost)

    def rest(self, days: int = 1) -> None:
        """Regeneracja kondycji między meczami/treningami."""
        recovery = 6 * days
        self.condition = _clamp(self.condition + recovery)

    def apply_form_change(self, delta: int) -> None:
        """Zmienia formę np. po dobrym/słabym meczu (punkt 33)."""
        self.form = _clamp(self.form + delta)

    def set_injury(self, injury: Injury) -> None:
        self.current_injury = injury

    def advance_week(self) -> None:
        """Przesuwa leczenie kontuzji o tydzień, jeśli zawodnik jest kontuzjowany."""
        if self.current_injury is not None:
            self.current_injury.advance_week()
            if self.current_injury.is_healed:
                self.current_injury = None

    def __repr__(self) -> str:
        status = f", KONTUZJA ({self.current_injury.name})" if self.is_injured else ""
        return (
            f"<Player {self.full_name} ({self.position.value}), "
            f"{self.age} lat, OVR {self.ovr}, potencjał {self.potential}{status}>"
        )
