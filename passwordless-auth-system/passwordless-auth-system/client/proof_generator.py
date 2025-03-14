import hashlib
import random
from constants import p,q,g

def generate_commitment():
    """Client generates commitment t = g^v mod p and sends it to the server."""
    v = random.randint(1, q)  # Random nonce
    t = pow(g, v, p)
    return v, t  # Return the random v for later proof generation

def generate_proof(v, c, password):
    """Generate Fiat-Shamir proof r using v, challenge c, and secret x derived from password."""
    x = int.from_bytes(hashlib.sha256(password.encode()).digest(), 'big') % q
    r = (v - c * x) % q  # Compute response
    return r


