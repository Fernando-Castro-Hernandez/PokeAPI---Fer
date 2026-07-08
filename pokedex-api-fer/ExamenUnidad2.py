from fastapi import FastAPI, HTTPException, status, Query, Header
from pydantic import BaseModel, Field
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from typing import List, Optional
import os
import json

app = FastAPI(title="Examen Unidad 2 - Biblioteca de Libros")
ARCHIVO_DB  = "library.json"

# Definimos la SECRET KEY
SECRET_KEY = "321"


#Función 1. Leer el archivo y cargarlo a la RAM (DESERIALIZAR)
def cargar_biblioteca() -> dict:
    if not os.path.exists(ARCHIVO_DB):
        return {}

    # Guardian y Portal para abrir un archivo en disco duro
    with open(ARCHIVO_DB, "r", encoding= "utf-8") as f:
        datos_texto = json.load(f)
        # Conversión de seguridad: JSON convierte ID´s a str
        # Los regresamos a int (1...2...3...)
        return {int(k):v for k,v in datos_texto.items()}

# Toma los cambios de la RAM y los guarda en el JSON deldisco duro
def guardar_biblioteca(biblioteca_actualizada: dict):
    with open(ARCHIVO_DB, "w", encoding = "utf-8") as f:
        json.dump(biblioteca_actualizada, f, ensure_ascii=False, indent=4)



# Uso de BaseModel para VAlIDAR
class Libro(BaseModel):
    id: int
    titulo: str
    autor: str
    editorial: str
    genero: List[str] = Field(min_items= 1, max_items= 4)
    categoria: str
    fecha_de_publicacion: str

# Libro parcial
class LibroParcial(BaseModel):
    id: int | None
    titulo: str | None
    autor: str | None
    editorial: str | None
    genero: List[str] | None = Field(default=None, min_items=1, max_items=4)
    categoria: str | None
    fecha_de_publicacion: str | None


# Endpoint GET General: Búsqueda y Paginación
@app.get("/libro/catalogo")
def obtener_todos_los_libros_por_catalogo(
        genero: str = None,
        autor: str = None,
        page: int = Query(default=1),
        size: int = Query(default=3)
):
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=400,
            detail="Los parámetros 'page' y 'size' deben ser mayores o iguales a 1"
        )

    biblioteca_local = cargar_biblioteca()

    # 2. Base de datos completa
    resultados = biblioteca_local

    if genero:
        genero_existe = any(genero.capitalize() in p["genero"] for p in biblioteca_local.values())
        if not genero_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Libro con genero {genero.capitalize()} en la Biblioteca..."
            )
        resultados = {id: p for id, p in resultados.items() if genero.capitalize() in p["genero"]}

    if autor:
        autor_existe = any(autor.lower() == p["autor"].lower() for p in biblioteca_local.values())
        if not autor_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Libro con la autor '{autor}' en la PokéDex..."
            )
        resultados = {id: p for id, p in resultados.items() if autor.lower() == p["autor"].lower()}

    if not resultados:
        mensaje_error = "No se encontraron los Libros en la Biblioteca"
        if genero:
            mensaje_error += f" de genero {genero.capitalize()}"
        if autor:
            mensaje_error += f" con autor '{autor.capitalize()}'"
        raise HTTPException(
            status_code=404,
            detail=f"{mensaje_error} en la biblioteca..."
        )
    # CAPA 2: PAGINACIÓN
    # Convertir diccionario a lista para poder paginarla
    biblioteca_en_lista = list(resultados.items())

    # Aplicar el Slicing y volvemos a empaquetar como diccionario
    resultados_paginados = dict(biblioteca_en_lista[ (page - 1) * size : page * size ])

    # Devolvemos los METADATOS y la información final
    return {
        "message"  : "successful",
        "total_de_concidencias"  : len(resultados),
        "tamanio_de_pagina"  : size,
        "pagina"  : page,
        "resultado"  : resultados_paginados
    }


# Endpoint GET Especifico: Búsqueda por ID
@app.get("/Libro/{libro_id}")
def get_all_books_by_id(libro_id: int):
    # CARGAR del disco
    biblioteca_local = cargar_biblioteca()

    if libro_id not in biblioteca_local:
        raise HTTPException(status_code=404, detail=f"Este Libro con el ID# {libro_id} no existe en la Biblioteca", headers={"X-Error": "NO ENCONTRADO"})
    return biblioteca_local[libro_id]

# Endpoint POST: Creación de Registros
@app.post("/libro", status_code=HTTP_201_CREATED)
def registrar_nuevo_libro(nuevo_libro: Libro, x_api_key: Optional[str] = Header(None)):

    if x_api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acceso Denegado para registrar un nuevo Libro"
        )

    # Cargamos la data actual del archivo
    biblioteca_local = cargar_biblioteca()
    nuevo_id = nuevo_libro.id

    if nuevo_id in biblioteca_local:
        raise  HTTPException(
            status_code=400,
            detail= f"ID {nuevo_id} ya existe en la biblioteca, el libro es {biblioteca_local[nuevo_id]['titulo'] }",
            headers={"X-Error": "Ya existe en la biblioteca"}
        )
    # Si el nuevo_id es nuevo, REGISTRALO en la pokedex del disco duro
    biblioteca_local[nuevo_id] = nuevo_libro.model_dump(exclude={"id"})

    # Guardamos los cambios en el disco duro (PERSISTENCIA SEGURA)
    guardar_biblioteca(biblioteca_local)

    return {
        "mensaje" : f" Nuevo Libro Registrado con el ID #{nuevo_id} y Nombre: {nuevo_libro.titulo}",
        "datos" : biblioteca_local[nuevo_id]
    }

# Endpoints PUT y PATCH: Actualización de Datos
@app.put("/Libro/{libro_id}", status_code=HTTP_200_OK)
def actualizar_libro_completo(libro_id: int, libro_actualizado: Libro, x_api_key: Optional[str] = Header(None)):

    biblioteca_local = cargar_biblioteca()

    if x_api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acceso Denegado para actualizar un Libro"
        )

    #Validar que el pokemon exista en la PokeDex
    if libro_id not in biblioteca_local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡NO existe ningun libro con el ID{libro_id} en la biblioteca!"
        )
    # 2. Reemplazar los datos viejos con el JSON nuevo comleto
    biblioteca_local[libro_id] = libro_actualizado.model_dump()

    guardar_biblioteca(biblioteca_local)
    # 3. Devolver un mensaje de actualización
    return {
        "mensaje" : "Libro actualizado correctamente",
        "datos" : biblioteca_local[libro_id]
    }

@app.patch("/libro/{libro_id}", status_code=HTTP_200_OK)
def actualizar_libro_parcial(libro_id: int, libro_parcial: LibroParcial, x_api_key: Optional[str] = Header(None)):
    biblioteca_local = cargar_biblioteca()

    if x_api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acceso Denegado para registrar un nuevo Libro"
        )

    libro_local = cargar_biblioteca()

    #Validar que el pokemon exista en la PokeDex
    if libro_id not in libro_local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡NO existe ningun libro con el ID{libro_id} en la Biblioteca!"
        )
    # 2. Extraer úbicamente los datos a actualizar
    # .model_dump(exclude_unset=True)  Para ignorar los campos vacios
    datos_a_actualizar = libro_parcial.model_dump(exclude_unset=True)

    # 3. Actualizar SÓLO las llaves que llegaron a datos_a_actualizar
    for llave, valor in datos_a_actualizar.items():
        libro_local[libro_id][llave] = valor

    guardar_biblioteca(libro_local)
    # 4. Devolver un mensaje de actualización
    return {
        "mensaje" : "Actualizacion parcial completada",
        "datos" : biblioteca_local[libro_id]
    }

# Endpoint DELETE: Eliminación de Registros
@app.delete("/Libro/{libro_id}", status_code=HTTP_200_OK)
def eliminar_libro(libro_id : int, x_api_key: Optional[str] = Header(None)):

    if x_api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acceso denegado eliminar registro"
        )

    # CARGAR
    biblioteca_local = cargar_biblioteca()

    # Validar
    if libro_id not in biblioteca_local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡NO existe ningun Libro con el ID {libro_id} en la biblioteca!"
        )

    # 2. Extraer y borrar el Pokémon de la PokeDex usando .pop()
    libro_eliminado = biblioteca_local.pop(libro_id)
    nombre = libro_eliminado['titulo']
    # Guardamos
    guardar_biblioteca(biblioteca_local)

    return {
        "mensaje" : f"Liberacion de {nombre}  completada. ¡Adiós!",
    }







