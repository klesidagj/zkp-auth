import hashlib
from constants import p, g, q
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def verify_proof(r, c, y, t):
    """Verifies the proof by checking t' = g^r * y^c mod p"""
    logging.debug(f"Verifying proof: r={r}, c={c}, y={y}, t={t}")
    y = int(y)

    # Compute t' = g^r * y^c mod p
    t_prime = (pow(g, r, p) * pow(y, c, p)) % p
    logging.debug(f"Computed t' = {t_prime}")

    # Recompute c from the challenge hash using stored `t`
    hash_input = f"{g}{y}{t_prime}".encode()
    computed_c = int(hashlib.sha256(hash_input).hexdigest(), 16) % q
    logging.debug(f"Computed challenge = {computed_c}, Received challenge = {c}")

    return computed_c == c  # Authentication is successful only if challenges match
