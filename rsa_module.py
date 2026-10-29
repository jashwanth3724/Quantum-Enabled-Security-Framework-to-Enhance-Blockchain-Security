import math

def generate_rsa_keys():

    # slightly larger primes for better demo
    p = 11
    q = 13

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 7
    d = pow(e, -1, phi)

    return (e, n), (d, n), p, q


def message_to_number(message, n):
    return sum(ord(c) for c in message) % n


def sign(message, private_key):

    d, n = private_key
    m = message_to_number(message, n)

    return pow(m, d, n)


def verify(message, signature, public_key):

    e, n = public_key
    m = message_to_number(message, n)

    return pow(signature, e, n) == m