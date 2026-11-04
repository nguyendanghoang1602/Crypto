# FINAL VALIDATION REPORT — RSA ACADEMIC REPORT QA

**Project Title:** Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication  
**Repository:** `https://github.com/nguyendanghoang1602/Crypto`  
**Branch:** `rsa-final-qa-2026-11-04`  
**Audit Date:** November 4, 2026  

---

## 1. REPOSITORY & WORKSPACE VERIFICATION

- **Actual Git Repository Location:** `D:\Crypto_repo` (verified via `git rev-parse --show-toplevel`)
- **Remote Origin URL:** `https://github.com/nguyendanghoang1602/Crypto.git` (verified via `git remote get-url origin`)
- **Workspace Clarification:** `D:\Crypto` is a local directory clone without `.git` metadata; `D:\Crypto_repo` is the authoritative Git tracking repository.

---

## 2. SUMMARY OF MICRO-FIXES & PRECISION REFINEMENTS

The final micro-fix pass incorporates all 5 required technical terminology refinements:

1. **SHA-256 Modulus Alignment vs. Homomorphic Distinction:** Clarified that SHA-256 maps arbitrary-length messages to a fixed-length 256-bit digest, allowing RSA-PSS to operate on a fixed-length digest-derived encoding that fits the RSA modulus rather than applying RSA directly to the full message. Explicitly reiterated that SHA-256 itself does not eliminate textbook RSA's multiplicative homomorphism.
2. **RSA-PSS Security Proof Theoretical Distinction:** Disentangled the engineering specification (RFC 8017 [2] / NIST FIPS 186-5 [4]) from foundational theoretical cryptanalysis (Bellare and Rogaway, EUROCRYPT '96 [23]), proving an essentially tight EUF-CMA security reduction to the RSA inversion problem in the Random Oracle Model (ROM).
3. **RSA-OAEP Key Transport Terminology:** Refined key transport description to "encrypting (wrapping) an ephemeral 256-bit AES key using RSA-OAEP" (NIST SP 800-56B Rev. 2 [5] and SP 800-38D [22]), maintaining the rigorous distinction between RSA key transport and KEM encapsulation (such as ML-KEM in RFC 10024 [19]).
4. **FIPS 140-3 Module Validation Terminology:** Corrected description to "Hardware Security Modules (HSMs) implemented in cryptographic modules validated under FIPS 140-3, where applicable," clarifying that FIPS 140-3 specifies security requirements for cryptographic modules rather than being an HSM product category.
5. **Calibrated Distributed Production Requirements:** Refined replay prevention wording to "production deployments with multiple gateway instances typically need durable, shared, atomic nonce check-and-insert mechanisms (e.g., Redis SETNX or SQL unique constraint transactions) with TTL expiration," preserving security importance while avoiding overly rigid absolute constraints.
6. **Enhanced Table Readability:** Slightly increased Table 1 (7.5 pt bold / 7.3 pt body) and Table 2 (7.4 pt bold / 7.2 pt body) font sizes, preserving visual clarity and strict 5-page A4 layout.

---

## 3. BENCHMARK STRUCTURE & MEASUREMENT COUNT

The empirical benchmark dataset in `03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv` and `benchmark_results.csv` contains exactly **840 raw measurements** with the following verified structure:

- **4 Algorithm Configurations:** RSA-2048, RSA-3072, RSA-4096, and ECDSA-secp256k1.
- **Trial Distribution per Algorithm:**
  - Key-generation: 10 measurements per algorithm ($4 \times 10 = 40\text{ measurements}$).
  - Signature generation: 100 measurements per algorithm ($4 \times 100 = 400\text{ measurements}$).
  - Signature verification: 100 measurements per algorithm ($4 \times 100 = 400\text{ measurements}$).
- **Aggregate Total:** $40 + 400 + 400 = 840\text{ measurements}$.

---

## 4. BIBLIOGRAPHY CITATION CROSS-REFERENCE TABLE (23 REFERENCES)

| Reference | Standard / Literature | In-Text Citation Location | Academic Venue / Organization | Verified |
| :--- | :--- | :--- | :--- | :---: |
| **[1]** | Rivest, Shamir, & Adleman (1978/1977) | Section 1, Section 2.1 | CACM / MIT Memorandum | **YES** |
| **[2]** | PKCS #1 v2.2 (RFC 8017) | Section 1, Section 2.1, Section 2.2 | IETF Informational | **YES** |
| **[3]** | TLS 1.3 Protocol (RFC 9846, supersedes RFC 8446) | Section 1, Section 2.3 | IETF Standards Track | **YES** |
| **[4]** | Digital Signature Standard (NIST FIPS 186-5) | Section 2.2 | NIST Standard (Key Separation) | **YES** |
| **[5]** | Pair-Wise Key Establishment (NIST SP 800-56B Rev. 2) | Section 2.2, Section 2.3, Section 3, Table 1, Table 2 | NIST Special Publication (6 authors) | **YES** |
| **[6]** | Key Management Part 1 (NIST SP 800-57 Part 1 Rev. 5) | Section 3, Table 1, Table 2 | NIST Special Publication | **YES** |
| **[7]** | Bellcore CRT Fault Attack (Boneh et al., 2001) | Section 3.2 | Journal of Cryptology | **YES** |
| **[8]** | Schnorr Signatures for secp256k1 (BIP 340) | Section 1, Section 3, Section 3.1, Table 1 | Bitcoin Improvement Proposal | **YES** |
| **[9]** | Segregated Witness Consensus (BIP 141) | Section 3.1 | Bitcoin Improvement Proposal | **YES** |
| **[10]** | MuSig2 Multi-Signatures (BIP 327) | Section 3.1 | Bitcoin Improvement Proposal | **YES** |
| **[11]** | Edwards-Curve Digital Signatures (RFC 8032) | Section 3, Table 1 | IETF Standards Track | **YES** |
| **[12]** | Bitcoin Developer Guide: Transactions | Section 1, Section 3, Section 3.1, Table 1 | Bitcoin Core Reference | **YES** |
| **[13]** | Ethereum Developer Documentation: Transactions | Section 1, Section 3, Section 3.1, Table 1 | Ethereum Foundation Docs | **YES** |
| **[14]** | Project Wycheproof Test Vectors (v0.9 Snapshot) | Section 5.2 | Google Security Research | **YES** |
| **[15]** | OAEP Reconsidered (Shoup, 2002 / CRYPTO 2001) | Section 2.2 | Journal of Cryptology / LNCS 2139 | **YES** |
| **[16]** | RSA-OAEP Security (Fujisaki et al., 2004 / CRYPTO 2001) | Section 2.2 | Journal of Cryptology / LNCS 2139 | **YES** |
| **[17]** | Optimal Asymmetric Encryption (Bellare-Rogaway, 1995) | Section 2.2 | EUROCRYPT '94 / LNCS 950 | **YES** |
| **[18]** | Legacy RSASSA-PKCS1-v1_5 Code Points (RFC 9963) | Section 2.3 | IETF Standards Track | **YES** |
| **[19]** | PQ/T Hybrid Key Agreement (RFC 10024) | Section 2.3 | IETF Standards Track | **YES** |
| **[20]** | Module-Lattice-Based DSS (NIST FIPS 204) | Section 6 (Conclusion) | NIST Standard (ML-DSA) | **YES** |
| **[21]** | Stateless Hash-Based DSS (NIST FIPS 205) | Section 6 (Conclusion) | NIST Standard (SLH-DSA) | **YES** |
| **[22]** | Galois/Counter Mode AES-GCM (NIST SP 800-38D) | Section 2.2, Section 2.3 | NIST Special Publication | **YES** |
| **[23]** | Exact Security of Signatures (Bellare-Rogaway, 1996) | Section 2.2 | EUROCRYPT '96 / LNCS 1070 | **YES** |

---

## 5. DOCUMENT LAYOUT & VERIFICATION METRICS

- **Primary Word Document:** Exactly **5 A4 pages** (`doc.ComputeStatistics(2) == 5`).
- **Rendered PDF Document:** Exactly **5 Pages** (`len(pdf) == 5`).
- **Word Count:** **4,688 words**.
- **Page-by-Page Structural Distribution:**
  - **Page 1:** Title, Metadata, Abstract, Keywords, Section 1 (Introduction), Section 2.1 (Math Foundations).
  - **Page 2:** Section 2.2 (OAEP vs. PSS, FIPS 186-5 Key Separation), Figure 1 (RSA-PSS Workflow), Section 2.3 (Applications), Section 3 (Why RSA?), Table 1 (Comparison Table + Caption), Section 3.1 start.
  - **Page 3:** Section 3.1 (Blockchain Trade-offs), Section 3.2 (Operational Value, CRT Faults), Section 4 (Proposed Design), Section 4.1 (Component Decomposition), Figure 2 (Architecture Diagram + Caption).
  - **Page 4:** Section 4.2 (Deterministic JSON), Algorithm 1 (Unified Box), Section 4.3 (Prototype Scope), Section 5 (Experimental Results), Section 5.1 (Scenarios), Section 5.2 (Wycheproof), Section 5.3 (Benchmark Intro), Table 2 Caption, Table 2 (All 4 rows unified).
  - **Page 5:** Figure 3 (Performance Chart + Caption), Performance Discussion (3 points), Section 6 (Conclusion), Section 7 (References [1]–[23] concluding cleanly).
- **Wycheproof Compliance:** **108 / 108 test cases passing** (63 valid accepted, 45 invalid rejected, 0 failures).
- **Operational Scenarios:** 5 / 5 target security scenarios validated.
- **Protected File Status:** `rsa_pss_experiment.py`, `generate_figures.py`, `benchmark_results.csv`, `raw_trials_all_algorithms.csv`, figure images, and Wycheproof test vectors remain **100% UNMODIFIED**.

---

## 6. DELIVERABLE ARTIFACT CHECKSUMS (SHA-256)

| Deliverable File | Size (Bytes) | SHA-256 Hash |
| :--- | :--- | :--- |
| `01_Final_Report/RSA_Real_World_Applications_Report.docx` | 456,097 | `bd22edd278447aacd99c4217a2b8927ba70a4b2156af615efcf78f229323fe68` |
| `01_Final_Report/RSA_Real_World_Applications_Report.pdf` | 448,481 | `2e52cf0de3455c8b7fe98fa1bdb2bde70fdb5430993f36534b180de173669f82` |
| `02_Source_Code/build_report_doc.py` | 59,397 | `244b68504d0ceaded4c664032730952bc6c850fd93fc539b2356cfe3a21e4158` |
| `05_Research_References/Research_Sources.md` | 21,982 | `549eed32cb7aabd1a71812f96ccc3ef13a96af84de7d69e7762a7b10c9758336` |
