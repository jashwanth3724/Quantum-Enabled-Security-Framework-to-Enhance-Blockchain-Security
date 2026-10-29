from ecdsa import SigningKey, SECP256k1

def generate_ecdsa_keys():
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    return sk, vk