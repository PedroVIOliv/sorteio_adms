from flask import Flask, render_template, jsonify
import random
import requests
import time
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Lista de membros do grupo e administradores atuais
MEMBROS = [
    "Alexandre", "Arthur Faria", "Arthur The Smiths", "Arthur Roraima",
    "Bernardo", "Catatau", "Fabio", "Raichu", "Sailor",
    "Luis Afonso", "Miguel saboroso", "Phasma", "Sann",
    "Rodka", "Sora", "Pedro Veloso", "Vitor Legaer"
]

# Define o bloco alvo, com valor padrão se não estiver no .env
TARGET_BLOCK_HEIGHT = int(os.getenv("TARGET_BLOCK_HEIGHT", 700000))

# Marca o tempo inicial do programa
start_time = time.time()

# Obtém a altura atual do bloco pela API do Blockstream
def get_current_block_height():
    try:
        response = requests.get("https://blockstream.info/api/blocks/tip/height")
        response.raise_for_status()
        return int(response.text)
    except Exception:
        return None

# Simula a altura do bloco para teste, ativando o bloco alvo após 10s
def debug_get_current_block_height():
    return TARGET_BLOCK_HEIGHT if time.time() - start_time > 10 else TARGET_BLOCK_HEIGHT - 1

# Obtém o hash de um bloco específico
def get_block_hash(block_height):
    try:
        response = requests.get(f"https://blockstream.info/api/block-height/{block_height}")
        response.raise_for_status()
        return response.text.strip()
    except Exception:
        return None

# Rota principal que renderiza a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota que retorna o status do sorteio em formato JSON
@app.route('/status.json')
def status_json():
    current_height = get_current_block_height()
    elegiveis = [m for m in MEMBROS]
    adms_selecionados = []
    status = "Aguardando o bloco alvo..."
    block_hash = None

    # Sorteia novos administradores se o bloco alvo for alcançado
    if current_height and current_height >= TARGET_BLOCK_HEIGHT:
        block_hash = get_block_hash(TARGET_BLOCK_HEIGHT)
        if block_hash:
            # Usa o hash do bloco como semente para a seleção aleatória
            random.seed(int(block_hash, 16))
            adms_selecionados = random.sample(elegiveis, 2)
            status = "Bloco alcançado!"

    # Monta a resposta JSON com os dados do sorteio
    return jsonify({
        "bloco_alvo": TARGET_BLOCK_HEIGHT,
        "altura_atual": current_height,
        "hash": block_hash,
        "status": status,
        "adms_selecionados": adms_selecionados,
        "elegiveis": elegiveis
    })

# Inicia o servidor no modo de depuração
if __name__ == "__main__":
    app.run(debug=True)
