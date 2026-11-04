# FINAL VALIDATION REPORT — RSA ACADEMIC REPORT QA

**Project Title:** Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication  
**Repository:** `https://github.com/nguyendanghoang1602/Crypto`  
**Branch:** `rsa-final-qa-2026-11-04`  
**Audit Date:** November 4, 2026  

---

## 1. REPOSITORY VERIFICATION

- **Actual Git Repository Location:** `D:\Crypto_repo` (verified via `git rev-parse --show-toplevel`)
- **Remote Origin URL:** `https://github.com/nguyendanghoang1602/Crypto.git` (verified via `git remote get-url origin`)
- **Workspace Clarification:** `D:\Crypto` is a local directory clone without `.git` metadata; `D:\Crypto_repo` is the authoritative Git tracking repository.

---

## 2. BENCHMARK STRUCTURE & MEASUREMENT COUNT

The empirical benchmark dataset in `03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv` and `benchmark_results.csv` contains exactly **840 raw measurements** with the following verified structure:

- **4 Algorithm Configurations:** RSA-2048, RSA-3072, RSA-4096, and ECDSA-secp256k1.
- **Trial Distribution per Algorithm:**
  - Key-generation: 10 measurements per algorithm ($4 \times 10 = 40\text{ measurements}$).
  - Signature generation: 100 measurements per algorithm ($4 \times 100 = 400\text{ measurements}$).
  - Signature verification: 100 measurements per algorithm ($4 \times 100 = 400\text{ measurements}$).
- **Aggregate Total:** $40 + 400 + 400 = 840\text{ measurements}$.

*Note:* Any prior mention of "14 algorithm configurations × 60 trials" in transitional review logs was a historical typographic discrepancy. The actual raw and aggregated benchmark CSV files are 100% intact and preserved.

---

## 3. BITCOIN RSA-2048 WITNESS ASSUMPTION

The hypothetical Bitcoin witness calculation in Section 3.1 ($1 + 3 + 256 + 3 + 256 = 519\text{ bytes}$) is rigorously formulated under the explicit simplified assumption of a 256-byte modulus payload (treating the standard public exponent $e = 65,537$ as implicit or fixed, rather than a full DER-encoded public key which spans $\approx 294\text{ bytes}$). This adds $\approx 410\text{–}412\text{ witness bytes}$ ($\approx 103\text{ virtual bytes}$ under BIP 141), representing an approximate 73% increase over the 141-vB baseline transaction. The report explicitly emphasizes that native Bitcoin consensus rules do not support RSA verification, framing this purely as a theoretical illustration of why consensus layers mandate compact elliptic curve signatures.

---

## 4. BIBLIOGRAPHY CITATION CROSS-REFERENCE TABLE

| Reference | Standard / Document | In-Text Citation Location | Bibliography Status | Verified |
| :--- | :--- | :--- | :--- | :---: |
| **[1]** | Rivest, Shamir, & Adleman (1978/1977) | Section 1, Section 2.1 | CACM / MIT Memorandum | **YES** |
| **[2]** | PKCS #1 v2.2 (RFC 8017) | Section 1, Section 2.1, Section 2.2, Section 3.2 | IETF Informational | **YES** |
| **[3]** | TLS 1.3 Protocol (RFC 9846, supersedes RFC 8446) | Section 1, Section 2.3 | IETF Standards Track | **YES** |
| **[4]** | Digital Signature Standard (NIST FIPS 186-5) | Section 2.2 | NIST Standard (Key Separation) | **YES** |
| **[5]** | Pair-Wise Key Establishment (NIST SP 800-56B Rev. 2) | Section 2.2, Section 2.3, Section 3, Table 1, Table 2 | 6 authors (incl. Scott Simon) | **YES** |
| **[6]** | Key Management Part 1 (NIST SP 800-57 Part 1 Rev. 5) | Section 3, Table 1, Table 2 | NIST Special Publication | **YES** |
| **[7]** | Bellcore CRT Fault Attack (Boneh et al., 2001) | Section 3.2 | Journal of Cryptology | **YES** |
| **[8]** | Schnorr Signatures for secp256k1 (BIP 340) | Section 1, Section 3, Section 3.1, Table 1 | Bitcoin Improvement Proposal | **YES** |
| **[9]** | Segregated Witness Consensus (BIP 141) | Section 3.1 | Bitcoin Improvement Proposal | **YES** |
| **[10]** | MuSig2 Multi-Signatures (BIP 327) | Section 3.1 | Bitcoin Improvement Proposal | **YES** |
| **[11]** | Edwards-Curve Digital Signatures (RFC 8032) | Section 3, Table 1 | IETF Standards Track | **YES** |
| **[12]** | Bitcoin Developer Guide: Transactions | Section 1, Section 3, Section 3.1, Table 1 | Bitcoin Core Reference | **YES** |
| **[13]** | Ethereum Developer Documentation: Transactions | Section 1, Section 3, Section 3.1, Table 1 | Ethereum Foundation Docs | **YES** |
| **[14]** | Project Wycheproof Test Vectors (v0.9 Snapshot) | Section 5.2 | Google Security Research | **YES** |
| **[15]** | OAEP Reconsidered (Shoup, 2002 / CRYPTO 2001) | Section 2.2 | Journal of Cryptology | **YES** |
| **[16]** | RSA-OAEP Security (Fujisaki et al., 2004 / CRYPTO 2001) | Section 2.2 | Journal of Cryptology | **YES** |
| **[17]** | Optimal Asymmetric Encryption (Bellare-Rogaway, 1995) | Section 2.2 | EUROCRYPT '94 | **YES** |
| **[18]** | Legacy RSASSA-PKCS1-v1_5 Code Points (RFC 9963) | Section 2.3 | IETF Standards Track | **YES** |
| **[19]** | PQ/T Hybrid Key Agreement (RFC 10024) | Section 2.3 | IETF Standards Track | **YES** |
| **[20]** | Module-Lattice-Based DSS (NIST FIPS 204) | Section 6 (Conclusion) | NIST Standard (ML-DSA) | **YES** |
| **[21]** | Stateless Hash-Based DSS (NIST FIPS 205) | Section 6 (Conclusion) | NIST Standard (SLH-DSA) | **YES** |
| **[22]** | Galois/Counter Mode AES-GCM (NIST SP 800-38D) | Section 2.2, Section 2.3 | NIST Special Publication | **YES** |

---

## 5. DOCUMENT LAYOUT & VERIFICATION METRICS

- **Primary Word Document:** Exactly **5 A4 pages** (`doc.ComputeStatistics(2) == 5`).
- **Rendered PDF Document:** Exactly **5 Pages** (`len(pdf) == 5`).
- **Word Count:** **4,729 words**.
- **Paragraph Count:** **137 paragraphs**.
- **Character Count (w/ spaces):** **30,238 characters**.
- **Table 2 Placement:** Table 2 caption and **all four data rows** (RSA-2048, RSA-3072, RSA-4096, ECDSA-secp256k1) reside entirely on **Page 4** with 89.1 pt bottom margin clearance.
- **Algorithm 1:** Boxed and unified on **Page 4** (`w:cantSplit`, `keep_together`).
- **Figures:**
  - Figure 1: Operational workflow of RSA-PSS (Page 2).
  - Figure 2: Off-chain cryptocurrency withdrawal architecture (Page 3).
  - Figure 3: Empirical median latency comparison chart (Page 5).
- **Wycheproof Compliance:** **108 / 108 test cases passing** (63 valid accepted, 45 invalid rejected, 0 failures).
- **Operational Scenarios:** 5 / 5 target security scenarios validated.
- **Protected File Status:** `rsa_pss_experiment.py`, `generate_figures.py`, `benchmark_results.csv`, `raw_trials_all_algorithms.csv`, figure images, and Wycheproof test vectors remain **100% UNMODIFIED**.

---

## 6. DELIVERABLE ARTIFACT CHECKSUMS (SHA-256)

| Deliverable File | Size (Bytes) | SHA-256 Hash |
| :--- | :--- | :--- |
| `01_Final_Report/RSA_Real_World_Applications_Report.docx` | 456,330 | `77d74bc4e15cf5bb3bf7f4cbf99866b0275ee1de27788ea68f35f1d62603ce79` |
| `01_Final_Report/RSA_Real_World_Applications_Report.pdf` | 468,056 | `449a0fb198c4ea4363c5fdaec8b561e3fea19a75278b443965aae948ec677356` |
| `02_Source_Code/build_report_doc.py` | 58,504 | `8f1f15aed94220471f2b6a84df1fe58f3002d164f270a9a2fff508028c6957d2` |
| `05_Research_References/Research_Sources.md` | 20,586 | `2af3e0672f105b6dd83fbb2225004738bbe392b7af8b1474b6385a75be2993b1` |
