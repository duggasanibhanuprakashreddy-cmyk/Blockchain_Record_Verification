import json
import os

from blockchain import Blockchain, Block


DATA_FILE = "data/blockchain.json"


# Check file
if not os.path.exists(DATA_FILE):
    print("ERROR: blockchain.json not found.")
    exit()


# Load existing blockchain
with open(DATA_FILE, "r") as file:
    data = json.load(file)


print("Original blocks:", len(data))


# Keep only first occurrence of each record ID
unique_records = []
seen_ids = set()

for item in data:

    record_id = item["record_id"]

    if record_id == "GENESIS":
        continue

    if record_id not in seen_ids:

        seen_ids.add(record_id)
        unique_records.append(item)


# Create fresh blockchain
new_blockchain = Blockchain()

# Remove automatically created genesis
new_blockchain.chain = []


# Create fresh genesis
genesis = Block(
    0,
    "GENESIS",
    "0",
    "0"
)

new_blockchain.chain.append(genesis)


# Rebuild blocks
for item in unique_records:

    new_blockchain.add_block(
        item["record_id"],
        item["record_hash"]
    )


# Prepare JSON
output = []

for block in new_blockchain.chain:

    output.append({
        "index": block.index,
        "timestamp": block.timestamp,
        "record_id": block.record_id,
        "record_hash": block.record_hash,
        "previous_hash": block.previous_hash,
        "current_hash": block.current_hash
    })


# Save
with open(DATA_FILE, "w") as file:

    json.dump(
        output,
        file,
        indent=4
    )


# Result
print()
print("========================================")
print("BLOCKVERIFY CLEANUP COMPLETE")
print("========================================")

print()
print("Original blocks:", len(data))
print("Cleaned blocks:", len(new_blockchain.chain))
print("Stored records:", len(new_blockchain.chain) - 1)

print()
print("Records kept:")

for block in new_blockchain.chain:

    if block.record_id != "GENESIS":

        print(
            "  Block",
            block.index,
            "->",
            block.record_id
        )


print()

if new_blockchain.is_chain_valid():

    print("Blockchain integrity: VALID")

else:

    print("Blockchain integrity: INVALID")

print()
print("========================================")