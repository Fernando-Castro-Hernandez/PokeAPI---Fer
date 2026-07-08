# Pokédex API 

Proyecto de la materia **Programación Aplicada** (3er cuatrimestre). Es una API REST construida con **FastAPI** que implementa el ciclo CRUD completo sobre una Pokédex de la primera generación (Kanto), con persistencia en archivos JSON.

El repositorio contiene dos aplicaciones independientes dentro de `pokedex-api-fer/`:

| Archivo | Aplicación | Datos |
|---|---|---|
| `main.py` | Pokédex API (151 Pokémon de Kanto) | `pokedex.json` |
| `ExamenUnidad2.py` | Biblioteca de Libros (Examen Unidad 2) | `library.json` |

## Tecnologías

- Python 3.13
- FastAPI + Uvicorn
- Pydantic (validación de modelos)
- Requests (consumo de la [PokeAPI](https://pokeapi.co) externa)

## Cómo ejecutar

Las dependencias ya están instaladas en el entorno virtual `pokedex-api-fer/venv`. Es importante ejecutar desde la carpeta `pokedex-api-fer/`, porque los archivos JSON se abren con rutas relativas:

```powershell
cd pokedex-api-fer
.\venv\Scripts\uvicorn main:app --reload          # Pokédex API
.\venv\Scripts\uvicorn ExamenUnidad2:app --reload # Biblioteca (Examen Unidad 2)
```

Con el servidor corriendo, la documentación interactiva (Swagger UI) queda disponible en:

- http://127.0.0.1:8000/docs

## Endpoints principales (Pokédex API)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/Pokemons/{pokemon_id}` | Obtener un Pokémon por su ID (path parameter) |
| GET | `/pokemons` | Listar con filtros `tipo` y `habilidad`, paginación `limit`/`offset` |
| GET | `/pokemon/catalogo` | Catálogo con filtros y paginación `page`/`size` |
| POST | `/pokemon/{pokemon_id}` | Registrar un nuevo Pokémon 🔒 |
| PUT | `/pokemon/{pokemon_id}` | Actualización completa de un Pokémon |
| PATCH | `/pokemon/{pokemon_id}` | Actualización parcial (solo los campos enviados) |
| DELETE | `/pokemon/{pokemon_id}` | Liberar (eliminar) un Pokémon 🔒 |
| GET | `/investigar/{nombre}` | Consulta la PokeAPI externa y devuelve un resumen |

🔒 = requiere el header `X-API-Key` con la clave secreta; sin ella responde `401 Unauthorized`.

Notas:

- Los iniciales en su forma base (Bulbasaur, Charmander y Squirtle — IDs 1, 4 y 7) no se pueden liberar (`403 Forbidden`).
- Los filtros que no encuentran coincidencias responden `404` con un mensaje descriptivo.

## Endpoints de la Biblioteca (ExamenUnidad2.py)

CRUD equivalente sobre libros: `GET /libro/catalogo` (filtros por `genero` y `autor`, paginación `page`/`size`), `GET /Libro/{libro_id}`, `POST /libro`, `PUT /Libro/{libro_id}`, `PATCH /libro/{libro_id}` y `DELETE /Libro/{libro_id}`. Todas las operaciones de escritura requieren el header `X-API-Key`.

## Conceptos practicados

- Path parameters y query parameters (con validación `Query(ge=1)`)
- Modelos Pydantic completos y parciales (`exclude_unset=True` para PATCH)
- Persistencia: serialización/deserialización JSON con conversión de llaves `str` → `int`
- Manejo de errores con `HTTPException` (400, 401, 403, 404) y headers personalizados
- Autenticación simple por header (`X-API-Key`)
- Consumo de una API externa con `requests`

## Autor

Fernando Castro Hernández
