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

## 2. SUMMARY OF ACADEMIC CORRECTIONS (FINAL AUDIT)

The final academic revision incorporates all 12 required technical corrections across theory, engineering, and course alignment:

1. **RSA-PSS Security Proof (Reference [23]):** Added Bellare and Rogaway (EUROCRYPT '96, LNCS 1070 [23]) as the original academic source proving the essentially tight security reduction of RSA-PSS to the RSA inversion problem in the Random Oracle Model (ROM). Clarified that RFC 8017 [2] specifies the engineering standard, distinct from Bellare-Rogaway EUROCRYPT '94 (OAEP, [17]).
2. **SHA-256 vs. Homomorphic Forgery:** Explicitly clarified that SHA-256 provides a fixed-length digest and makes signing long messages practical, but hashing alone does not eliminate textbook RSA's multiplicative homomorphism. EUF-CMA security is provided by RSA-PSS's structured encoding (EMSA-PSS), randomized salt, and verification process.
3. **AES-GCM Key Transport Terminology:** Corrected phrasing to "a 256-bit AES key used with AES-GCM" (NIST SP 800-38D [22]), maintaining the distinction between asymmetric key transport (RSA-OAEP) and symmetric bulk authenticated encryption.
4. **TLS 1.3 Certificate Authentication:** Disentangled three distinct concepts: (i) X.509 certificate identity binding via CA signature; (ii) CertificateVerify proving private-key possession over the handshake transcript; and (iii) RFC 9846 [3] strictly requiring RSA-PSS for CertificateVerify when RSA server keys are used (the CA signature itself is not required to be RSA-PSS), with RFC 9963 [18] legacy client exceptions preserved.
5. **ECDSA Nonce Hazards vs. Nonce Bias:** Delineated exact nonce reuse ($s_1 - s_2 \equiv k^{-1}(z_1 - z_2) \pmod n$) allowing direct two-signature algebraic recovery from slight nonce bias/leakage, which requires multiple signatures and lattice-based Hidden Number Problem (HNP) techniques.
6. **RSA Public Exponent:** Replaced rigid standard assertions with "commonly chosen as 65,537, which is a Fermat prime ($e = 2^{16} + 1$)."
7. **GNFS vs. Pollard's Rho:** Clarified that GNFS has sub-exponential complexity for factoring $n=p\cdot q$, whereas Pollard's rho has expected fully exponential complexity $\mathcal{O}(\sqrt{q})$ in a cyclic group of prime order $q$, explaining why RSA requires substantially larger keys (RSA-3072 $\approx$ 128-bit) per NIST SP 800-56B [5] and SP 800-57 [6].
8. **Theoretical Operation Counts vs. Empirical Latency:** Clarified that modular multiplications and ECC group additions represent distinct primitive operations whose counts cannot be directly equated, validating performance conclusions empirically via measured benchmark latency.
9. **Restrained Wycheproof Interpretation:** Reframed the bundled 108-vector test suite as demonstrating agreement with that selected test set (63 valid accepted, 45 invalid rejected) rather than claiming full protocol certification or absence of all vulnerabilities.
10. **ETH Atomic Units:** Corrected description to "Valid request of 12.5 ETH, represented as an integer amount in wei (12,500,000,000,000,000,000 wei)."
11. **Key Separation Rationale:** Grounded NIST FIPS 186-5 Section 5.1 [4] key separation in preventing cross-protocol interactions, enforcing cryptographic purpose separation, and reducing compromise impact, without overbroad theoretical claims.
12. **Production Security Requirements:** Reframed HSMs, PKI, revocation, and Redis/SQL distributed replay mechanisms as production architecture requirements appropriate to the system; refined authentication terminology to MFA and OpenID Connect.

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

| Reference | Standard / Literature | In-Text Citation Location | Bibliography Status | Verified |
| :--- | :--- | :--- | :--- | :---: |
| **[1]** | Rivest, Shamir, & Adleman (1978/1977) | Section 1, Section 2.1 | CACM / MIT Memorandum | **YES** |
| **[2]** | PKCS #1 v2.2 (RFC 8017) | Section 1, Section 2.1, Section 2.2 | IETF Informational | **YES** |
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
| **[23]** | Exact Security of Signatures (Bellare-Rogaway, 1996) | Section 2.2 | EUROCRYPT '96 / LNCS 1070 | **YES** |

---

## 5. DOCUMENT LAYOUT & VERIFICATION METRICS

- **Primary Word Document:** Exactly **5 A4 pages** (`doc.ComputeStatistics(2) == 5`).
- **Rendered PDF Document:** Exactly **5 Pages** (`len(pdf) == 5`).
- **Word Count:** **4,646 words**.
- **Page-by-Page Structural Distribution:**
  - **Page 1:** Title, Metadata, Abstract, Keywords, Section 1 (Introduction), Section 2.1 (Math Foundations).
  - **Page 2:** Section 2.2 (OAEP vs. PSS, Key Separation), Figure 1 (RSA-PSS Workflow), Section 2.3 (Applications), Section 3 (Why RSA?), Table 1 (Comparison Table + Caption), Section 3.1 start.
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
| `01_Final_Report/RSA_Real_World_Applications_Report.docx` | 456,030 | `c30f3e6ab7a5737233833fc3825bfff1f319976e6c8dd7a3c919e024494ae227` |
| `01_Final_Report/RSA_Real_World_Applications_Report.pdf` | 447,989 | `a6fb7c38198eea8864588d947ee5b5afcd110006c99fc6cfb63a513928d347f0` |
| `02_Source_Code/build_report_doc.py` | 59,134 | `11016ab7cb1b6dec58b6176c1631e376306c942046c42c43eebb655459d0d157` |
| `05_Research_References/Research_Sources.md` | 21,982 | `549eed32cb7aabd1a71812f96ccc3ef13a96af84de7d69e7762a7b10c9758336` |
