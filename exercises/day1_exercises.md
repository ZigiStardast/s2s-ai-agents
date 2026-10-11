# Dan 1 — od programa do agenta

## Vežba A: alati bez AI-ja

U `examples/02_tools_without_ai.py` pokrenite svaki alat ručno. Zapišite šta vraćaju `list_files`, `read_file`, `run_tests` i `search_logs`.

Pitanje: da li je ijedan od ovih alata sam po sebi „agent“? Zašto ne?

## Vežba B: promenite dostupne alate

U `src/agent.py` privremeno uklonite `search_logs` iz liste alata. Pokrenite mock ili live primer. Da li agent i dalje može da napravi zaključak? Koji dokaz mu nedostaje?

## Vežba C: opisi alata

Promenite docstring funkcije `read_file` u nejasan opis. Ponovo pokrenite live agenta i posmatrajte da li se izbor alata menja. Objasnite zašto su ime, potpis i docstring važni.

## Vežba D: granica iteracija

Promenite `max_iters=3` na `max_iters=4`, ali ne više. Uporedite trajanje i execution trace.
