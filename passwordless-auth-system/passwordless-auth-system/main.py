import hashlib

from flask import Flask, request, jsonify, send_from_directory
from server.db import  get_public_key
from constants import g, q
from flask_cors import CORS
from client.cli import user_registration
from server.verifier import verify_proof
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
app = Flask(__name__)
CORS(app)  # Allow all origins by default
challenges = {}

# Serve the Register Page
@app.route('/register', methods=['GET'])
def serve_register_page():
    return send_from_directory('fe', 'register.html')

# Serve the Login Page
@app.route('/login', methods=['GET'])
def serve_login_page():
    return send_from_directory('fe', 'login.html')

# Endpoint to handle user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    y=user_registration(username,password)
    return jsonify({"message": "User registered successfully!", "public_key": hex(y)})

@app.route('/auth/start', methods=['POST'])
def start_auth():
    username = request.form['username']
    commitment_t = int(request.form['commitment_t'], 16)  # Convert from hex

    y = get_public_key(username)  # Retrieve public key y
    if not y:
        logging.warning(f"User {username} not found.")
        return jsonify({"error": "User not found"}), 404

    # Compute challenge `c` based on `t` received from client
    # `c = H(g, y, t) mod q`
    c = int(hashlib.sha256(f"{g}{y}{commitment_t}".encode()).hexdigest(), 16) % q
    logging.debug(f"Challenge generated: c={c} for user {username}")

    # Store the challenge and commitment temporarily
    challenges[username] = (c, commitment_t)

    return jsonify({"challenge_c": hex(c)})


@app.route('/auth/verify', methods=['POST'])
def verify_auth():
    username = request.form['username']
    r_hex = request.form['r']
    c_hex = request.form['c']

    if username not in challenges:
        logging.warning(f"User {username} attempted login with no challenge stored.")
        return jsonify({"error": "No pending authentication request"}), 400

    c, commitment_t = challenges.pop(username)  # Retrieve stored challenge and commitment
    r = int(r_hex, 16)  # Convert from hex
    c = int(c_hex, 16)  # Convert from hex

    y = get_public_key(username)
    if not y:
        logging.warning(f"User {username} not found during verification.")
        return jsonify({"error": "User not found"}), 404
    logging.debug(f"Verifying proof for user {username}: r={r}, c={c}, y={y}, t={commitment_t}")
    # Verify proof using the correct stored commitment `t`
    if verify_proof(r, c, y, commitment_t):
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid proof!"}), 401

if __name__ == '__main__':
    app.run(debug=True)