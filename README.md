# ⚡ BlockVerify

### Blockchain-Based Tamper-Proof Record Verification

BlockVerify is a secure digital record verification system that uses **SHA-256 cryptographic hashing** and a **blockchain-style chained ledger** to detect whether a stored digital record has been modified after creation.

The system generates a unique cryptographic fingerprint for each record and stores that fingerprint inside a chained block. During verification, the record is hashed again and compared with the stored hash.

- If the hashes match, the record is considered **Genuine** (Verified ✅).  
- If they do not match, the record is detected as **Tampered** (Security Alert ⚠️).

---

## 🎯 Problem Statement

Digital records can be modified or tampered with after they are created. Traditional centralized record systems may not provide an easy, verifiable way to confirm whether the original data has been modified.

BlockVerify addresses this problem by creating a tamper-evident record verification system using cryptographic hashing and blockchain immutability concepts.

---

## 💡 How BlockVerify Works

1. **Add Record:** A digital record (Student ID, Name, Course, CGPA) is entered into the system.
2. **Cryptographic Fingerprint:** The record is converted into a deterministic SHA-256 hash.
3. **Chained Ledger:** The hash is anchored inside a blockchain block linked cryptographically to the previous block's hash.
4. **Verification:** During verification, the record is hashed again using SHA-256.
5. **Tamper Detection:** The newly generated hash is compared with the blockchain's stored hash.
6. **Integrity Audit:** The blockchain continuously validates block linkage and internal hash consistency.

---

## 🔐 Key Features

- ⚡ **Interactive Web Interface & Streamlit App**
- 🔒 **SHA-256 Cryptographic Hashing**
- ⛓️ **Chained Blockchain-Style Ledger**
- 🛡️ **Instant Tamper Detection & Avalanche Effect Demonstration**
- 🔎 **Two-Way Record Verification (Stored vs Generated Hash comparison)**
- 📋 **Stored Records Management**
- 🧱 **Blockchain Explorer**
- ✅ **Blockchain Integrity Checking**
- 💾 **JSON-Based & Persistent Storage**
- 🚫 **Duplicate Record ID Protection**
- ☀️/🌙 **Dark & Light Mode Support**

---

## 🏗️ System Architecture

```text
                ┌──────────────────┐
                │      User        │
                └────────┬─────────┘
                         │
                         ▼
        ┌──────────────────────────────────┐
        │     BlockVerify Web / UI App      │
        └────────┬─────────────────┬───────┘
                 │                 │
      ┌──────────┴──────────┐      │
      ▼                     ▼      ▼
┌───────────────┐     ┌───────────────┐
│  Add Record   │     │ Verify Record │
└───────┬───────┘     └───────┬───────┘
        │                     │
        ▼                     ▼
┌────────────────────────────────────┐
│       SHA-256 Hashing              │
└────────────────┬───────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Blockchain-Style│
        │     Ledger      │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Verification   │
        └────────┬────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
   ✅ Genuine        ⚠️ Tampered
```

---

## 🚀 Running the Project

### 1. Run Streamlit Application Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit application
streamlit run app.py
```
Access the application at `http://localhost:8501`.

### 2. Deploying to Streamlit Cloud
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your repository, set the main file path to `app.py`, and click **Deploy**.

### 3. Deploying to Vercel
The repository includes complete web assets (`index.html`) and serverless API handlers (`api/index.py` and `vercel.json`):
1. Connect your GitHub repository to [Vercel](https://vercel.com).
2. Deploy with zero configuration.
3. Access the full interactive web application directly at your `.vercel.app` URL!

---

## 🛠️ Technologies Used

- **Python** – Core blockchain logic and cryptographic hashing
- **Streamlit** – Python-based web application interface
- **Vanilla HTML5/CSS3/JavaScript** – Vercel-ready frontend web application
- **SHA-256** – Cryptographic record fingerprinting
- **JSON** – Local blockchain ledger persistence
- **Vercel Serverless** – Cloud API endpoints