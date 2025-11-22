# multiuser_exchange.py
import random
import hashlib

def _random_bases(n):
    return [random.randint(0,1) for _ in range(n)]

def _random_bits(n):
    return [random.randint(0,1) for _ in range(n)]

def simulate_bb84(length=128, noise_rate=0.02):
    alice_bits = _random_bits(length)
    alice_bases = _random_bases(length)
    bob_bases = _random_bases(length)
    bob_bits = []
    for i in range(length):
        if alice_bases[i] == bob_bases[i]:
            bit = alice_bits[i]
            if random.random() < noise_rate:
                bit = 1 - bit
            bob_bits.append(bit)
        else:
            bob_bits.append(random.randint(0,1))
    sifted = [i for i in range(length) if alice_bases[i] == bob_bases[i]]
    shared_bits = [alice_bits[i] for i in sifted]
    # convert shared bits to bytes
    b = 0
    bytelist = []
    for i, bit in enumerate(shared_bits):
        b = (b << 1) | bit
        if (i % 8) == 7:
            bytelist.append(b & 0xFF)
            b = 0
    raw = bytes(bytelist) if bytelist else b""
    if len(raw) < 32:
        raw = hashlib.sha3_512(raw).digest()
    shared_key_hex = hashlib.sha3_512(raw).hexdigest()[:64]
    return {
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "sifted_indices": sifted,
        "shared_key_hex": shared_key_hex
    }
