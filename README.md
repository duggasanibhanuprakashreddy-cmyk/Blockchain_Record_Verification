# ⚡ BlockVerify

### Blockchain-Based Tamper-Proof Record Verification

BlockVerify is a secure digital record verification system that uses **SHA-256 cryptographic hashing** and a **blockchain-style chained ledger** to detect whether a stored digital record has been modified after creation.

The system generates a unique cryptographic fingerprint for each record and stores that fingerprint inside a chained block. During verification, the record is hashed again and compared with the stored hash.

If the hashes match, the record is considered **Genuine**.  
If they do not match, the record is detected as **Tampered**.

---

## 🎯 Problem Statement

Digital records can be modified or tampered with after they are created.

Traditional record systems may not provide an easy way to verify whether the original data has been changed.

BlockVerify addresses this problem by creating a tamper-evident record verification system using cryptographic hashing and blockchain concepts.

---

## 💡 Proposed Solution

BlockVerify follows these steps:

1. A digital record is entered into the system.
2. The record is converted into a SHA-256 hash.
3. The hash is stored inside a blockchain-style block.
4. Each block is linked to the previous block using its hash.
5. During verification, the record is hashed again.
6. The newly generated hash is compared with the stored hash.
7. The system reports whether the record is **Genuine** or **Tampered**.

---

## 🔐 Key Features

- ⚡ Simple and user-friendly interface
- 🔒 SHA-256 cryptographic hashing
- ⛓️ Chained blockchain-style ledger
- 🛡️ Tamper detection
- 🔎 Record verification
- 📋 Stored records management
- 🧱 Blockchain explorer
- ✅ Blockchain integrity checking
- 💾 JSON-based persistent storage
- 🚫 Duplicate record ID protection

---

## 🏗️ System Architecture

```text
                ┌──────────────────┐
                │      User        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Streamlit UI    │
                └────────┬─────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
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
              │ Verification    │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
         ✅ Genuine        ⚠️ Tampered
## Testing and Verification Flow

The BlockVerify system follows these steps to verify digital records:

1. The user enters a unique Record ID and record details.
2. The system generates a SHA-256 hash of the record.
3. The record hash is stored in the blockchain ledger.
4. During verification, the record is hashed again.
5. The newly generated hash is compared with the stored hash.
6. If both hashes match, the record is marked as **Genuine**.
7. If the hashes do not match, the record is marked as **Tampered**.
8. The blockchain integrity is also checked using the previous and current block hashes.

This process helps detect unauthorized modifications to stored digital records.