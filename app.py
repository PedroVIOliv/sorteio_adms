from flask import Flask, render_template, jsonify
import random
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MEMBROS = [
    "Alexandre", "Arthur Faria", "Arthur The Smiths", "Arthur Roraima",
    "Bernardo", "Catatau", "Fabio", "Raichu", "Sailor",
    "Luis Afonso", "Miguel saboroso", "Phasma", "Sann",
    "Rodka", "Sora", "Pedro Veloso", "Vitor Legaer"
]
ADMS_ATUAIS = ["Pedro Veloso", "Vitor Legaer"]
TARGET_BLOCK_HEIGHT = int(os.getenv("TARGET_BLOCK_HEIGHT", 700000))

start_time = time.time()

def get_current_block_height():
    try:
        response = requests.get("https://blockstream.info/api/blocks/tip/height")
        response.raise_for_status()
        return int(response.text)
    except Exception as e:
        return None

def debug_get_current_block_height():
    """Simula a altura do bloco para teste.
       Depois de 10s de app rodando, passa a dizer que o bloco chegou."""
    if time.time() - start_time > 10:
        return TARGET_BLOCK_HEIGHT
    else:
        return TARGET_BLOCK_HEIGHT - 1

def get_block_hash(block_height):
    try:
        url = f"https://blockstream.info/api/block-height/{block_height}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status.json')
def status_json():
    current_height = get_current_block_height()
    elegiveis = [m for m in MEMBROS if m not in ADMS_ATUAIS]
    adms_selecionados = []
    status = "Aguardando o bloco alvo..."
    block_hash = None
    if current_height and current_height >= TARGET_BLOCK_HEIGHT:
        block_hash = get_block_hash(TARGET_BLOCK_HEIGHT)
        if block_hash:
            seed = int(block_hash, 16)
            random.seed(seed)
            adms_selecionados = random.sample(elegiveis, 2)
            status = "Bloco alcançado!"

    data = {
        "bloco_alvo": TARGET_BLOCK_HEIGHT,
        "altura_atual": current_height if current_height else None,
        "hash": block_hash if block_hash else None,
        "status": status,
        "adms_selecionados": adms_selecionados,
        "elegiveis": elegiveis
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
