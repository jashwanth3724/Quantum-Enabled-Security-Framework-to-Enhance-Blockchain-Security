import hashlib
import time

class Block:

    def __init__(self, index, transaction, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.timestamp) + str(self.transaction) + str(self.previous_hash)
        return hashlib.sha256(data.encode()).hexdigest()


def create_blockchain():

    blockchain = []

    genesis = Block(0, "Genesis Block", "0")
    blockchain.append(genesis)

    transactions = [
        "Likhitha sends 1000 BTC to Jashwanth",
        "Jashwanth sends 500 BTC to Poorvi",
        "Poorvi sends 234 BTC to Abishek",
        "Abishek sends 156 BTC to Santhosh"
    ]

    previous_hash = genesis.hash

    for i, tx in enumerate(transactions):

        block = Block(i + 1, tx, previous_hash)
        blockchain.append(block)

        previous_hash = block.hash

    return blockchain