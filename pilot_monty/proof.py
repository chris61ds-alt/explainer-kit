"""Monty Hall: exact enumeration + seeded simulation. Writes proof.json (single source of truth for the video)."""
import json, numpy as np
from fractions import Fraction
# exact: car uniformly in 3 doors, player picks uniformly, host opens a goat door (uniform if two available)
stay = switch = Fraction(0)
for car in range(3):
    for pick in range(3):
        p = Fraction(1, 9)
        goats = [d for d in range(3) if d != pick and d != car]
        for opened in goats:
            q = p / len(goats)
            other = [d for d in range(3) if d not in (pick, opened)][0]
            stay += q * (pick == car); switch += q * (other == car)
assert stay + switch == 1
# negative control: host opens a random unpicked door (may reveal car) → conditional on goat shown, 50/50
nc_stay = nc_switch = Fraction(0)
for car in range(3):
    for pick in range(3):
        for opened in [d for d in range(3) if d != pick]:
            q = Fraction(1, 9) * Fraction(1, 2)
            if opened == car: continue
            other = [d for d in range(3) if d not in (pick, opened)][0]
            nc_stay += q * (pick == car); nc_switch += q * (other == car)
SEED, N = 2026, 10_000
rng = np.random.default_rng(SEED)
car = rng.integers(0, 3, N); pick = rng.integers(0, 3, N); coin = rng.integers(0, 2, N)
opened = np.empty(N, int)
for i in range(N):
    goats = [d for d in range(3) if d != pick[i] and d != car[i]]
    opened[i] = goats[coin[i] % len(goats)]
other = 3 - pick - opened
stay_win = pick == car; switch_win = other == car
assert np.all(stay_win ^ switch_win)            # exactly one strategy wins every game
out = dict(exact=dict(stay=str(stay), switch=str(switch)),
           negative_control_ignorant_host=dict(stay=str(nc_stay / (nc_stay + nc_switch)), switch=str(nc_switch / (nc_stay + nc_switch))),
           simulation=dict(seed=SEED, n=N, stay_wins=int(stay_win.sum()), switch_wins=int(switch_win.sum())),
           order=switch_win.astype(int).tolist())
json.dump(out, open("proof.json", "w"))
print({k: v for k, v in out.items() if k != "order"})
