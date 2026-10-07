import hashlib
from datetime import datetime


class Block:
    def __init__(self, index, record_id, record_hash, previous_hash):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.record_id = record_id
        self.record_hash = record_hash
        self.previous_hash = previous_hash

        self.current_hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = (
            str(self.index)
            + self.timestamp
            + self.record_id
            + self.record_hash
            + self.previous_hash
        )

        return hashlib.sha256(block_data.encode()).hexdigest()


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            0,
            "GENESIS",
            "0",
            "0"
        )

        self.chain.append(genesis_block)

    def add_block(self, record_id, record_hash):
        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            record_id,
            record_hash,
            previous_block.current_hash
        )

        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):

            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check current block hash
            if current_block.current_hash != current_block.calculate_hash():
                return False

            # Check connection with previous block
            if current_block.previous_hash != previous_block.current_hash:
                return False

        return True

    @classmethod
    def from_data(cls, data):

        blockchain = cls()

        # Remove automatically created Genesis block
        blockchain.chain = []

        for item in data:

            block = Block(
                item["index"],
                item["record_id"],
                item["record_hash"],
                item["previous_hash"]
            )

            # Restore original timestamp
            block.timestamp = item["timestamp"]

            # Restore original current hash
            block.current_hash = item["current_hash"]

            blockchain.chain.append(block)

        return blockchain