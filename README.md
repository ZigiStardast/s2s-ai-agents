# AI agenti u akciji

Ovo je kompletan početni repozitorijum za dvodnevnu univerzitetsku radionicu o AI agentima. Kroz mali izmišljeni univerzitetski sistem CampusHub studenti polaze od običnog DSPy programa, dodaju Python funkcije kao alate, a zatim prave jedan jednostavan DSPy ReAct agent koji istražuje bug koristeći samo bezbedne alate za čitanje.

Najvažnija razlika radionice je:

> U modularnom pipeline-u programer određuje redosled koraka. Kod agenta programer zadaje cilj, alate i granice, a agent dinamički bira sledeću akciju.

## Preduslovi

- Python 3.11 ili 3.12
- osnovno poznavanje Python-a i komandne linije
- za live režim: OpenRouter API ključ

Radionica može da se prati i bez ključa u `mock` režimu. Mock režim je deterministička simulacija petlje, a ne pravi AI agent.

## Instalacija — Windows PowerShell

```powershell
git clone <URL-REPOZITORIJUMA>
cd ai-agenti-u-akciji
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Ako PowerShell blokira aktivaciju, pokrenite PowerShell kao korisnik i izvršite `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, pa ponovite aktivaciju.

## Instalacija — macOS/Linux

```bash
git clone <URL-REPOZITORIJUMA>
cd ai-agenti-u-akciji
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

`.env` je lokalni tekstualni fajl sa podešavanjima i tajnama koji Python učitava pri pokretanju; ne commit-ujte ga.

## OpenRouter podešavanje

1. Napravite nalog i API ključ na [OpenRouter](https://openrouter.ai/).
2. Otvorite `.env` i unesite ključ:

```dotenv
OPENROUTER_API_KEY=ovde_unesite_svoj_kljuc
OPENROUTER_MODEL=openrouter/free
AGENT_MODE=live
```

Model nije hard-kodiran u programu. `openrouter/free` je zgodan podrazumevani router, ali se dostupnost i besplatni limiti menjaju. Instruktor treba da testira izabrani model neposredno pre radionice. Drugi model se bira promenom samo vrednosti `OPENROUTER_MODEL`, na primer `google/gemini-2.0-flash-exp:free` ako je tada dostupan.

Nikada ne stavljajte pravi API ključ u Python fajl, screenshot, commit ili javni repozitorijum.

## Prvo pokretanje

Proverite da su lokalni alati ispravni:

```bash
python -m pytest -q
```

Pokrenite mock režim bez API ključa:

```bash
python -m src.main --scenario booking_bug --mock
```

Isto preko `.env` promenljive:

```bash
# macOS/Linux
AGENT_MODE=mock python -m src.main --scenario booking_bug

# Windows PowerShell
$env:AGENT_MODE="mock"
python -m src.main --scenario booking_bug
```

Pokrenite mali DSPy primer (zahteva live podešavanje i API ključ):

```bash
python examples/01_basic_dspy.py
```

Pokrenite agenta nad izabranim scenarijem:

```bash
python -m src.main --scenario booking_bug
python -m src.main --scenario duplicate_booking --review
python -m src.main --scenario booking_bug --mock --propose
```

Za detalje o grešci dodajte `--debug`. Za ručne provere OpenRouter-a koristite:

```bash
python scripts/smoke_test_openrouter.py
python scripts/smoke_test_react.py
```

Ove smoke testove ne pokreće pytest jer troše realne API pozive.

## Struktura

```text
src/                 kratki kod radionice
examples/            koraci od Predict-a do ReAct-a
demo_projects/       dva mala CampusHub scenarija
exercises/           zadaci za studente
instructor/          plan, beleške, rešenja i troubleshooting
tests/               deterministički testovi bez API-ja
```

## Česte greške

- `OPENROUTER_API_KEY is missing`: proverite da `.env` postoji i da ste pokrenuli komandu iz korena repozitorijuma.
- `401`: ključ je pogrešan, istekao ili ima razmake oko vrednosti.
- `429`: besplatni model je privremeno ograničen; pokušajte kasnije, izaberite drugi model ili koristite `AGENT_MODE=mock`.
- nema modela: proverite aktuelan naziv modela na OpenRouter-u.
- ReAct dosegne `max_iters`: agent nije stigao do zaključka; pokrenite ponovo ili u nastavnoj vežbi pažljivo povećajte limit na najviše 4.
- `pytest` nije pronađen: aktivirajte `.venv` i pokrenite `python -m pip install -r requirements.txt`.

Detaljniji odgovori su u [instructor/TROUBLESHOOTING.md](instructor/TROUBLESHOOTING.md).

## Cilj radionice

Student treba da ume da pokaže: SIGNATURE → TOOLS → REACT → INPUT → RESULT. Alat je obična Python funkcija koju je agentu dozvoljeno da pozove; model bira akciju, a Python izvršava alat. Veća autonomija nije automatski bolja — dobri agenti imaju jasne granice.
