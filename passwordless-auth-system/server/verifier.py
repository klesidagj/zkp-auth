import hashlib
from server.constants import p, g, q

# Verify proof (t, s) for given username
def verify_proof(t, s, y):
    # Compute challenge c = H(t || y)
    hash_input = f"{t}{y}".encode()
    c = int(hashlib.sha256(hash_input).hexdigest(), 16) % q

    # Verify if g^s mod p == t * y^c mod p
    lhs = pow(g, s, p)
    rhs = (t * pow(y, c, p)) % p
    return lhs == rhs