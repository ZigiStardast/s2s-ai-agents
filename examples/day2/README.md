# Dan 2 — nezavisni primeri

Ovi primeri dopunjuju postojeći agent, ali ne menjaju CampusHub kod, alate, ReAct agent ili Reviewer.

## 1. Reviewer: dobar i loš dokaz

Pokretanje iz korena repozitorijuma:

```bash
python -m examples.day2.01_reviewer_comparison --offline
```

Za pravi DSPy Reviewer:

```bash
python -m examples.day2.01_reviewer_comparison
```

Live verzija zahteva API ključ. `--offline` je jasno označena simulacija i ne koristi LLM. Uspešan ispis prikazuje dva slučaja, očekivanje za diskusiju i stvarni verdict/feedback. Live model može da se ne složi sa očekivanjem.

Pitanja:

- Zašto prvi zaključak nema dovoljno dokaza?
- Koji deo drugog slučaja je proverljiv?
- Da li Reviewer popravlja nalaz ili ga samo ocenjuje?

Ako OpenRouter free model nije dostupan, koristite eksplicitni `--offline`.

## 2. Prompt injection u dokumentu

Pokretanje bez LLM-a:

```bash
python -m examples.day2.02_prompt_injection --offline
```

Pokretanje sa DSPy `Predict`:

```bash
python -m examples.day2.02_prompt_injection
```

Live verzija zahteva API ključ. Dokumenti u `data/` su fikcionalni i nepouzdani; ne pristupa se Slack-u, Confluence-u, credential-ima ili stvarnim sistemima. Model samo generiše tekstualni odgovor. Ne postoji automatsko izvršavanje privilegovanih radnji.

Pitanja:

- Ko je autor legitimnog zadatka, a ko je samo sadržaj dokumenta?
- Da li je model ignorisao ili sledio ubačenu instrukciju?
- Koju dodatnu granicu bismo želeli u pravom sistemu?

Ako API nije dostupan, koristite eksplicitni `--offline`; to je simulacija bez LLM-a.

## 3. Poređenje trajectory

```bash
python -m examples.day2.03_trajectory_comparison
```

Ne zahteva API ključ. Sve tri trajectory su kratki, izmišljeni primeri za razgovor, a ne snimljeni rezultati ReAct agenta. Uspešan ispis poredi tačnost, dokaze i nepotrebno ponavljanje alata.

Pitanja:

- Koji agent ima najbolju ravnotežu između cene i dokaza?
- Zašto je drugo pretraživanje istog loga nepotrebno?
- Da li brzina sama po sebi znači pouzdanost?

Ako nema API-ja, ovaj primer i dalje radi jer nema LLM poziv.

## 4. Human approval workflow

```bash
python -m examples.day2.04_human_approval_workflow
```

Kada program pita `[y/N]`, unesite `y` za odobrenje ili samo pritisnite Enter za odbijanje. Ovo je lokalna deterministička simulacija: ništa se ne šalje u Slack, ništa se ne upisuje u Confluence i nijedan fajl se ne menja.

Pitanja:

- Koji korak je zadržao čoveka u kontroli?
- Šta se dešava kada korisnik odbije predlog?
- Koje provere bi bile potrebne pre stvarne objave?

API ključ nije potreban. Primer je fallback za razgovor o dozvolama i granicama.
