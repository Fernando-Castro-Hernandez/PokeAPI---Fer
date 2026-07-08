# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Student project (Programación Aplicada course) with two independent FastAPI apps living in `pokedex-api-fer/`:

- `main.py` — Pokédex API (`pokedex.json` as its data file)
- `ExamenUnidad2.py` — Library/books API (`library.json` as its data file)

They don't share code; each app duplicates the same load/save/CRUD pattern. Code, comments, and route/field names are in Spanish — keep that convention when editing.

## Running the apps

There is no requirements.txt; dependencies (fastapi, uvicorn, requests) are installed in the committed-style venv at `pokedex-api-fer/venv` (Python 3.13).

Run from inside `pokedex-api-fer/` — the JSON data files are opened with relative paths, so the working directory matters:

```powershell
cd pokedex-api-fer
.\venv\Scripts\uvicorn main:app --reload          # Pokédex API
.\venv\Scripts\uvicorn ExamenUnidad2:app --reload # Library API
```

Interactive docs at `http://127.0.0.1:8000/docs`. There are no tests or linters configured.

## Architecture

Both apps follow the same pattern:

- **Persistence**: a plain JSON file on disk. `cargar_*()` deserializes it into a dict (converting keys back from `str` to `int` — JSON stringifies dict keys, and all lookups assume `int` IDs) and `guardar_*()` writes the whole dict back. Every endpoint that touches data reloads the file first.
- **Validation**: Pydantic `BaseModel` pairs — a full model (`Pokemon` / `Libro`) for POST/PUT and a `*Parcial` model with all-optional fields for PATCH (using `model_dump(exclude_unset=True)`).
- **Auth**: write endpoints (POST/PUT/PATCH/DELETE) check the `X-API-Key` header against a hardcoded `SECRET_KEY` (`"panamericano"` in main.py, `"321"` in ExamenUnidad2.py) and return 401 on mismatch.
- **Filtering + pagination**: GET catalog endpoints filter by attribute (tipo/habilidad or genero/autor), 404 when no match, then paginate via dict→list slicing (limit/offset or page/size).

Quirks to be aware of in `main.py`:

- There is a large hardcoded `pokedex` dict (151 Gen-1 entries) alongside the JSON file. Most endpoints use `cargar_pokedex()` (the file), but PUT (`actualizar_pokemon_completo`) and the `/pokemon/catalogo` endpoint still operate on the in-memory dict, so their changes don't persist and can disagree with the file.
- Route casing/naming is inconsistent (`/Pokemons/{id}` vs `/pokemons` vs `/pokemon/{id}`); FastAPI routes are case-sensitive.
- `/investigar/{nombre}` calls the external PokeAPI (https://pokeapi.co) with `requests` and maps the response into the `Pokemon` model (nivel is randomized).
