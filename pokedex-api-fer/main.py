from fastapi import FastAPI, HTTPException, status, Query, Header
from pydantic import BaseModel, Field
from typing import List, Optional
import os
import json
import random
import requests

app = FastAPI(title="Pokédex API de Fer")
ARCHIVO_DB  = "pokedex.json"

# Definimos la SECRET KEY
SECRET_KEY = "panamericano"


#Función 1. Leer el archivo y cargarlo a la RAM (DESERIALIZAR)
def cargar_pokedex() -> dict:  # Obligar a la funcion a devolver un diccionario de python
    """Almacena el arcvhivo en un diccionario en python"""
    # Si el archivo no existe, devolvemos diccionario vaicio
    if not os.path.exists(ARCHIVO_DB):
        return {}

    # Guardian y Portal para abrir un archivo en disco duro
    with open(ARCHIVO_DB, "r", encoding= "utf-8") as f:
        datos_texto = json.load(f)
        # Conversión de seguridad: JSON convierte ID´s a str
        # Los regresamos a int (1...2...3...)
        return {int(k):v for k,v in datos_texto.items()}

# Toma los cambios de la RAM y los guarda en el JSON deldisco duro
def guardar_pokedex(pokedex_actualizada: dict):
    # Guardian para acceder al archivo
    with open(ARCHIVO_DB, "w", encoding = "utf-8") as f:
        json.dump(pokedex_actualizada, f, ensure_ascii=False, indent=4)




pokedex = {
    # --- GENERACIÓN 1 (Kanto) ---
    1: {"nombre": "Bulbasaur", "tipo": ["Planta", "Veneno"], "nivel": 5, "habilidad": "Espesura", "ataque": 49, "defensa": 49, "movimientos": ["Placaje", "Latigazo", "Drenadoras", "Hoja Afilada"]},
    2: {"nombre": "Ivysaur", "tipo": ["Planta", "Veneno"], "nivel": 16, "habilidad": "Espesura", "ataque": 62, "defensa": 63, "movimientos": ["Placaje", "Latigazo", "Drenadoras", "Hoja Afilada"]},
    3: {"nombre": "Venusaur", "tipo": ["Planta", "Veneno"], "nivel": 32, "habilidad": "Espesura", "ataque": 82, "defensa": 83, "movimientos": ["Latigazo", "Drenadoras", "Hoja Afilada", "Rayo Solar"]},
    4: {"nombre": "Charmander", "tipo": ["Fuego"], "nivel": 5, "habilidad": "Mar Llamas", "ataque": 52, "defensa": 43, "movimientos": ["Arañazo", "Gruñido", "Ascuas", "Furia Dragón"]},
    5: {"nombre": "Charmeleon", "tipo": ["Fuego"], "nivel": 16, "habilidad": "Mar Llamas", "ataque": 64, "defensa": 58, "movimientos": ["Arañazo", "Ascuas", "Furia Dragón", "Lanzallamas"]},
    6: {"nombre": "Charizard", "tipo": ["Fuego", "Volador"], "nivel": 36, "habilidad": "Mar Llamas", "ataque": 84, "defensa": 78, "movimientos": ["Ascuas", "Furia Dragón", "Lanzallamas", "Vuelo"]},
    7: {"nombre": "Squirtle", "tipo": ["Agua"], "nivel": 5, "habilidad": "Torrente", "ataque": 48, "defensa": 65, "movimientos": ["Placaje", "Refugio", "Pistola Agua", "Giro Rápido"]},
    8: {"nombre": "Wartortle", "tipo": ["Agua"], "nivel": 16, "habilidad": "Torrente", "ataque": 63, "defensa": 80, "movimientos": ["Placaje", "Pistola Agua", "Giro Rápido", "Mordisco"]},
    9: {"nombre": "Blastoise", "tipo": ["Agua"], "nivel": 36, "habilidad": "Torrente", "ataque": 83, "defensa": 100, "movimientos": ["Pistola Agua", "Giro Rápido", "Mordisco", "Hidrobomba"]},
    10: {"nombre": "Caterpie", "tipo": ["Bicho"], "nivel": 5, "habilidad": "Polvo Escudo", "ataque": 30, "defensa": 35, "movimientos": ["Placaje", "Disparo Demora", "Picadura", "Fortaleza"]},
    11: {"nombre": "Metapod", "tipo": ["Bicho"], "nivel": 7, "habilidad": "Mudar", "ataque": 20, "defensa": 55, "movimientos": ["Fortaleza", "Placaje", "Disparo Demora", "Picadura"]},
    12: {"nombre": "Butterfree", "tipo": ["Bicho", "Volador"], "nivel": 10, "habilidad": "Ojo Compuesto", "ataque": 45, "defensa": 50, "movimientos": ["Confusión", "Polvo Veneno", "Paralizador", "Tornado"]},
    13: {"nombre": "Weedle", "tipo": ["Bicho", "Veneno"], "nivel": 5, "habilidad": "Polvo Escudo", "ataque": 35, "defensa": 30, "movimientos": ["Picotazo Venenoso", "Disparo Demora", "Picadura", "Fortaleza"]},
    14: {"nombre": "Kakuna", "tipo": ["Bicho", "Veneno"], "nivel": 7, "habilidad": "Mudar", "ataque": 25, "defensa": 50, "movimientos": ["Fortaleza", "Picotazo Venenoso", "Disparo Demora", "Picadura"]},
    15: {"nombre": "Beedrill", "tipo": ["Bicho", "Veneno"], "nivel": 10, "habilidad": "Enjambre", "ataque": 90, "defensa": 40, "movimientos": ["Ataque Furia", "Furia Bilial", "Doble Ataque", "Pin Misil"]},
    16: {"nombre": "Pidgey", "tipo": ["Normal", "Volador"], "nivel": 5, "habilidad": "Vista Lince", "ataque": 45, "defensa": 40, "movimientos": ["Placaje", "Ataque Arena", "Tornado", "Ataque Rápido"]},
    17: {"nombre": "Pidgeotto", "tipo": ["Normal", "Volador"], "nivel": 18, "habilidad": "Vista Lince", "ataque": 60, "defensa": 55, "movimientos": ["Placaje", "Tornado", "Ataque Rápido", "Remolino"]},
    18: {"nombre": "Pidgeot", "tipo": ["Normal", "Volador"], "nivel": 36, "habilidad": "Vista Lince", "ataque": 80, "defensa": 75, "movimientos": ["Tornado", "Ataque Rápido", "Remolino", "Ataque Ala"]},
    19: {"nombre": "Rattata", "tipo": ["Normal"], "nivel": 5, "habilidad": "Fuga", "ataque": 56, "defensa": 35, "movimientos": ["Placaje", "Látigo", "Ataque Rápido", "Hipercolmillo"]},
    20: {"nombre": "Raticate", "tipo": ["Normal"], "nivel": 20, "habilidad": "Fuga", "ataque": 81, "defensa": 60, "movimientos": ["Ataque Rápido", "Hipercolmillo", "Foco Energía", "Tratamiento"]},
    21: {"nombre": "Spearow", "tipo": ["Normal", "Volador"], "nivel": 5, "habilidad": "Vista Lince", "ataque": 60, "defensa": 30, "movimientos": ["Picotazo", "Gruñido", "Malicioso", "Ataque Furia"]},
    22: {"nombre": "Fearow", "tipo": ["Normal", "Volador"], "nivel": 20, "habilidad": "Vista Lince", "ataque": 90, "defensa": 65, "movimientos": ["Picotazo", "Ataque Furia", "Persecución", "Pico Taladro"]},
    23: {"nombre": "Ekans", "tipo": ["Veneno"], "nivel": 5, "habilidad": "Intimidación", "ataque": 60, "defensa": 44, "movimientos": ["Envoltura", "Malicioso", "Picotazo Venenoso", "Mordisco"]},
    24: {"nombre": "Arbok", "tipo": ["Veneno"], "nivel": 22, "habilidad": "Intimidación", "ataque": 85, "defensa": 69, "movimientos": ["Picotazo Venenoso", "Mordisco", "Deslumbrar", "Bomba Ácido"]},
    25: {"nombre": "Pikachu", "tipo": ["Eléctrico"], "nivel": 5, "habilidad": "Elec. Estática", "ataque": 55, "defensa": 40, "movimientos": ["Impactrueno", "Gruñido", "Onda Trueno", "Ataque Rápido"]},
    26: {"nombre": "Raichu", "tipo": ["Eléctrico"], "nivel": "Piedra Trueno", "habilidad": "Elec. Estática", "ataque": 90, "defensa": 55, "movimientos": ["Impactrueno", "Onda Trueno", "Ataque Rápido", "Rayo"]},
    27: {"nombre": "Sandshrew", "tipo": ["Tierra"], "nivel": 5, "habilidad": "Velo Arena", "ataque": 75, "defensa": 85, "movimientos": ["Arañazo", "Defensa Rizo", "Ataque Arena", "Magnitud"]},
    28: {"nombre": "Sandslash", "tipo": ["Tierra"], "nivel": 22, "habilidad": "Velo Arena", "ataque": 100, "defensa": 110, "movimientos": ["Ataque Arena", "Magnitud", "Cuchillada", "Terremoto"]},
    29: {"nombre": "Nidoran♀", "tipo": ["Veneno"], "nivel": 5, "habilidad": "Punto Tóxico", "ataque": 47, "defensa": 52, "movimientos": ["Gruñido", "Arañazo", "Picotazo Venenoso", "Mordisco"]},
    30: {"nombre": "Nidorina", "tipo": ["Veneno"], "nivel": 16, "habilidad": "Punto Tóxico", "ataque": 62, "defensa": 67, "movimientos": ["Gruñido", "Arañazo", "Picotazo Venenoso", "Mordisco"]},
    31: {"nombre": "Nidoqueen", "tipo": ["Veneno", "Tierra"], "nivel": "Piedra Lunar", "habilidad": "Punto Tóxico", "ataque": 92, "defensa": 87, "movimientos": ["Picotazo Venenoso", "Mordisco", "Golpe Cuerpo", "Tierra Viva"]},
    32: {"nombre": "Nidoran♂", "tipo": ["Veneno"], "nivel": 5, "habilidad": "Punto Tóxico", "ataque": 57, "defensa": 40, "movimientos": ["Malicioso", "Picotazo", "Picotazo Venenoso", "Cornada"]},
    33: {"nombre": "Nidorino", "tipo": ["Veneno"], "nivel": 16, "habilidad": "Punto Tóxico", "ataque": 72, "defensa": 57, "movimientos": ["Malicioso", "Picotazo", "Picotazo Venenoso", "Cornada"]},
    34: {"nombre": "Nidoking", "tipo": ["Veneno", "Tierra"], "nivel": "Piedra Lunar", "habilidad": "Punto Tóxico", "ataque": 102, "defensa": 77, "movimientos": ["Picotazo Venenoso", "Cornada", "Ayuda", "Tierra Viva"]},
    35: {"nombre": "Clefairy", "tipo": ["Hada"], "nivel": 5, "habilidad": "Gran Encanto", "ataque": 45, "defensa": 48, "movimientos": ["Destructor", "Gruñido", "Canto", "Metrónomo"]},
    36: {"nombre": "Clefable", "tipo": ["Hada"], "nivel": "Piedra Lunar", "habilidad": "Gran Encanto", "ataque": 70, "defensa": 73, "movimientos": ["Canto", "Metrónomo", "Fuerza Lunar", "Amortiguador"]},
    37: {"nombre": "Vulpix", "tipo": ["Fuego"], "nivel": 5, "habilidad": "Absorbe Fuego", "ataque": 41, "defensa": 40, "movimientos": ["Ascuas", "Látigo", "Anulación", "Giro Fuego"]},
    38: {"nombre": "Ninetales", "tipo": ["Fuego"], "nivel": "Piedra Fuego", "habilidad": "Absorbe Fuego", "ataque": 76, "defensa": 75, "movimientos": ["Anulación", "Giro Fuego", "Lanzallamas", "Fuego Fatuo"]},
    39: {"nombre": "Jigglypuff", "tipo": ["Normal", "Hada"], "nivel": 5, "habilidad": "Gran Encanto", "ataque": 45, "defensa": 20, "movimientos": ["Canto", "Destructor", "Defensa Rizo", "Doblebofetón"]},
    40: {"nombre": "Wigglytuff", "tipo": ["Normal", "Hada"], "nivel": "Piedra Lunar", "habilidad": "Gran Encanto", "ataque": 70, "defensa": 45, "movimientos": ["Canto", "Doblebofetón", "Vozarrón", "Carantoña"]},
    41: {"nombre": "Zubat", "tipo": ["Veneno", "Volador"], "nivel": 5, "habilidad": "Foco Interno", "ataque": 45, "defensa": 35, "movimientos": ["Chupavidas", "Supersónico", "Impresión", "Mordisco"]},
    42: {"nombre": "Golbat", "tipo": ["Veneno", "Volador"], "nivel": 22, "habilidad": "Foco Interno", "ataque": 80, "defensa": 70, "movimientos": ["Supersónico", "Impresión", "Mordisco", "Ataque Ala"]},
    43: {"nombre": "Oddish", "tipo": ["Planta", "Veneno"], "nivel": 5, "habilidad": "Clorofila", "ataque": 50, "defensa": 55, "movimientos": ["Absorber", "Crecimiento", "Polvo Veneno", "Ácido"]},
    44: {"nombre": "Gloom", "tipo": ["Planta", "Veneno"], "nivel": 21, "habilidad": "Clorofila", "ataque": 65, "defensa": 70, "movimientos": ["Polvo Veneno", "Ácido", "Paralizador", "Somnífero"]},
    45: {"nombre": "Vileplume", "tipo": ["Planta", "Veneno"], "nivel": "Piedra Hoja", "habilidad": "Clorofila", "ataque": 80, "defensa": 85, "movimientos": ["Somnífero", "Megaagotar", "Bomba Germen", "Danza Pétalo"]},
    46: {"nombre": "Paras", "tipo": ["Bicho", "Planta"], "nivel": 5, "habilidad": "Efecto Espora", "ataque": 70, "defensa": 55, "movimientos": ["Arañazo", "Paralizador", "Absorber", "Cuchillada"]},
    47: {"nombre": "Parasect", "tipo": ["Bicho", "Planta"], "nivel": 24, "habilidad": "Efecto Espora", "ataque": 95, "defensa": 80, "movimientos": ["Absorber", "Cuchillada", "Espora", "Tijera X"]},
    48: {"nombre": "Venonat", "tipo": ["Bicho", "Veneno"], "nivel": 5, "habilidad": "Polvo Escudo", "ataque": 55, "defensa": 50, "movimientos": ["Placaje", "Anulación", "Supersónico", "Confusión"]},
    49: {"nombre": "Venomoth", "tipo": ["Bicho", "Veneno"], "nivel": 31, "habilidad": "Polvo Escudo", "ataque": 65, "defensa": 60, "movimientos": ["Supersónico", "Confusión", "Rayo Psicodélico", "Zumbido"]},
    50: {"nombre": "Diglett", "tipo": ["Tierra"], "nivel": 5, "habilidad": "Trampa Arena", "ataque": 55, "defensa": 25, "movimientos": ["Arañazo", "Gruñido", "Disparo Lodo", "Magnitud"]},
    51: {"nombre": "Dugtrio", "tipo": ["Tierra"], "nivel": 26, "habilidad": "Trampa Arena", "ataque": 100, "defensa": 50, "movimientos": ["Disparo Lodo", "Magnitud", "Acuchillar", "Terremoto"]},
    52: {"nombre": "Meowth", "tipo": ["Normal"], "nivel": 5, "habilidad": "Recogida", "ataque": 45, "defensa": 35, "movimientos": ["Arañazo", "Gruñido", "Mordisco", "Día de Pago"]},
    53: {"nombre": "Persian", "tipo": ["Normal"], "nivel": 28, "habilidad": "Flexibilidad", "ataque": 70, "defensa": 60, "movimientos": ["Mordisco", "Día de Pago", "Sorpresa", "Acuchillar"]},
    54: {"nombre": "Psyduck", "tipo": ["Agua"], "nivel": 5, "habilidad": "Humedad", "ataque": 52, "defensa": 48, "movimientos": ["Arañazo", "Látigo", "Pistola Agua", "Confusión"]},
    55: {"nombre": "Golduck", "tipo": ["Agua"], "nivel": 33, "habilidad": "Humedad", "ataque": 82, "defensa": 78, "movimientos": ["Pistola Agua", "Confusión", "Furia", "Hidrobomba"]},
    56: {"nombre": "Mankey", "tipo": ["Lucha"], "nivel": 5, "habilidad": "Espíritu Vital", "ataque": 80, "defensa": 35, "movimientos": ["Arañazo", "Malicioso", "Patada Baja", "Golpe Karate"]},
    57: {"nombre": "Primeape", "tipo": ["Lucha"], "nivel": 28, "habilidad": "Espíritu Vital", "ataque": 105, "defensa": 60, "movimientos": ["Patada Baja", "Golpe Karate", "Furia", "Tajo Cruzado"]},
    58: {"nombre": "Growlithe", "tipo": ["Fuego"], "nivel": 5, "habilidad": "Intimidación", "ataque": 70, "defensa": 45, "movimientos": ["Mordisco", "Rugido", "Ascuas", "Rueda Fuego"]},
    59: {"nombre": "Arcanine", "tipo": ["Fuego"], "nivel": "Piedra Fuego", "habilidad": "Intimidación", "ataque": 110, "defensa": 80, "movimientos": ["Ascuas", "Rueda Fuego", "Velocidad", "Envite Ígneo"]},
    60: {"nombre": "Poliwag", "tipo": ["Agua"], "nivel": 5, "habilidad": "Absorbe Agua", "ataque": 50, "defensa": 40, "movimientos": ["Burbuja", "Hipnosis", "Pistola Agua", "Doblebofetón"]},
    61: {"nombre": "Poliwhirl", "tipo": ["Agua"], "nivel": 25, "habilidad": "Absorbe Agua", "ataque": 65, "defensa": 65, "movimientos": ["Hipnosis", "Pistola Agua", "Doblebofetón", "Disparo Lodo"]},
    62: {"nombre": "Poliwrath", "tipo": ["Agua", "Lucha"], "nivel": "Piedra Agua", "habilidad": "Absorbe Agua", "ataque": 95, "defensa": 95, "movimientos": ["Doblebofetón", "Disparo Lodo", "Sumisión", "Hidrobomba"]},
    63: {"nombre": "Abra", "tipo": ["Psíquico"], "nivel": 5, "habilidad": "Sincronía", "ataque": 20, "defensa": 15, "movimientos": ["Teletransporte", "Cinético", "Confusión", "Psíquico"]},
    64: {"nombre": "Kadabra", "tipo": ["Psíquico"], "nivel": 16, "habilidad": "Sincronía", "ataque": 35, "defensa": 30, "movimientos": ["Teletransporte", "Confusión", "Anulación", "Psicorrayo"]},
    65: {"nombre": "Alakazam", "tipo": ["Psíquico"], "nivel": "Intercambio", "habilidad": "Sincronía", "ataque": 50, "defensa": 45, "movimientos": ["Confusión", "Anulación", "Psicorrayo", "Psíquico"]},
    66: {"nombre": "Machop", "tipo": ["Lucha"], "nivel": 5, "habilidad": "Agallas", "ataque": 80, "defensa": 50, "movimientos": ["Patada Baja", "Malicioso", "Foco Energía", "Golpe Karate"]},
    67: {"nombre": "Machoke", "tipo": ["Lucha"], "nivel": 28, "habilidad": "Agallas", "ataque": 100, "defensa": 70, "movimientos": ["Foco Energía", "Golpe Karate", "Sísmico", "Tajo Cruzado"]},
    68: {"nombre": "Machamp", "tipo": ["Lucha"], "nivel": "Intercambio", "habilidad": "Agallas", "ataque": 130, "defensa": 80, "movimientos": ["Golpe Karate", "Sísmico", "Tajo Cruzado", "Puño Dinámico"]},
    69: {"nombre": "Bellsprout", "tipo": ["Planta", "Veneno"], "nivel": 5, "habilidad": "Clorofila", "ataque": 75, "defensa": 35, "movimientos": ["Látigo Cepa", "Crecimiento", "Polvo Veneno", "Ácido"]},
    70: {"nombre": "Weepinbell", "tipo": ["Planta", "Veneno"], "nivel": 21, "habilidad": "Clorofila", "ataque": 90, "defensa": 50, "movimientos": ["Crecimiento", "Polvo Veneno", "Ácido", "Hoja Afilada"]},
    71: {"nombre": "Victreebel", "tipo": ["Planta", "Veneno"], "nivel": "Piedra Hoja", "habilidad": "Clorofila", "ataque": 105, "defensa": 65, "movimientos": ["Ácido", "Hoja Afilada", "Bomba Germen", "Hoja Aguda"]},
    72: {"nombre": "Tentacool", "tipo": ["Agua", "Veneno"], "nivel": 5, "habilidad": "Cuerpo Puro", "ataque": 40, "defensa": 35, "movimientos": ["Picotazo Venenoso", "Supersónico", "Pistola Agua", "Constricción"]},
    73: {"nombre": "Tentacruel", "tipo": ["Agua", "Veneno"], "nivel": 30, "habilidad": "Cuerpo Puro", "ataque": 70, "defensa": 65, "movimientos": ["Supersónico", "Pistola Agua", "Constricción", "Hidrobomba"]},
    74: {"nombre": "Geodude", "tipo": ["Roca", "Tierra"], "nivel": 5, "habilidad": "Cabeza Roca", "ataque": 80, "defensa": 100, "movimientos": ["Placaje", "Defensa Rizo", "Lanzarrocas", "Magnitud"]},
    75: {"nombre": "Graveler", "tipo": ["Roca", "Tierra"], "nivel": 25, "habilidad": "Cabeza Roca", "ataque": 95, "defensa": 115, "movimientos": ["Defensa Rizo", "Lanzarrocas", "Magnitud", "Pedrada"]},
    76: {"nombre": "Golem", "tipo": ["Roca", "Tierra"], "nivel": "Intercambio", "habilidad": "Cabeza Roca", "ataque": 120, "defensa": 130, "movimientos": ["Lanzarrocas", "Magnitud", "Pedrada", "Terremoto"]},
    77: {"nombre": "Ponyta", "tipo": ["Fuego"], "nivel": 5, "habilidad": "Fuga", "ataque": 85, "defensa": 55, "movimientos": ["Placaje", "Gruñido", "Ascuas", "Giro Fuego"]},
    78: {"nombre": "Rapidash", "tipo": ["Fuego"], "nivel": 40, "habilidad": "Fuga", "ataque": 100, "defensa": 70, "movimientos": ["Ascuas", "Giro Fuego", "Pisotón", "Envite Ígneo"]},
    79: {"nombre": "Slowpoke", "tipo": ["Agua", "Psíquico"], "nivel": 5, "habilidad": "Despiste", "ataque": 65, "defensa": 65, "movimientos": ["Maldición", "Placaje", "Pistola Agua", "Confusión"]},
    80: {"nombre": "Slowbro", "tipo": ["Agua", "Psíquico"], "nivel": 37, "habilidad": "Despiste", "ataque": 75, "defensa": 110, "movimientos": ["Placaje", "Pistola Agua", "Confusión", "Amnesia"]},
    81: {"nombre": "Magnemite", "tipo": ["Eléctrico", "Acero"], "nivel": 5, "habilidad": "Imán", "ataque": 35, "defensa": 70, "movimientos": ["Impactrueno", "Supersónico", "Bomba Imán", "Chispa"]},
    82: {"nombre": "Magneton", "tipo": ["Eléctrico", "Acero"], "nivel": 30, "habilidad": "Imán", "ataque": 60, "defensa": 95, "movimientos": ["Supersónico", "Bomba Imán", "Chispa", "Foco Resplandor"]},
    83: {"nombre": "Farfetch'd", "tipo": ["Normal", "Volador"], "nivel": 5, "habilidad": "Vista Lince", "ataque": 90, "defensa": 55, "movimientos": ["Picotazo", "Ataque Arena", "Corte Furia", "Acuchillar"]},
    84: {"nombre": "Doduo", "tipo": ["Normal", "Volador"], "nivel": 5, "habilidad": "Fuga", "ataque": 85, "defensa": 45, "movimientos": ["Picotazo", "Gruñido", "Ataque Furia", "Pico Taladro"]},
    85: {"nombre": "Dodrio", "tipo": ["Normal", "Volador"], "nivel": 31, "habilidad": "Fuga", "ataque": 110, "defensa": 70, "movimientos": ["Gruñido", "Ataque Furia", "Pico Taladro", "Triataque"]},
    86: {"nombre": "Seel", "tipo": ["Agua"], "nivel": 5, "habilidad": "Sebo", "ataque": 45, "defensa": 55, "movimientos": ["Cabezazo", "Gruñido", "Pistola Agua", "Rayo Aurora"]},
    87: {"nombre": "Dewgong", "tipo": ["Agua", "Hielo"], "nivel": 34, "habilidad": "Sebo", "ataque": 70, "defensa": 80, "movimientos": ["Pistola Agua", "Rayo Aurora", "Acua Jet", "Rayo Hielo"]},
    88: {"nombre": "Grimer", "tipo": ["Veneno"], "nivel": 5, "habilidad": "Hedor", "ataque": 80, "defensa": 50, "movimientos": ["Destructor", "Gas Venenoso", "Residuos", "Lodo"]},
    89: {"nombre": "Muk", "tipo": ["Veneno"], "nivel": 38, "habilidad": "Hedor", "ataque": 105, "defensa": 75, "movimientos": ["Gas Venenoso", "Residuos", "Lodo", "Bomba Lodo"]},
    90: {"nombre": "Shellder", "tipo": ["Agua"], "nivel": 5, "habilidad": "Caparazón", "ataque": 65, "defensa": 100, "movimientos": ["Placaje", "Refugio", "Pistola Agua", "Clavo Icicle"]},
    91: {"nombre": "Cloyster", "tipo": ["Agua", "Hielo"], "nivel": "Piedra Agua", "habilidad": "Caparazón", "ataque": 95, "defensa": 180, "movimientos": ["Refugio", "Pistola Agua", "Púas", "Carámbano"]},
    92: {"nombre": "Gastly", "tipo": ["Fantasma", "Veneno"], "nivel": 5, "habilidad": "Levitación", "ataque": 35, "defensa": 30, "movimientos": ["Lengüetazo", "Hipnosis", "Tinieblas", "Infortunio"]},
    93: {"nombre": "Haunter", "tipo": ["Fantasma", "Veneno"], "nivel": 25, "habilidad": "Levitación", "ataque": 50, "defensa": 45, "movimientos": ["Hipnosis", "Tinieblas", "Puño Sombra", "Bola Sombra"]},
    94: {"nombre": "Gengar", "tipo": ["Fantasma", "Veneno"], "nivel": "Intercambio", "habilidad": "Levitación", "ataque": 65, "defensa": 60, "movimientos": ["Tinieblas", "Puño Sombra", "Bola Sombra", "Pesadilla"]},
    95: {"nombre": "Onix", "tipo": ["Roca", "Tierra"], "nivel": 5, "habilidad": "Cabeza Roca", "ataque": 45, "defensa": 160, "movimientos": ["Placaje", "Fortaleza", "Atadura", "Lanzarrocas"]},
    96: {"nombre": "Drowzee", "tipo": ["Psíquico"], "nivel": 5, "habilidad": "Insomnio", "ataque": 48, "defensa": 45, "movimientos": ["Destructor", "Hipnosis", "Anulación", "Confusión"]},
    97: {"nombre": "Hypno", "tipo": ["Psíquico"], "nivel": 26, "habilidad": "Insomnio", "ataque": 73, "defensa": 70, "movimientos": ["Hipnosis", "Anulación", "Confusión", "Psicorrayo"]},
    98: {"nombre": "Krabby", "tipo": ["Agua"], "nivel": 5, "habilidad": "Corte Fuerte", "ataque": 105, "defensa": 90, "movimientos": ["Burbuja", "Malicioso", "Agarre", "Martillazo"]},
    99: {"nombre": "Kingler", "tipo": ["Agua"], "nivel": 28, "habilidad": "Corte Fuerte", "ataque": 130, "defensa": 115, "movimientos": ["Malicioso", "Agarre", "Martillazo", "Tijera X"]},
    100: {"nombre": "Voltorb", "tipo": ["Eléctrico"], "nivel": 5, "habilidad": "Insonorizar", "ataque": 30, "defensa": 50, "movimientos": ["Placaje", "Chispa", "Carga", "Autodestrucción"]},
    101: {"nombre": "Electrode", "tipo": ["Eléctrico"], "nivel": 30, "habilidad": "Insonorizar", "ataque": 50, "defensa": 70, "movimientos": ["Chispa", "Carga", "Autodestrucción", "Explosión"]},
    102: {"nombre": "Exeggcute", "tipo": ["Planta", "Psíquico"], "nivel": 5, "habilidad": "Clorofila", "ataque": 40, "defensa": 80, "movimientos": ["Barrera", "Hipnosis", "Reflejo", "Confusion"]},
    103: {"nombre": "Exeggutor", "tipo": ["Planta", "Psíquico"], "nivel": "Piedra Hoja", "habilidad": "Clorofila", "ataque": 95, "defensa": 85, "movimientos": ["Hipnosis", "Reflejo", "Bomba Germen", "Psíquico"]},
    104: {"nombre": "Cubone", "tipo": ["Tierra"], "nivel": 5, "habilidad": "Cabeza Roca", "ataque": 50, "defensa": 95, "movimientos": ["Gruñido", "Hueso Palo", "Malicioso", "Bonemerang"]},
    105: {"nombre": "Marowak", "tipo": ["Tierra"], "nivel": 28, "habilidad": "Cabeza Roca", "ataque": 80, "defensa": 110, "movimientos": ["Hueso Palo", "Malicioso", "Bonemerang", "Falso-tortazo"]},
    106: {"nombre": "Hitmonlee", "tipo": ["Lucha"], "nivel": 20, "habilidad": "Flexibilidad", "ataque": 120, "defensa": 53, "movimientos": ["Patada Baja", "Foco Energía", "Patada Salto", "A Bocajarro"]},
    107: {"nombre": "Hitmonchan", "tipo": ["Lucha"], "nivel": 20, "habilidad": "Vista Lince", "ataque": 105, "defensa": 79, "movimientos": ["Puño Cometa", "Puño Fuego", "Puño Hielo", "Puño Trueno"]},
    108: {"nombre": "Lickitung", "tipo": ["Normal"], "nivel": 5, "habilidad": "Ritmo Propio", "ataque": 55, "defensa": 75, "movimientos": ["Lengüetazo", "Supersónico", "Pisotón", "Desenrrollar"]},
    109: {"nombre": "Koffing", "tipo": ["Veneno"], "nivel": 5, "habilidad": "Levitación", "ataque": 65, "defensa": 95, "movimientos": ["Placaje", "Smog", "Polución", "Autodestrucción"]},
    110: {"nombre": "Weezing", "tipo": ["Veneno"], "nivel": 35, "habilidad": "Levitación", "ataque": 90, "defensa": 120, "movimientos": ["Smog", "Polución", "Autodestrucción", "Bomba Lodo"]},
    111: {"nombre": "Rhyhorn", "tipo": ["Tierra", "Roca"], "nivel": 5, "habilidad": "Pararrayos", "ataque": 85, "defensa": 95, "movimientos": ["Cornada", "Malicioso", "Pisotón", "Pedrada"]},
    112: {"nombre": "Rhydon", "tipo": ["Tierra", "Roca"], "nivel": 42, "habilidad": "Pararrayos", "ataque": 130, "defensa": 120, "movimientos": ["Cornada", "Pisotón", "Pedrada", "Terremoto"]},
    113: {"nombre": "Chansey", "tipo": ["Normal"], "nivel": 5, "habilidad": "Cura Natural", "ataque": 5, "defensa": 5, "movimientos": ["Destructor", "Gruñido", "Amortiguador", "Doblebofetón"]},
    114: {"nombre": "Tangela", "tipo": ["Planta"], "nivel": 5, "habilidad": "Clorofila", "ataque": 55, "defensa": 115, "movimientos": ["Constricción", "Polvo Sueño", "Absorber", "Megaagotar"]},
    115: {"nombre": "Kangaskhan", "tipo": ["Normal"], "nivel": 5, "habilidad": "Madrugar", "ataque": 95, "defensa": 80, "movimientos": ["Mordisco", "Golpe Cuerpo", "Sorpresa", "Triturar"]},
    116: {"nombre": "Horsea", "tipo": ["Agua"], "nivel": 5, "habilidad": "Nado Rápido", "ataque": 40, "defensa": 70, "movimientos": ["Burbuja", "Pantalla Humo", "Pistola Agua", "Ciclón"]},
    117: {"nombre": "Seadra", "tipo": ["Agua"], "nivel": 32, "habilidad": "Punto Tóxico", "ataque": 65, "defensa": 95, "movimientos": ["Burbuja", "Pantalla Humo", "Pistola Agua", "Ciclón"]},
    118: {"nombre": "Goldeen", "tipo": ["Agua"], "nivel": 5, "habilidad": "Nado Rápido", "ataque": 67, "defensa": 60, "movimientos": ["Picotazo", "Supersónico", "Flail", "Cascada"]},
    119: {"nombre": "Seaking", "tipo": ["Agua"], "nivel": 33, "habilidad": "Nado Rápido", "ataque": 92, "defensa": 65, "movimientos": ["Supersónico", "Flail", "Cascada", "Perforador"]},
    120: {"nombre": "Staryu", "tipo": ["Agua"], "nivel": 5, "habilidad": "Iluminación", "ataque": 45, "defensa": 55, "movimientos": ["Placaje", "Pistola Agua", "Giro Rápido", "Recuperación"]},
    121: {"nombre": "Starmie", "tipo": ["Agua", "Psíquico"], "nivel": "Piedra Agua", "habilidad": "Iluminación", "ataque": 75, "defensa": 85, "movimientos": ["Pistola Agua", "Giro Rápido", "Recuperación", "Psíquico"]},
    122: {"nombre": "Mr. Mime", "tipo": ["Psíquico", "Hada"], "nivel": 5, "habilidad": "Insonorizar", "ataque": 45, "defensa": 65, "movimientos": ["Confusión", "Barrera", "Pantalla Luz", "Reflejo"]},
    123: {"nombre": "Scyther", "tipo": ["Bicho", "Volador"], "nivel": 5, "habilidad": "Enjambre", "ataque": 110, "defensa": 80, "movimientos": ["Ataque Rápido", "Malicioso", "Foco Energía", "Falso-tortazo"]},
    124: {"nombre": "Jynx", "tipo": ["Hielo", "Psíquico"], "nivel": 5, "habilidad": "Despiste", "ataque": 50, "defensa": 35, "movimientos": ["Lamedura", "Polvo Nieve", "Beso Amoroso", "Puño Hielo"]},
    125: {"nombre": "Electabuzz", "tipo": ["Eléctrico"], "nivel": 5, "habilidad": "Elec. Estática", "ataque": 83, "defensa": 57, "movimientos": ["Impactrueno", "Ataque Rápido", "Chispa", "Puño Trueno"]},
    126: {"nombre": "Magmar", "tipo": ["Fuego"], "nivel": 5, "habilidad": "Cuerpo Llama", "ataque": 95, "defensa": 57, "movimientos": ["Ascuas", "Pantalla Humo", "Giro Fuego", "Puño Fuego"]},
    127: {"nombre": "Pinsir", "tipo": ["Bicho"], "nivel": 5, "habilidad": "Corte Fuerte", "ataque": 125, "defensa": 100, "movimientos": ["Agarre", "Foco Energía", "Sumisión", "Guillotina"]},
    128: {"nombre": "Tauros", "tipo": ["Normal"], "nivel": 5, "habilidad": "Intimidación", "ataque": 100, "defensa": 95, "movimientos": ["Placaje", "Malicioso", "Cornada", "Golpe Cuerpo"]},
    129: {"nombre": "Magikarp", "tipo": ["Agua"], "nivel": 5, "habilidad": "Nado Rápido", "ataque": 10, "defensa": 55, "movimientos": ["Salpicadura", "Placaje", "Azote", "Bote"]},
    130: {"nombre": "Gyarados", "tipo": ["Agua", "Volador"], "nivel": 20, "habilidad": "Intimidación", "ataque": 125, "defensa": 79, "movimientos": ["Mordisco", "Furia Dragon", "Acua Cola", "Hiperrayo"]},
    131: {"nombre": "Lapras", "tipo": ["Agua", "Hielo"], "nivel": 5, "habilidad": "Absorbe Agua", "ataque": 85, "defensa": 80, "movimientos": ["Pistola Agua", "Canto", "Rayo Confuso", "Rayo Hielo"]},
    132: {"nombre": "Ditto", "tipo": ["Normal"], "nivel": 5, "habilidad": "Flexibilidad", "ataque": 48, "defensa": 48, "movimientos": ["Transformación", "Placaje", "Esquiva", "Copia"]},
    133: {"nombre": "Eevee", "tipo": ["Normal"], "nivel": 5, "habilidad": "Fuga", "ataque": 55, "defensa": 50, "movimientos": ["Placaje", "Látigo", "Ataque Rápido", "Mordisco"]},
    134: {"nombre": "Vaporeon", "tipo": ["Agua"], "nivel": "Piedra Agua", "habilidad": "Absorbe Agua", "ataque": 65, "defensa": 60, "movimientos": ["Placaje", "Pistola Agua", "Pisar Fondo", "Hidrobomba"]},
    135: {"nombre": "Jolteon", "tipo": ["Eléctrico"], "nivel": "Piedra Trueno", "habilidad": "Absorbe Elec", "ataque": 65, "defensa": 60, "movimientos": ["Impactrueno", "Ataque Rápido", "Doble Patada", "Rayo"]},
    136: {"nombre": "Flareon", "tipo": ["Fuego"], "nivel": "Piedra Fuego", "habilidad": "Absorbe Fuego", "ataque": 130, "defensa": 60, "movimientos": ["Ascuas", "Ataque Rápido", "Giro Fuego", "Lanzallamas"]},
    137: {"nombre": "Porygon", "tipo": ["Normal"], "nivel": 5, "habilidad": "Rastro", "ataque": 60, "defensa": 70, "movimientos": ["Conversión", "Placaje", "Psicorrayo", "Triataque"]},
    138: {"nombre": "Omanyte", "tipo": ["Roca", "Agua"], "nivel": 5, "habilidad": "Nado Rápido", "ataque": 40, "defensa": 100, "movimientos": ["Constricción", "Refugio", "Pistola Agua", "Pedrada"]},
    139: {"nombre": "Omastar", "tipo": ["Roca", "Agua"], "nivel": 40, "habilidad": "Nado Rápido", "ataque": 60, "defensa": 125, "movimientos": ["Constricción", "Pistola Agua", "Pedrada", "Púas Tóxicas"]},
    140: {"nombre": "Kabuto", "tipo": ["Roca", "Agua"], "nivel": 5, "habilidad": "Nado Rápido", "ataque": 80, "defensa": 90, "movimientos": ["Arañazo", "Fortaleza", "Absorber", "Disparo Lodo"]},
    141: {"nombre": "Kabutops", "tipo": ["Roca", "Agua"], "nivel": 40, "habilidad": "Nado Rápido", "ataque": 115, "defensa": 105, "movimientos": ["Absorber", "Disparo Lodo", "Cuchillada", "Tijera X"]},
    142: {"nombre": "Aerodactyl", "tipo": ["Roca", "Volador"], "nivel": 5, "habilidad": "Cabeza Roca", "ataque": 105, "defensa": 65, "movimientos": ["Mordisco", "Garraguda", "Ataque Ala", "Avalancha"]},
    143: {"nombre": "Snorlax", "tipo": ["Normal"], "nivel": 5, "habilidad": "Inmunidad", "ataque": 110, "defensa": 65, "movimientos": ["Placaje", "Defensa Rizo", "Amnesia", "Golpe Cuerpo"]},
    144: {"nombre": "Articuno", "tipo": ["Hielo", "Volador"], "nivel": 5, "habilidad": "Presión", "ataque": 85, "defensa": 100, "movimientos": ["Tornado", "Polvo Nieve", "Rayo Aurora", "Rayo Hielo"]},
    145: {"nombre": "Zapdos", "tipo": ["Eléctrico", "Volador"], "nivel": 5, "habilidad": "Presión", "ataque": 90, "defensa": 85, "movimientos": ["Tornado", "Impactrueno", "Pico Taladro", "Rayo"]},
    146: {"nombre": "Moltres", "tipo": ["Fuego", "Volador"], "nivel": 5, "habilidad": "Presión", "ataque": 100, "defensa": 90, "movimientos": ["Tornado", "Ascuas", "Ataque Ala", "Lanzallamas"]},
    147: {"nombre": "Dratini", "tipo": ["Dragón"], "nivel": 5, "habilidad": "Mudar", "ataque": 64, "defensa": 45, "movimientos": ["Constricción", "Malicioso", "Onda Trueno", "Furia Dragón"]},
    148: {"nombre": "Dragonair", "tipo": ["Dragón"], "nivel": 30, "habilidad": "Mudar", "ataque": 84, "defensa": 65, "movimientos": ["Onda Trueno", "Furia Dragón", "Portazo", "Acua Cola"]},
    149: {"nombre": "Dragonite", "tipo": ["Dragón", "Volador"], "nivel": 55, "habilidad": "Foco Interno", "ataque": 134, "defensa": 95, "movimientos": ["Furia Dragón", "Acua Cola", "Ataque Ala", "Enfado"]},
    150: {"nombre": "Mewtwo", "tipo": ["Psíquico"], "nivel": 5, "habilidad": "Presión", "ataque": 110, "defensa": 90, "movimientos": ["Confusión", "Rapidez", "Psicocorte", "Psíquico"]},
    151: {"nombre": "Mew", "tipo": ["Psíquico"], "nivel": 5, "habilidad": "Sincronía", "ataque": 100, "defensa": 100, "movimientos": ["Destructor", "Metrónomo", "Megaagotar", "Psíquico"]}
}

# Uso de BaseModel para VAlIDAR
# Pokemon completo
class Pokemon(BaseModel):
    id: int # Este campo en MUY IMPORTANTE
    nombre: str
    tipo: List[str]
    nivel: int
    habilidad: str
    movimientos: List[str] = Field(min_items= 1, max_items= 4)
    ataque: int
    defensa: int

# Pokemon parcial
class PokemonParcial(BaseModel):
    int: int | None
    nombre: str | None = None
    tipo: List[str] | None = None
    nivel: int | None = None
    habilidad: str | None = None
    movimientos: List[str] | None = Field(default=None, min_items=1, max_items=4)
    ataque: int | None = None
    defensa: int | None = None


@app.get("/Read Root")
def leer_root():
    return {"Message": "Pokédex API de Ferchito, Mi pokemonsito Fav es Kyogre" }

# @app.get("/Pokemons")
#def get_all_pokemons():
    return pokedex

#Buenas practicas especificar que hace la API
#Ejemplo de Path Parameter
@app.get("/Pokemons/{pokemon_id}")
def get_all_pokemon_by_id(pokemon_id: int):
    # 1. Cargar los datos reales del disco duro a la RAM

    # CARGAR del disco
    pokedex_local = cargar_pokedex()

    if pokemon_id not in pokedex_local:
        raise HTTPException(status_code=404, detail=f"Este Pokemonsito con el ID# {pokemon_id} no existe en la region", headers={"X-Error": "NO ENCONTRADO"})
    return pokedex_local[pokemon_id]

# Ejemplo de Query Parameter
@app.get("/pokemons") # 1. Añadimos Limit y Offset
def obtener_todos_los_pokemon(tipo: str = None, habilidad: str = None , limit: int = 5, offset: int = 0):
    # 2. Base de datos completa
    pokedex_real = cargar_pokedex()
    resultados = pokedex_real

    if tipo:
        tipo_existe = any(tipo.capitalize() in p["tipo"] for p in pokedex.values())
        if not tipo_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Pokémon de tipo {tipo.capitalize()} en la PokéDex..."
            )
        resultados = {id: p for id, p in resultados.items() if tipo.capitalize() in p["tipo"]}

    if habilidad:
        hab_existe = any(habilidad.lower() == p["habilidad"].lower() for p in pokedex.values())
        if not hab_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Pokémon con la habilidad '{habilidad}' en la PokéDex..."
            )
        resultados = {id: p for id, p in resultados.items() if habilidad.lower() == p["habilidad"].lower()}

    if not resultados:
        mensaje_error = "No se encontraron Pokémon"
        if tipo:
            mensaje_error += f" de tipo {tipo.capitalize()}"
        if habilidad:
            mensaje_error += f" con la habilidad '{habilidad}'"
        raise HTTPException(
            status_code=404,
            detail=f"{mensaje_error} en la PokéDex..."
        )
    # CAPA 2: PAGINACIÓN
    # Convertir diccionario a lista para poder paginarla
    pokedex_en_lista = list(resultados.items())

    # Aplicar el Slicing y volvemos a empaquetar como diccionario

    resultados_paginados = dict(pokedex_en_lista[offset : offset + limit])

    # Devolvemos los METADATOS y la información final
    return {
        "message"  : "successful",
        "total_de_concidencias"  : len(resultados),
        "limite_pagina"  : limit,
        "desplazamiento"  : offset,
        "resultado"  : resultados_paginados

    }

# Endopoint para REGISTRAR nuevo Pokemon = VERIFICAR
@app.post("/pokemon/{pokemon_id}")
def registrar_nuevo_pokemon(nuevo_pokemon: Pokemon, x_api_key: Optional[str] = Header(None)):

    if x_api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acceso Denegado para registrar un nuevo Pokemon"
        )

    # Cargamos la data actual del archivo
    pokedex_local = cargar_pokedex()
    nuevo_id = nuevo_pokemon.id

    if nuevo_id in pokedex_local:
        raise  HTTPException(
            status_code=400,
            detail= f"ID {pokemon_id} ya existe en la Pokedex, el pokemon es {pokedex_local[nuevo_id]['nombre'] }",
            headers={"X-Error": "Ya existe en la Pokedex"}
        )
    # Si el nuevo_id es nuevo, REGISTRALO en la pokedex del disco duro
    pokedex_local[nuevo_id] = nuevo_pokemon.model_dump(exclude={"id"})

    # Guardamos los cambios en el disco duro (PERSISTENCIA SEGURA)
    guardar_pokedex(pokedex_local)

    return {
        "mensaje" : f"¡Ya esta! Nuevo Pokemosn Registrado con el ID #{nuevo_id} y Nombre: {nuevo_pokemon.nombre}",
        "datos" : pokedex_local[nuevo_id]
    }

# Ciclo CRUD
# ENDPOINT para actualizar un Pokemon por completo (reemplazo total).
@app.put("/pokemon/{pokemon_id}")
def actualizar_pokemon_completo(pokemon_id: int, pokemon_actualizado: Pokemon):
    #Validar que el pokemon exista en la PokeDex
    if pokemon_id not in pokedex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡NO existe ningun pokemon con el ID{pokemon_id} en la Pokedex!"
        )
    # 2. Reemplazar los datos viejos con el JSON nuevo comleto
    pokedex[pokemon_id] = pokemon_actualizado.model_dump()

    # 3. Devolver un mensaje de actualización
    return {
        "mensaje" : "Pokemon actualizado correctamente",
        "datos" : pokedex[pokemon_id]
    }

    # ENDPOINT para actualizar un pokemon parcialmente
@app.patch("/pokemon/{pokemon_id}")
def actualizar_pokemon_parcial(pokemon_id: int, pokemon_parcial: PokemonParcial):
    pokedex_local = cargar_pokedex()


    #Validar que el pokemon exista en la PokeDex
    if pokemon_id not in pokedex_local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡NO existe ningun pokemon con el ID{pokemon_id} en la Pokedex!"
        )
    # 2. Extraer úbicamente los datos a actualizar
    # .model_dump(exclude_unset=True)  Para ignorar los campos vacios
    datos_a_actualizar = pokemon_parcial.model_dump(exclude_unset=True)

    # 3. Actualizar SÓLO las llaves que llegaron a datos_a_actualizar
    for llave, valor in datos_a_actualizar.items():
        pokedex_local[pokemon_id][llave] = valor

    guardar_pokedex(pokedex_local)
    # 4. Devolver un mensaje de actualización
    return {
        "mensaje" : "Actualizacion parcial completada",
        "datos" : pokedex[pokemon_id]
    }

# ENDPOINT para liberar (Eliminar) un pokemon en la PokeDex
@app.delete("/pokemon/{pokemon_id}")
def liberar_pokemon(pokemon_id : int, x_api_key: Optional[str] = Header(None)):

    if x_api_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acceso Denegado para lberar Pokemon"
        )

    # CARGAR
    pokedex_local = cargar_pokedex()

    # Validar que no se puedan eliminar los 3 pokemones principales en su forma base
    if pokemon_id in [1, 4, 7]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No puedes liberar al pokemon con ID#{pokemon_id} en la Pokedex!"
        )

    # Validar
    if pokemon_id not in pokedex_local:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡NO existe ningun pokemon con el ID {pokemon_id} en la Pokedex!"
        )

    # 2. Extraer y borrar el Pokémon de la PokeDex usando .pop()
    pokemon_liberado = pokedex_local.pop(pokemon_id)
    nombre = pokemon_liberado['nombre']
    # Guardamos
    guardar_pokedex(pokedex_local)

    return {
        "mensaje" : f"Liberacion de {nombre}  completada. ¡Adiós!",
    }

#Crear ENDPOINT que filtre por PAGE and SIZE
@app.get("/pokemon/catalogo")
def obtener_todos_los_pokkemon_por_catalogo(
        tipo: str = None,
        habilidad: str = None,
        page: int = Query(default=1, ge=1), # ge=1 significa "Greater than or Equal to 1" (Mayor o igual a 1)
        size: int = Query(default=3, ge=1)
):
    # 2. Base de datos completa
    resultados = pokedex

    if tipo:
        tipo_existe = any(tipo.capitalize() in p["tipo"] for p in pokedex.values())
        if not tipo_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Pokémon de tipo {tipo.capitalize()} en la PokéDex..."
            )
        resultados = {id: p for id, p in resultados.items() if tipo.capitalize() in p["tipo"]}

    if habilidad:
        hab_existe = any(habilidad.lower() == p["habilidad"].lower() for p in pokedex.values())
        if not hab_existe:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún Pokémon con la habilidad '{habilidad}' en la PokéDex..."
            )
        resultados = {id: p for id, p in resultados.items() if habilidad.lower() == p["habilidad"].lower()}

    if not resultados:
        mensaje_error = "No se encontraron Pokémon"
        if tipo:
            mensaje_error += f" de tipo {tipo.capitalize()}"
        if habilidad:
            mensaje_error += f" con la habilidad '{habilidad}'"
        raise HTTPException(
            status_code=404,
            detail=f"{mensaje_error} en la PokéDex..."
        )
    # CAPA 2: PAGINACIÓN
    # Convertir diccionario a lista para poder paginarla
    pokedex_en_lista = list(resultados.items())

    # Aplicar el Slicing y volvemos a empaquetar como diccionario
    resultados_paginados = dict(pokedex_en_lista[ (page - 1) * size : page * size ])

    # Devolvemos los METADATOS y la información final
    return {
        "message"  : "successful",
        "total_de_concidencias"  : len(resultados),
        "tamanio_de_pagina"  : size,
        "pagina"  : page,
        "resultado"  : resultados_paginados

    }

#Endpoint para extraer informacion de internet
@app.get("/investigar/{nombre}", response_model = Pokemon)
def investigar_pokemon_externo(nombre:str ):
    #1 Armar la URL apuntando al servidor(PokeApi)
    url_externa = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    #2 Nuestro servidor hace una llamada get hacia internet
    respuesta = requests.get(url_externa)
    #3  Verificar si el servidor externo nos devolvio un error 404
    if respuesta.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"No hay informacion de {nombre.capitalize()} en la PokeApi externa "
        )
    #4 Convertir a JSON
    datos = respuesta.json()

    tipos =[]
    for tipo in datos["types"]:
        tipos.append(tipo["type"]["name"])

    movimientos = []
    for movimiento in datos["moves"]:
        movimientos.append(movimiento["move"]["name"])

    #5 Extraemos solo lo que queremos del JSON gigante
    resumen = {
        "id" : datos["id"],
        "nombre" : datos["name"],
        "tipo" : tipos,
        "nivel" : random.randint(1,100),
        "habilidad" : datos["abilities"][0]["ability"]["name"],
        "movimientos" : movimientos[0:4],
        "ataque" : datos ["stats"][1]["base_stat"],
        "defensa" : datos ["stats"][2]["base_stat"]

    }
    return resumen





