from flask import Flask, render_template, jsonify
import random
import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# The order we want to show on the page:
ORIGINAL_LIST = [
    "Alexandre", "Arthur Faria", "Arthur The Smiths", "Arthur Roraima",
    "Bernardo", "Catatau", "Fabio", "Raichu", "Sailor",
    "Luis Afonso", "Miguel saboroso", "Phasma", "Sann",
    "Rodka", "Sora", "Pedro Veloso", "Vitor Legaer"
]

TARGET_BLOCK_HEIGHT = int(os.getenv("TARGET_BLOCK_HEIGHT", 700000))
ELIMINATION_INTERVAL = 2  # seconds between each elimination

# Global dict to store info after the block is reached
sorteio_data = {
    "start_time": None,         # when reveal started
    "block_hash": None,         # for seeding
    "elimination_order": [],    # entire random order (secret)
    "losers_order": [],         # everyone except final 2, in order
    "final_winners": [],        # last 2 in the random order
}

def get_current_block_height():
    """Fetch current blockchain height from Blockstream."""
    try:
        r = requests.get("https://blockstream.info/api/blocks/tip/height")
        r.raise_for_status()
        return int(r.text)
    except:
        return None

def get_block_hash(height):
    """Fetch block hash by height from Blockstream."""
    try:
        r = requests.get(f"https://blockstream.info/api/block-height/{height}")
        r.raise_for_status()
        return r.text.strip()
    except:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status.json")
def status_json():
    current_height = get_current_block_height()

    # If not started, check if we can start
    if sorteio_data["start_time"] is None:
        if current_height and current_height >= TARGET_BLOCK_HEIGHT:
            _start_reveal()  # sets start_time, block_hash, etc.
        else:
            # Still waiting, return basic status
            return jsonify({
                "bloco_alvo": TARGET_BLOCK_HEIGHT,
                "altura_atual": current_height,
                "status": "Aguardando o bloco alvo...",
                "hash": None,
                "all_members": ORIGINAL_LIST,   # show them in original order
                "eliminados": [],
                "restantes": ORIGINAL_LIST,     # nobody eliminated yet
                "adms_selecionados": []
            })

    # If started, we are in the reveal phase or done
    return jsonify(_reveal_status(current_height))

def _start_reveal():
    """Initialize everything once the block is reached."""
    sorteio_data["start_time"] = time.time()
    block_hash = get_block_hash(TARGET_BLOCK_HEIGHT)
    if not block_hash:
        return
    sorteio_data["block_hash"] = block_hash

    # SECRET shuffle (for elimination order)
    random.seed(int(block_hash, 16))
    elimination_order = random.sample(ORIGINAL_LIST, len(ORIGINAL_LIST))
    sorteio_data["elimination_order"] = elimination_order

    # Everyone except last 2 = losers
    sorteio_data["losers_order"] = elimination_order[:-2]
    # The last 2 in the random order are final winners
    sorteio_data["final_winners"] = elimination_order[-2:]

def _reveal_status(current_height):
    """Return how many are eliminated so far."""
    elapsed = time.time() - sorteio_data["start_time"]
    intervals_passed = int(elapsed // ELIMINATION_INTERVAL)

    total_losers = len(sorteio_data["losers_order"])
    # Limit intervals
    if intervals_passed > total_losers:
        intervals_passed = total_losers

    already_eliminated = sorteio_data["losers_order"][:intervals_passed]
    remaining = [m for m in ORIGINAL_LIST if m not in already_eliminated]  # keep original order

    # If we have only 2 left, the game is done
    if len(remaining) == 2:
        status = "Bloco alcançado e sorteio concluído!"
        adms_selecionados = sorteio_data["final_winners"]
    else:
        status = "Bloco alcançado! Revelando gradualmente..."
        adms_selecionados = []

    return {
        "bloco_alvo": TARGET_BLOCK_HEIGHT,
        "altura_atual": current_height,
        "status": status,
        "hash": sorteio_data["block_hash"],
        "all_members": ORIGINAL_LIST,            # show them in the original order
        "eliminados": already_eliminated,        # how many are already out
        "restantes": remaining,                  # who’s still in, in original order
        "adms_selecionados": adms_selecionados
    }

if __name__ == "__main__":
    app.run(debug=True)