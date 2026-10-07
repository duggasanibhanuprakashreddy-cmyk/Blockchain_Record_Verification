import json
import os

from blockchain import Block

DATA_FILE = "data/blockchain.json"


def save_blockchain(blockchain):
    """Save the complete blockchain ledger to a JSON file."""
    data = []

    for block in blockchain.chain:
        data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "record_id": block.record_id,
            "record_hash": block.record_hash,
            "previous_hash": block.previous_hash,
            "current_hash": block.current_hash
        })

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_blockchain():
    """Load the stored blockchain ledger from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return None

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    return data