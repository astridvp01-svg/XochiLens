from fastapi import FastAPI, UploadFile, File, HTTPException
import json
import os

app = FastAPI(title="XochiLens - Sistema Experto Puebla")

DATA_PATH = "species_data.json"

def load_species():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/")
def read_root():
    return {"mensaje": "API de XochiLens activa"}

@app.post("/analizar-especie/")
async def analizar_especie(file: UploadFile = File(...)):
    species_list = load_species()
    match_result = {
        "especie_detectada": species_list[0] if species_list else {},
        "porcentaje_similitud": 82.5,
        "estado_ambiental": "Óptimo"
    }
    similitud = match_result["porcentaje_similitud"]
    
    if 50.0 <= similitud < 75.0:
        return {
            "alerta": "Especie fuera del catálogo núcleo o similitud baja; consulte con un biólogo local.",
            "sugerencias": species_list[:3]
        }
    return {
        "resultado": "Éxito",
        "ficha_tecnica": match_result["especie_detectada"],
        "similitud": f"{similitud}%"
    }