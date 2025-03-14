import hashlib
from constants import p, g, q
from server.db import store_user

def user_registration(username, password):
    """Registers a new user by deriving the secret key x and computing the public key y."""
    x = int.from_bytes(hashlib.sha256(password.encode()).digest(), 'big') % q
    y = pow(g, x, p)  # Public key y = g^x mod p
    store_user(username, y)  # Store in database
    print(f"User {username} registered successfully with public key: {y}")
    return y