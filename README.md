# 🔐 Quantum Secured Blockchain

## 📌 Overview

Quantum Secured Blockchain is an academic project that explores the security challenges faced by traditional blockchain systems in the era of quantum computing. The project examines classical cryptographic algorithms such as RSA and ECDSA and studies how quantum computing techniques, including Shor's Algorithm, could affect their security.

The project aims to explore quantum-resistant security approaches, particularly Post-Quantum Cryptography (PQC), to improve blockchain security against potential quantum attacks.

## 🎯 Objectives

- Understand the security limitations of classical cryptographic algorithms.
- Study the impact of quantum computing on blockchain security.
- Explore RSA and ECDSA cryptographic mechanisms.
- Demonstrate or analyze the impact of Shor's Algorithm on classical cryptography.
- Investigate post-quantum cryptographic approaches for enhancing blockchain security.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Cryptography:** RSA, ECDSA
- **Quantum Computing Concepts:** Shor's Algorithm
- **Blockchain:** Blockchain fundamentals and security
- **Libraries:** Refer to `requirements.txt` for project dependencies.

## 📂 Project Structure

```text
quantum-secured-blockchain/
│
├── __pycache__/
├── app.py
├── blockchain.py
├── ecdsa_module.py
├── requirements.txt
├── rsa_module.py
├── run_demo.py
├── shor_attack.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/quantum-secured-blockchain.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Navigate to the project directory

```bash
cd quantum-secured-blockchain
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux or macOS:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Project

Run the main application:

```bash
python app.py
```

To run the demonstration script, if supported by your implementation:

```bash
python run_demo.py
```

## 🔍 Key Components

- **`app.py`** — Application entry point.
- **`blockchain.py`** — Blockchain-related implementation.
- **`ecdsa_module.py`** — ECDSA cryptographic operations.
- **`rsa_module.py`** — RSA cryptographic operations.
- **`shor_attack.py`** — Shor's Algorithm-related attack demonstration or simulation.
- **`run_demo.py`** — Demonstration script.
- **`requirements.txt`** — Python project dependencies.

*The descriptions above are based on the filenames; confirm them against the actual source code.*

## 🔒 Security Significance

Quantum computing presents a potential threat to widely used public-key cryptographic systems. Shor's Algorithm, when executed on a sufficiently capable fault-tolerant quantum computer, could threaten RSA and elliptic-curve cryptography.

This project provides an academic exploration of these risks and motivates research into post-quantum cryptographic alternatives.

## 🚀 Future Enhancements

- Integrate standardized post-quantum cryptographic algorithms.
- Evaluate the performance of classical and post-quantum cryptographic approaches.
- Explore quantum-resistant digital signatures for blockchain transactions.
- Investigate Quantum Key Distribution (QKD) and Quantum Random Number Generation (QRNG).
- Extend security testing and performance evaluation.

## 🎓 Project Type

Academic Project / Blockchain Security Research

## 👥 Contributors

Add the names of your project team members here.

## ⚠️ Disclaimer

This project is intended for educational and research purposes. Any attack-related demonstrations should be performed only in controlled environments. The project should not be considered a production-ready blockchain security solution.
