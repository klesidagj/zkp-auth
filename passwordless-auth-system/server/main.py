import hashlib

from flask import Flask, request, jsonify
from server.db import store_user, get_public_key
from server.constants import g, p
from client.proof_generator import generate_proof
from server.verifier import verify_proof

app = Flask(__name__)

#endpoint to acccess in browser for registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Compute public key y
    x = int.from_bytes(hashlib.sha256(password.encode()).digest(), 'big') % (p - 1)
    y = pow(g, x, p)

    # Store username and public key
    store_user(username, y)

    # Generate proof for user to copy
    t, s = generate_proof(password, y)
    return jsonify({
        "message": "Registration successful.",
        "public_key": y,
        "proof_t": t,
        "proof_s": s
    })


#endpoint to access in browser for login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    t = int(request.form['proof_t'])
    s = int(request.form['proof_s'])

    # Fetch public key for the username
    y = get_public_key(username)
    if not y:
        return jsonify({"error": "User not found"}), 404

    # Verify proof
    if verify_proof(t, s, y):
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid proof!"}), 401


if __name__ == '__main__':
    app.run(debug=True)