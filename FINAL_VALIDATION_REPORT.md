# FINAL VALIDATION REPORT — RSA ACADEMIC REPORT QA

**Project Title:** Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication  
**Repository:** `https://github.com/nguyendanghoang1602/Crypto`  
**Branch:** `rsa-final-qa-2026-11-04`  
**Audit Date:** November 5, 2026  
**Auditing Panel:** Senior Cryptography Researcher, Academic Reviewer, Blockchain Security Engineer, and QA Specialist  

---

## 1. REPOSITORY & WORKSPACE VERIFICATION

- **Authoritative Git Repository:** `D:\Crypto_repo` (verified via `git rev-parse --show-toplevel`)
- **Remote Origin URL:** `https://github.com/nguyendanghoang1602/Crypto.git` (verified via `git remote get-url origin`)
- **Workspace Clarification:** `D:\Crypto` is a local directory clone without `.git` metadata; `D:\Crypto_repo` is the authoritative Git tracking repository.

---

## 2. COMPREHENSIVE AUDIT & CONTENT MERGE SUMMARY

The final academic release consolidates and elevates Version A (local review baseline) and Version B (GitHub release candidate):

1. **Independent Evaluation (Phase 1):** Completed in `COMPARATIVE_QUALITY_ASSESSMENT.md`. Version B (9.535 / 10 weighted score) was selected as baseline over Version A (7.885 / 10), preserving all valuable theoretical and mathematical content.
2. **Mathematical Foundations (Phase 3 & 6):**
   - Formalized the theoretical distinction between the **Integer Factorization Problem (IFP)** and the **RSA Inversion Problem (RSAP)**. Table 1 Row 1 updated to *"Integer Factorization (IFP) / RSA Inversion Problem"*.
   - Extended Euclidean Algorithm solving Bézout's identity $e \cdot d + k \cdot \phi(n) = 1$.
   - Chinese Remainder Theorem (CRT) optimization ($4\times$ speedup) and Euler's totient theorem.
   - Textbook RSA multiplicative homomorphism: $(m_1)^e \cdot (m_2)^e \equiv (m_1 \cdot m_2)^e \pmod n$.
3. **RSA-OAEP & RSA-PSS Rigor (Phase 3 & 6):**
   - RSA-OAEP: Documented IND-CCA2 security reduction history in ROM (Bellare-Rogaway 1994, Shoup 2001, Fujisaki et al. 2001). Correct key wrapping terminology: *"encrypting (wrapping) an ephemeral 256-bit AES key using RSA-OAEP to protect bulk data authenticated with AES-GCM (NIST SP 800-38D [22]), maintaining distinction from KEM encapsulation (such as ML-KEM in RFC 10024 [19])"*.
   - RSA-PSS: Attributed foundational theoretical EUF-CMA proof in ROM to Bellare and Rogaway (EUROCRYPT '96 [23]). Clarified that SHA-256 provides a fixed-length digest-derived encoding that fits the modulus, while structured EMSA-PSS encoding and verification prevent algebraic attacks.
4. **Key Separation & TLS 1.3 PKI (Phase 3 & 6):**
   - Grounded NIST FIPS 186-5 Section 5.1 [4] key separation in preventing cross-protocol interactions, enforcing purpose separation, and reducing compromise impact.
   - Deconstructed TLS 1.3: (i) X.509 CA identity binding; (ii) `CertificateVerify` transcript signing; and (iii) RFC 9846 [3] RSA-PSS server mandate (CA signature is separate and not required to be RSA-PSS), with RFC 9963 [18] client legacy exceptions preserved.
5. **Blockchain Technical Modeling (Phase 3 & 6):**
   - Delineated sub-exponential GNFS from fully exponential Pollard's rho $\mathcal{O}(\sqrt{q})$ in cyclic group of prime order $q$.
   - Explicit simplified 256-byte modulus assumption ($1 + 3 + 256 + 3 + 256 = 519\text{ bytes}$, $+410\text{–}412\text{ bytes}$, $+103\text{ vB}$, $\approx 73\%$ increase over 141-vB baseline P2WPKH).
   - Scoped MuSig2 (BIP 327 [10]) to native compact signature aggregation. Explicitly cited BIP 341 [27], ERC-2098 [28], and EIP-198 [29].
6. **Side-Channel & Fault Attacks (Phase 3):**
   - Bellcore CRT hardware fault attack (Boneh et al., 2001 [7]): formulated single-fault ($p = \gcd((s')^e - m, n)$) and two-signature fault conditions. Clarified why base blinding defends against timing attacks but not CRT faults; fault mitigation mandates post-computation verification ($s^e \bmod n == m$).
7. **Implementation Architecture & Trust Boundaries (Phase 4 & 6):**
   - Algorithm 1 annotated with explicit trust boundaries: (1) Internal Secure Signer Service; (2) Network Transit; and (3) Edge Verification Gateway.
   - Calibrated production considerations: cryptographic modules validated under FIPS 140-3 [25], durable shared atomic nonce check-and-insert (Redis SETNX / SQL unique constraints), MFA and OpenID Connect [26].
   - Specified withdrawal amount in Scenario 1 as integer amount in wei ($12,500,000,000,000,000,000$ wei).
8. **Restrained Wycheproof Interpretation (Phase 4):**
   - 108/108 passing test vectors reframed as demonstrating agreement with that selected test set without claiming full protocol certification or absence of all vulnerabilities.
9. **Comprehensive 29-Reference Bibliography (Phase 5):**
   - Fully cataloged and verified in `REFERENCE_AUDIT.md`, adding formal entries [24]–[29] for RFC 8785 [24], FIPS 140-3 [25], OpenID Connect [26], BIP 341 [27], ERC-2098 [28], and EIP-198 [29].

---

## 3. BENCHMARK DATASET INTEGRITY & MEASUREMENT COUNT

The empirical benchmark dataset in `03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv` and `benchmark_results.csv` contains exactly **840 raw measurements** with the following verified structure:

- **4 Algorithm Configurations:** RSA-2048, RSA-3072, RSA-4096, and ECDSA-secp256k1.
- **Trial Distribution per Algorithm:**
  - Key-generation: 10 measurements per algorithm ($4 \times 10 = 40\text{ measurements}$).
  - Signature generation: 100 measurements per algorithm ($4 \times 100 = 400\text{ measurements}$).
  - Signature verification: 100 measurements per algorithm ($4 \times 100 = 400\text{ measurements}$).
- **Aggregate Total:** $40 + 400 + 400 = 840\text{ measurements}$.

---

## 4. DOCUMENT LAYOUT & VERIFICATION METRICS

- **Primary Word Document:** Exactly **5 A4 pages** (`doc.ComputeStatistics(2) == 5`).
- **Rendered PDF Document:** Exactly **5 Pages** (`len(pdf) == 5`).
- **Word Count:** **4,939 words** across 144 paragraphs.
- **Page-by-Page Structural Distribution:**
  - **Page 1:** Title, Metadata, Abstract, Keywords, Section 1 (Introduction), Section 2.1 (Math Foundations).
  - **Page 2:** Section 2.2 (OAEP vs. PSS, FIPS 186-5 Key Separation), Figure 1 (RSA-PSS Workflow), Section 2.3 (Applications), Section 3 (Why RSA?), Table 1 (Comparison Matrix + Caption), Section 3.1 start.
  - **Page 3:** Section 3.1 (Blockchain Trade-offs), Section 3.2 (Operational Value, CRT Faults), Section 4 (Proposed Design), Section 4.1 (Component Decomposition), Figure 2 (Architecture Diagram + Caption).
  - **Page 4:** Section 4.2 (Deterministic JSON), Algorithm 1 (Unified Box with Trust Boundaries), Section 4.3 (Prototype Scope), Section 5 (Experimental Results), Section 5.1 (Scenarios), Section 5.2 (Wycheproof), Section 5.3 (Benchmark Intro), Table 2 Caption, Table 2 (All 4 rows unified).
  - **Page 5:** Figure 3 (Performance Chart + Caption), Performance Discussion (3 points), Section 6 (Conclusion), Section 7 (References [1]–[29] concluding cleanly).
- **Wycheproof Compliance:** **108 / 108 test cases passing** (63 valid accepted, 45 invalid rejected, 0 failures).
- **Operational Scenarios:** 5 / 5 target security scenarios validated.
- **Protected File Status:** `rsa_pss_experiment.py`, `generate_figures.py`, `benchmark_results.csv`, `raw_trials_all_algorithms.csv`, figure images, and Wycheproof test vectors remain **100% UNMODIFIED**.

---

## 5. DELIVERABLE ARTIFACT CHECKSUMS (SHA-256)

| Deliverable File | Size (Bytes) | SHA-256 Hash |
| :--- | :--- | :--- |
| `01_Final_Report/RSA_Real_World_Applications_Report_FINAL.docx` | 456,896 | `b62d9f4d53e18d2d2a4b2aeecea06ebd0f9253909ef32dec4d7e9e814adea250` |
| `01_Final_Report/RSA_Real_World_Applications_Report_FINAL.pdf` | 452,538 | `b8393e09608a1a3ac9d13952cd5615776e209da05d83cb7cfbc299496b9dccaa` |
| `01_Final_Report/RSA_Real_World_Applications_Report.docx` | 456,896 | `b62d9f4d53e18d2d2a4b2aeecea06ebd0f9253909ef32dec4d7e9e814adea250` |
| `01_Final_Report/RSA_Real_World_Applications_Report.pdf` | 452,538 | `b8393e09608a1a3ac9d13952cd5615776e209da05d83cb7cfbc299496b9dccaa` |
| `02_Source_Code/build_report_doc.py` | 61,730 | `6b72fa998a5eb7c6dc019390966184b5de849d88f6fe76259bcc6ebee9de5d06` |
| `05_Research_References/Research_Sources.md` | 25,603 | `5a45e4b2a9c461211da1ad4b37fce3eab02db7d182d0d909332662b4e33e2dea` |
| `COMPARATIVE_QUALITY_ASSESSMENT.md` | 13,521 | `ba4b55aef16bf856d7f2b5fbf05f5fa122ca640871dd515e4024b5ddfeb34d55` |
| `CONTENT_MERGE_CHANGELOG.md` | 9,255 | `3f8e9aae9061619998a4ad224273176a0778271fe07a3b33f68a67451a349b23` |
| `TECHNICAL_ISSUE_REGISTER.md` | 18,223 | `439f9983f425fbf27d5807b70ae640c5dd54706583b7a364aa71081bb10d680c` |
| `REFERENCE_AUDIT.md` | 11,752 | `3f21ce8d15a91bc0203e2873fbe275bd02aa568748d8483e0545cc8ee0707543` |
