# FPS Football Player — Football Engine

Nowy silnik gry (career mode piłkarski), budowany od zera zgodnie z
Game Planem 1.0. Frontend (HTML/CSS/JS) i backend (ten silnik, Python)
komunikują się przez API — na tym etapie API jeszcze nie istnieje,
bo Etap 1 to czysto logika świata.

## Status: Etap 5 — świat ✅ (Etapy 1-4 ✅)

Zbudowane w tym etapie:

- `football_engine/world/` — `Club`, `League`: podstawowe jednostki świata.
- `football_engine/season/fixtures.py` — generator prawdziwego terminarza
  (podwójny "każdy z każdym", metoda circle), zamiast losowania kolejnego meczu.
- `football_engine/match/simulation.py` — statystyczna symulacja wyniku meczu
  (rozkład Poissona, siła drużyny + przewaga własnego boiska).
- `football_engine/season/season_engine.py` — `SeasonEngine`: spina terminarz,
  symulację meczów i tabelę; pozwala rozgrywać sezon kolejka-po-kolejce
  (Tryb 1/2) albo od razu do końca (Tryb 3), bez losowania wyniku sezonu z góry.
- `football_engine/season/standings.py` — budowanie i wypisywanie tabeli ligowej.
- `football_engine/time_engine.py` — `GameCalendar`: sezon + numer kolejki.

Zbudowane w Etapie 2:

- `football_engine/career/position.py` — `Position` (12 pozycji) + grupy pozycji.
- `football_engine/career/attributes.py` — `Attributes` (19 umiejętności) i `calculate_ovr()`
  liczące OVR jako ważoną średnią zależną od pozycji (napastnik ≠ obrońca).
- `football_engine/career/player.py` — `Player`: tożsamość, atrybuty, OVR (zawsze
  liczone na bieżąco), potencjał, forma, kondycja, kontuzja.
- `football_engine/career/injury.py` — typy kontuzji + ryzyko rosnące wraz ze
  spadkiem kondycji (nie czysto losowe zdarzenie w tle).
- `football_engine/career/training.py` — 5 kategorii treningu (technika, fizyczny,
  strzelecki, taktyczny, regeneracja), każda rusza konkretne atrybuty.
- `football_engine/career/development.py` — rozwój sezonowy: szybki wzrost do 23
  lat (tym szybszy, im większa "przestrzeń" do potencjału), plateau 24-29,
  spadek od 30 (szybszy po 33).

Uruchomienie demo:

```bash
python demo.py             # Etap 1: sezon ligowy
python demo_player.py      # Etap 2: zawodnik — trening, mecze, kontuzje, rozwój
python demo_club.py        # Etap 3: skład, trener, rywalizacja o pozycję
python demo_transfers.py   # Etap 4: okna, AI klubów, negocjacje, wypożyczenia
python demo_world.py       # Etap 5: wiele lig, awanse/spadki, ewolucja siły klubów
```

Zbudowane w Etapie 5:

- `football_engine/world/league_system.py` — `LeagueSystem`: piramida lig w
  obrębie kraju (tier 0 = najwyższy poziom), `apply_promotion_relegation()`
  przenosi kluby między sąsiednimi poziomami na podstawie końcowej tabeli.
- `football_engine/world/world_engine.py` — `WorldEngine`: rozgrywa sezon we
  WSZYSTKICH ligach naraz, stosuje awanse/spadki, przelicza siłę każdego
  klubu z jego składu (punkt 60 — siła klubu ewoluuje, nie jest sztywna) i
  automatycznie przechodzi do kolejnego sezonu z nowym terminarzem.
- AI transferowe z Etapu 4 działa teraz na całym systemie lig na raz
  (`WorldEngine.run_transfer_window()`), nie tylko w obrębie jednej ligi.

Zbudowane w Etapie 4:

- `football_engine/time_engine.py` — `GameCalendar` rozszerzony o realną datę
  (nie tylko sezon+kolejka), potrzebną pod okna transferowe.
- `football_engine/transfer/window.py` — okna: letnie (1 lipca-31 sierpnia),
  zimowe (1-31 stycznia); poza nimi transfery są zamknięte.
- `football_engine/transfer/valuation.py` — `estimate_market_value()`: wycena
  z OVR (wykładniczo), wieku (szczyt ~24-26 lat) i premii za potencjał.
- `football_engine/transfer/offer.py` — `negotiate_transfer()`: oferta ->
  kontrpropozycja -> akceptacja/zerwanie (do 3 rund), `execute_transfer()`.
- `football_engine/transfer/ai.py` — `identify_club_needs()` (braki w składzie
  ORAZ starzejący się liderzy pozycji), `find_transfer_target()` (wiek 18-27,
  w budżecie), `run_transfer_window()` spinający to w jedną rundę AI.
- `football_engine/transfer/loan.py` — wypożyczenia z opcjonalnym wykupem,
  zawodnik wraca do klubu macierzystego po zakończeniu okresu.
- `football_engine/world/club.py` — dodane `transfer_budget`.

Zbudowane w Etapie 3:

- `football_engine/club/manager.py` — `Manager`: preferencje (młodzi/doświadczeni/
  balanced) i osobny słownik zaufania per zawodnik — niezależny od OVR.
- `football_engine/club/squad.py` — `selection_score()` (OVR + forma + kondycja +
  zaufanie + preferencja trenera), `select_matchday_squad()` (11 + ławka + poza
  kadrą per pozycja formacji), `describe_position_battle()` — komunikat medialny
  o rywalizacji o miejsce w składzie.
- `football_engine/world/club.py` — rozszerzony o `squad`, `manager`,
  `recalculate_strength_from_squad()` (siła klubu wyliczana ze składu, zamiast
  ustawiana ręcznie jak w Etapie 1).

## Świadome uproszczenia Etapu 1 (i gdzie zostaną rozbudowane)

- Klub ma jedną liczbę `strength` zamiast pełnego składu zawodników —
  realny skład i wyliczanie siły z zawodników dojdzie w **Etapie 2** (Zawodnik).
- Mecz jest wynikiem statystycznym (Poisson), a nie akcja-po-akcji —
  interaktywny match engine z decyzjami gracza (pkt 30-32 Game Planu)
  dojdzie w **Etapie 6**, korzystając z tych samych klubów/lig.
- Terminarz nadal obsługuje tylko parzystą liczbę klubów w lidze — obsługa
  "wolnego losu" (bye) dla lig nieparzystych jeszcze nie została dodana
  (nie okazała się potrzebna do Etapu 5, wraca jako zaległość).
- ~~Czas to sezon + numer kolejki, bez konkretnych dat~~ — naprawione w
  Etapie 4: `GameCalendar` ma teraz realną datę.

## Świadome uproszczenia Etapu 5

- Trener klubu (Etap 3) nie jest jeszcze automatycznie zmieniany przez AI po
  słabym sezonie/spadku (punkt 59 planu wspomina o tym szerzej) — Manager
  pozostaje przypisany ręcznie; rotacja trenerów przez AI to naturalne
  rozszerzenie `WorldEngine`.
- `WorldEngine.simulate_full_season()` NIE wywołuje jeszcze sezonowego
  rozwoju zawodników (Etap 2) — wymaga to śledzenia minut rozegranych przez
  każdego zawodnika w symulowanych meczach, co dojdzie razem z pełną
  integracją warstwy kariery gracza nad silnikiem świata.
- Import `Club`/`League` w kilku modułach (`season/fixtures.py`,
  `season/standings.py`, `match/simulation.py`) jest teraz pod `TYPE_CHECKING`
  — to konieczne, żeby `football_engine.world` (który od Etapu 5 importuje
  `WorldEngine`, a ten z kolei `SeasonEngine`) nie tworzył cyklu importów.
  Zasada na przyszłość: moduł potrzebujący cudzej klasy WYŁĄCZNIE do
  podpowiedzi typów importuje ją pod `TYPE_CHECKING`, nie na starcie pliku.

## Roadmapa (zgodnie z Game Planem, punkt 66)

1. ✅ Silnik: czas + sezony + mecze + tabela
2. ✅ Zawodnik: OVR + atrybuty + forma + kondycja + kontuzje
3. ✅ Klub: skład + trener + rywalizacja + pierwszy skład
4. ✅ Transfery: okna + AI + oferty + negocjacje + wypożyczenia
5. ✅ Świat: inne ligi + transfery + awanse/spadki
6. ✅ Puchary: Puchar Polski + Liga Europy/Konferencji + Liga Mistrzów
7. ✅ Reprezentacja: U19 → U21 → senior → EURO → MŚ
8. ✅ UI: responsywny mobile frontend + PWA manifest + JSON API pod Capacitor
9. ✅ System zapisu: wersjonowany pełny zapis kariery do JSON
10. ✅ Polish: newsy + efekty UI/audio manifest + balans

## Struktura projektu

```
football_engine/
├── __init__.py
├── time_engine.py          # GameCalendar
├── world/
│   ├── club.py               # Club
│   ├── league.py              # League
│   ├── league_system.py        # LeagueSystem, apply_promotion_relegation
│   └── world_engine.py          # WorldEngine
├── match/
│   └── simulation.py          # simulate_match (Poisson)
├── season/
│   ├── fixtures.py             # generate_double_round_robin
│   ├── standings.py            # build_table, print_table
│   └── season_engine.py        # SeasonEngine
├── career/
│   ├── position.py              # Position, PositionGroup
│   ├── attributes.py            # Attributes, calculate_ovr
│   ├── player.py                 # Player
│   ├── injury.py                 # Injury, check_for_injury
│   ├── training.py               # TrainingFocus, train
│   └── development.py            # apply_season_development
├── club/
│   ├── manager.py                 # Manager, ManagerPreference
│   └── squad.py                   # selection_score, select_matchday_squad, describe_position_battle
└── transfer/
    ├── window.py                   # TransferWindow, is_window_open, describe_window_status
    ├── valuation.py                # estimate_market_value
    ├── offer.py                    # negotiate_transfer, execute_transfer
    ├── ai.py                       # identify_club_needs, find_transfer_target, run_transfer_window
    └── loan.py                     # create_loan, end_loan, exercise_buy_option
demo.py             # Etap 1
demo_player.py      # Etap 2
demo_club.py         # Etap 3
demo_transfers.py    # Etap 4
demo_world.py        # Etap 5
```

Zero zewnętrznych zależności na tym etapie — czysta biblioteka standardowa
Pythona. Flask (backend API pod frontend) dojdzie razem z pierwszym etapem,
który faktycznie potrzebuje komunikacji z frontendem.


# Etapy 6–10 — wersja ukończona 6.0

Dodano:
- **Puchary**: Puchar Polski oraz moduł rozgrywek europejskich (LM/LE/LK), losowanie i drabinka.
- **Reprezentacja**: U19, U21 i senior, selekcja po wieku/kraju, mecze i obsługa turniejów EURO/MŚ.
- **AAA Mobile UI**: responsywny frontend w `web/`, manifest PWA i gotową warstwę pod Capacitor; frontend komunikuje się z backendem przez JSON API.
- **System zapisu**: wersjonowany pełny zapis świata, klubów, składów, zawodników i kalendarza w JSON.
- **Polish**: newsy, efekty UI/audio manifest, balans siły oraz kontroler `CareerGame` spinający sezon.
- **Stabilność**: terminarz obsługuje nieparzystą liczbę klubów przez `bye`; dodano testy regresyjne.

## Uruchomienie wersji ukończonej

```bash
python -m unittest discover -s tests -v
python server.py
```

Następnie otwórz `http://127.0.0.1:8080/web/`.

Projekt nadal nie wymaga zewnętrznych paczek Pythona. Backend korzysta wyłącznie ze standardowej biblioteki, więc można go później bez zmiany logiki opakować w Flask/FastAPI albo podłączyć bezpośrednio do Capacitor.


## Uruchomienie na Render

Projekt jest przygotowany do wdrożenia jako Render Web Service. W repozytorium znajdują się `render.yaml`, `Procfile`, `requirements.txt` i `runtime.txt`.

### Opcja A — Blueprint
1. Wgraj projekt do GitHub.
2. W Render wybierz **New → Blueprint** i wskaż repozytorium.
3. Render odczyta `render.yaml` i uruchomi usługę.

### Opcja B — ręcznie
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `python server.py`
- Health Check Path: `/api/health`

Po deploymencie otwórz publiczny adres Render i wejdź na `/web/`. API zdrowia powinno zwracać JSON pod `/api/health`.

> Uwaga: system plików Render dla standardowej usługi webowej nie jest trwałym miejscem na docelowe save'y. `career_save.json` jest obecnie zapisywany lokalnie przez proces. Do trwałych zapisów produkcyjnych należy później podłączyć bazę danych lub persistent disk.
