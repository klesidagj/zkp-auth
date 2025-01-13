
# Passwordless Authentication System using Zero Knowledge Proofs

This project implements a passwordless authentication system using Zero Knowledge Proof (ZKP) principles. It enables secure user registration and login without directly storing or transmitting sensitive user passwords. 

---

## **Table of Contents**
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [File Structure](#file-structure)
4. [Setup and Installation](#setup-and-installation)
5. [Usage](#usage)
6. [System Architecture](#system-architecture)
7. [Endpoints](#endpoints)
8. [Contributing](#contributing)
9. [License](#license)

---

## **Overview**

This project provides a secure and efficient authentication system leveraging cryptographic techniques:
- **Backend:** Handles proof verification and stores user public keys.
- **Frontend:** Simple HTML interfaces for user registration and login.
- **Client:** Generates ZKP proofs for authentication.

---

## **System Requirements**
- **Programming Language:** Python 3.8+
- **Backend Framework:** Flask
- **Database:** PostgreSQL
- **Dependencies:** 
  - psycopg2
  - pycryptodome
  - hashlib

---

## **File Structure**
```
passwordless-auth-system
├── client
│   ├── cli.py            # Simple CLI for user input and proof submission.
│   └── proof_generator.py # Generates proof based on the user's secret.
├── fe
│   ├── login.html        # Frontend page for user login.
│   └── register.html     # Frontend page for user registration.
├── main.py               # Server API for receiving and verifying proofs.
├── server
│   ├── constants.py      # Cryptographic constants used in the ZKP system.
│   ├── db.py             # Handles database operations (e.g., user public keys).
│   └── verifier.py       # Verifies the proof using the ZKP protocol.
└── test_main.http        # Example HTTP requests for testing.
```

---

## **Setup and Installation**

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/passwordless-auth-system.git
cd passwordless-auth-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL
1. Set up a PostgreSQL database.
2. Update the `db.py` file with your database credentials.

### 4. Run the Application
```bash
python main.py
```

---

## **Usage**

### Registration
1. Open `register.html` in your browser.
2. Provide a username and password to register.
3. The server stores your public key, while the client retains the proof.

### Login
1. Open `login.html` in your browser.
2. Submit your username, proof (challenge and response values).
3. The server verifies the proof and grants access upon validation.

---

## **System Architecture**

### 1. **Frontend**
- HTML files for user registration (`register.html`) and login (`login.html`).

### 2. **Client**
- `cli.py`: Handles user input and registration by creating public keys.
- `proof_generator.py`: Generates ZKP proofs for authentication.

### 3. **Server**
- `constants.py`: Defines global cryptographic parameters (e.g., g, p, q).
- `db.py`: Manages database operations for storing and retrieving user public keys.
- `verifier.py`: Verifies proofs using the ZKP protocol.

---

## **Endpoints**

### `/register` (GET, POST)
- **GET:** Serves the registration page.
- **POST:** Receives username and password, generates public key, and stores it in the database.

### `/login` (GET, POST)
- **GET:** Serves the login page.
- **POST:** Receives proof (challenge and response) and validates it against the stored public key.

---
