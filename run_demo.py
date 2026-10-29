from blockchain import create_blockchain, Block
from rsa_module import generate_rsa_keys, sign, verify
from shor_attack import shor_factor
import time

# -------------------------------------------------
# CREATE BLOCKCHAIN
# -------------------------------------------------

chain = create_blockchain()

print("\n==============================")
print("   BLOCKCHAIN BEFORE ATTACK")
print("==============================\n")

time.sleep(2)

for block in chain:

    if "Attacker" in block.transaction:
        print("⚠ MALICIOUS BLOCK INSERTED ⚠")

    print("Block:", block.index)
    print("Transaction:", block.transaction)
    print("Hash:", block.hash)
    print()

    time.sleep(1.5)

time.sleep(2)
# -------------------------------------------------
# RSA SECURITY
# -------------------------------------------------

print("\n==============================")
print("      RSA SECURITY ACTIVE")
print("==============================\n")

public_key, private_key, p_real, q_real = generate_rsa_keys()

transaction = "Likhitha sends 1000 BTC to Jashwanth"

signature = sign(transaction, private_key)

time.sleep(2)

print("Transaction:", transaction)
print("Signature:", signature)
print("Verification:", verify(transaction, signature, public_key))

time.sleep(2)

# -------------------------------------------------
# SHOR ATTACK
# -------------------------------------------------

print("\n==============================")
print("   QUANTUM ATTACK STARTED")
print("   Running Shor Algorithm...")
print("==============================\n")

time.sleep(2)

e, N = public_key

p, q = shor_factor(N)

print("RSA modulus N =", N)
print("Factors discovered:", p, "and", q)

phi = (p - 1) * (q - 1)

d = pow(e, -1, phi)

print("Recovered PRIVATE KEY:", d)

time.sleep(2)

# -------------------------------------------------
# ATTACKER FORGES TRANSACTION
# -------------------------------------------------

print("\n==============================")
print("   ATTACKER INSERTING FAKE BLOCK")
print("==============================\n")

fake_transaction = "Likhitha sends 100 BTC to Attacker"

time.sleep(2)

fake_signature = pow(sum(ord(c) for c in fake_transaction) % N, d, N)

print("Forged Transaction:", fake_transaction)
print("Forged Signature:", fake_signature)

time.sleep(2)

valid = verify(fake_transaction, fake_signature, public_key)

print("Network accepted transaction:", valid)

time.sleep(2)

# -------------------------------------------------
# INSERT MALICIOUS BLOCK
# -------------------------------------------------

previous_hash = chain[2].hash

fake_block = Block(3, fake_transaction, previous_hash)

chain.insert(3, fake_block)

time.sleep(2)

# -------------------------------------------------
# SHOW BLOCKCHAIN AFTER ATTACK
# -------------------------------------------------

print("\n==============================")
print("   BLOCKCHAIN AFTER ATTACK")
print("==============================\n")

time.sleep(2)

for block in chain:

    if "Attacker" in block.transaction:
        print("⚠ MALICIOUS BLOCK INSERTED ⚠")

    time.sleep(2)

    print("Block:", block.index)
    print("Transaction:", block.transaction)
    print("Hash:", block.hash)
    print()