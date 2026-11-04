# COMPARATIVE QUALITY ASSESSMENT — RSA RESEARCH REPORT

**Evaluation Subject:** Academic Research Report  
**Title:** *Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication*  
**Date of Audit:** November 5, 2026  
**Auditing Panel:**  
1. Senior Cryptography Researcher  
2. Academic Research Paper Reviewer  
3. RSA, RSA-OAEP, RSA-PSS Security Specialist  
4. Blockchain and Cryptocurrency Security Engineer  
5. Python Cryptographic Implementation Auditor  
6. Technical Editor and Scientific Document Quality Assurance Specialist  

---

## 1. EXECUTIVE SUMMARY & INVENTORY

Two primary document revisions of the research report were inventoried and audited line-by-line:

- **VERSION A (Local Baseline / Transitional Review Version):**
  - Path: `D:\Crypto\RSA_Real_World_Applications_Report.docx` / `D:\Crypto\RSA_Project_Review_Final\01_Final_Report\RSA_Real_World_Applications_Report.docx`
  - Size: 455,500 bytes | SHA-256: `f81706a844b906448c4168a6dac4bc1cdaa71dad26f5456ffff33a31856d3df6`
  - Word Count: 3,860 body words (67 non-empty paragraphs)
  - References: 22 references ([1]–[22])
- **VERSION B (GitHub Release Candidate on `rsa-final-qa-2026-11-04`, Commit `59b1703`):**
  - Path: `D:\Crypto_repo\01_Final_Report\RSA_Real_World_Applications_Report.docx`
  - Size: 456,097 bytes | SHA-256: `bd22edd278447aacd99c4217a2b8927ba70a4b2156af615efcf78f229323fe68`
  - Word Count: 4,094 body words (4,688 total words including headers/tables across 138 paragraphs)
  - References: 23 references ([1]–[23])

---

## 2. INDEPENDENT SCORING MATRIX (10-POINT SCALE)

Both versions were evaluated against the weighted academic criteria defined in Phase 1:

| Evaluation Criterion | Weight | Version A Score | Version A Weighted | Version B Score | Version B Weighted | Evaluation Rationale & Distinctions |
|---|:---:|:---:|:---:|:---:|:---:|---|
| **1. Cryptographic Mathematical Correctness** | 20% | 7.8 / 10 | 1.56 | **9.6 / 10** | **1.92** | Version A omits Bézout's identity for $e \cdot d + k \cdot \phi(n) = 1$, lacks the CRT quintuple derivation and $4\times$ speedup proof, inaccurately claims SHA-256 prevents modular overflow, and conflates operation counts between modular multiplications and ECC group additions. Version B provides rigorous derivations, exact mathematical formulations of the Extended Euclidean Algorithm, and precise distinction of the algebraic recovery equation for ECDSA nonce reuse ($s_1 - s_2 \equiv k^{-1}(z_1 - z_2) \pmod n$). |
| **2. Academic Rigor and Theoretical Depth** | 20% | 7.2 / 10 | 1.44 | **9.5 / 10** | **1.90** | Version A fails to cite the foundational Bellare-Rogaway 1996 paper [23] for RSA-PSS provable security in the Random Oracle Model (ROM), incorrectly attributing the tight proof to RFC 8017. Version B rigorously delineates the engineering standard (RFC 8017 / FIPS 186-5) from theoretical reductions in ROM (Bellare-Rogaway 1996 [23]), while properly presenting the IND-CCA2 history of RSA-OAEP (Bellare-Rogaway 1994, Shoup 2001, Fujisaki et al. 2001). |
| **3. Technical Accuracy and Standards Compliance** | 15% | 7.5 / 10 | 1.125 | **9.4 / 10** | **1.41** | Version A uses imprecise terminology ("256-bit AES-GCM", "HSMs, e.g., FIPS 140-3", and presents FIPS 186-5 key separation with unproven overbroad claims). Version B uses exact phrasing ("a 256-bit AES key used with AES-GCM", cryptographic modules validated under FIPS 140-3, calibrated key separation rationale, and delineates KEM encapsulation from RSA key wrapping). |
| **4. Research Structure and Logical Coherence** | 10% | 8.8 / 10 | 0.88 | **9.6 / 10** | **0.96** | Both versions preserve the approved WHAT–WHY–HOW pedagogy. However, Version B introduces Section 1 with the four information assurance objectives and Kerckhoffs's principle, creating a tighter logical foundation. |
| **5. Experimental Methodology and Reproducibility** | 15% | 8.2 / 10 | 1.23 | **9.5 / 10** | **1.425** | Version A uses vague financial units ("12.5 ETH atomic units") and overly strong claims regarding Wycheproof ("validating execution against this selected verification suite"). Version B specifies exact integer units in wei ($12,500,000,000,000,000,000$ wei) and provides calibrated interpretation of the 108 Wycheproof test vectors. |
| **6. Citation Quality and Academic Integrity** | 10% | 8.0 / 10 | 0.80 | **9.6 / 10** | **0.96** | Version A has 22 references, omitting Bellare-Rogaway 1996. Version B has 23 fully verified references with active DOIs and RFC URLs, synchronized with in-text callouts. |
| **7. Document Formatting and Presentation** | 10% | 8.5 / 10 | 0.85 | **9.6 / 10** | **0.96** | Version A suffered from layout instability in transitional iterations. Version B achieves a clean 5 A4 page layout with all 4 rows of Table 2 unified on Page 4 and Algorithm 1 unified in a boxed container. |
| **TOTAL WEIGHTED SCORE** | **100%** | — | **7.885 / 10** | — | **9.535 / 10** | **Version B clearly outperforms Version A across all technical and academic dimensions.** |

---

## 3. COMPREHENSIVE COMPARATIVE INVENTORY

### 3.1. Strengths and Weaknesses of Version A
- **Strengths:**
  - Preserved the fundamental WHAT–WHY–HOW structural scaffolding.
  - Successfully maintained the 840-measurement benchmark baseline and 108 Wycheproof vector results.
  - Included the core educational prototype description and five operational security test scenarios.
- **Weaknesses:**
  - Incomplete mathematical foundations in Section 2.1 (omitted Extended Euclidean Algorithm solving Bézout's identity $e \cdot d + k \cdot \phi(n) = 1$ and CRT parameter derivations).
  - Inaccurate attribution of the RSA-PSS tight security reduction to RFC 8017 rather than Bellare & Rogaway (1996).
  - Inaccurate terminology ("preventing modular overflow", "256-bit AES-GCM", "HSMs, e.g., FIPS 140-3").
  - Conflated ECDSA nonce reuse with slight nonce bias without providing the algebraic recovery derivation.
  - Vague financial unit phrasing ("12.5 ETH atomic units") that obscured integer representation in wei.
  - Overstated Wycheproof test suite authority.

### 3.2. Strengths and Weaknesses of Version B
- **Strengths:**
  - Rigorous mathematical framing aligned with University Course Sessions 1–7.
  - Correct theoretical citation of Bellare and Rogaway (EUROCRYPT '96 [23]) for the tight EUF-CMA reduction in the Random Oracle Model.
  - Disentangled three distinct concepts in TLS 1.3 authentication (X.509 binding, `CertificateVerify`, and RSA-PSS server mandate).
  - Rigorous differentiation of exact ECDSA nonce reuse from lattice-based Hidden Number Problem attacks for slight bias.
  - Exact financial representation in wei ($12,500,000,000,000,000,000$ wei).
  - Proper key wrapping terminology ("encrypting (wrapping) an ephemeral 256-bit AES key using RSA-OAEP") distinct from KEM encapsulation.
  - Stable 5-page A4 typography with zero split table rows.
- **Weaknesses Identified for Resolution in Phase 6:**
  - Table 1 listed the hard problem of RSA simply as "Factoring" without formalizing the theoretical separation between the Integer Factorization Problem (IFP) and the RSA Inversion Problem (RSAP).
  - MuSig2 aggregation capability was stated broadly without explicitly scoping it to native compact on-chain signature aggregation versus standard RSASSA-PSS.
  - Algorithm 1 did not explicitly annotate architectural trust boundaries, private-key isolation, and edge verification steps.
  - Mentions of technical standards (RFC 8785, FIPS 140-3, OpenID Connect, BIP 341, ERC-2098, EIP-198) lacked formal numbered bibliographic citations in Section 7.

---

## 4. DETAILED CONTENT COMPARISON & MERGE DIRECTIVES

| Document Section | Version A Text | Version B Text | Comparison & Merge Decision |
|---|---|---|---|
| **Section 1 (Introduction)** | Opens immediately with RSA history (Rivest, Shamir, Adleman 1977/1978). | Introduces the 4 information assurance goals (Confidentiality, Integrity, Authenticity, Non-Repudiation) and Kerckhoffs's principle before introducing RSA. | **Adopt Version B:** Provides foundational academic framing aligned with Course Session 2 and classical cryptography principles. |
| **Section 2.1 (Math Foundations)** | Mentions factoring $n = p \cdot q$ and Euler totient; omits Bézout's identity and CRT formulas. | Explicitly includes Bézout's identity $e \cdot d + k \cdot \phi(n) = 1$, Extended Euclidean Algorithm, CRT parameter quintuple $(p, q, d_p, d_q, q_{inv})$, and multiplicative homomorphism $(m_1)^e \cdot (m_2)^e \equiv (m_1 \cdot m_2)^e \pmod n$. | **Adopt Version B:** Retains essential number-theoretic depth aligned with Course Sessions 1 and 6. |
| **Section 2.2 (OAEP vs. PSS)** | Inaccurate PSS attribution to RFC 8017; claims SHA-256 "prevents modular overflow"; uses "encapsulating 256-bit AES-GCM". | Cites Bellare-Rogaway 1996 [23]; explains SHA-256 provides fixed-length digest-derived encoding fitting modulus; uses "encrypting (wrapping) an ephemeral 256-bit AES key using RSA-OAEP". | **Adopt Version B:** Corrects all academic and standards attributions; preserves KEM distinction. |
| **Section 2.3 (Applications)** | Conflates X.509 certificate signatures with `CertificateVerify`. | Disentangles CA signature, `CertificateVerify` transcript signing, and RFC 9846 server RSA-PSS mandate. | **Adopt Version B:** Technologically precise analysis of TLS 1.3 PKI semantics. |
| **Section 3.1 (Blockchain Trade-offs)** | Assumes super-linear GNFS without explaining Pollard's rho group complexity; omits explicit simplified assumption for 256-byte modulus. | Delineates sub-exponential GNFS from fully exponential Pollard's rho $\mathcal{O}(\sqrt{q})$ in cyclic group of order $q$; formulates explicit simplified 256-byte modulus payload assumption. | **Adopt Version B:** Mathematically sound complexity comparison and transparent witness modeling. |
| **Section 3.2 (Operational Value & Faults)** | Claims ECDSA nonce reuse or slight bias allows direct algebraic recovery; direct comparison of primitive operation counts. | Distinguishes algebraic recovery equation for exact nonce reuse from lattice HNP attacks for bias; notes modular multiplications and curve additions cannot be directly equated; validates empirically via benchmarks. | **Adopt Version B:** Accurate cryptanalytic categorization. |
| **Section 4.2 & Algorithm 1** | Standard pseudocode without trust boundaries. | Standard pseudocode with parameterized `emBits`. | **Merge & Enhance:** Augment Version B's algorithm with explicit trust boundaries (Internal Secure Signer Service vs. Network Transit vs. Verification Edge Gateway). |
| **Section 4.3 (Prototype Scope)** | Uses absolute language ("mandatory production requirements", "HSMs, e.g., FIPS 140-3", "OAuth"). | Calibrated phrasing: cryptographic modules validated under FIPS 140-3, durable shared atomic check-and-insert, MFA and OpenID Connect. | **Adopt Version B:** Professional qualification distinguishing educational prototype from production exchange. |
| **Section 5.1 (Scenarios)** | "Valid request (12.5 ETH atomic units)". | "Valid request of 12.5 ETH, represented as an integer amount in wei ($12,500,000,000,000,000,000$ wei)". | **Adopt Version B:** Eliminates ambiguity between token units and integer atomic units. |
| **Section 5.2 (Wycheproof)** | "validating execution against this selected verification suite". | Calibrated: demonstrates agreement with the selected 108 test vectors without claiming full protocol certification or absence of all vulnerabilities. | **Adopt Version B:** Restrained, academically defensible interpretation. |
| **Table 1 (Comparison Matrix)** | Row 1 lists "Factoring" for RSA. | Row 1 lists "Factoring". | **Rewrite in Final Report:** Expand to "Integer Factorization (IFP) / RSA Inversion Problem" to reflect theoretical distinction. |
| **Section 7 (References)** | 22 references ([1]–[22]). | 23 references ([1]–[23]). | **Expand to 29 References:** Retain all 23 references and add formal entries for RFC 8785 [24], FIPS 140-3 [25], OpenID Connect Core 1.0 [26], BIP 341 [27], ERC-2098 [28], and EIP-198 [29]. |

---

## 5. BASELINE SELECTION & STRATEGIC MERGE DECISION

### Professional Determination:
**Version B is selected as the primary baseline foundation**, supplemented by targeted enhancements from the Phase 3, 5, and 6 technical audits:

1. **Academic Superiority:** Version B already incorporates the critical cryptographic fixes identified across previous audit rounds (Bellare-Rogaway 1996 PSS proof, Bézout's identity, GNFS vs. Pollard's rho, ECDSA exact reuse vs. bias, and TLS 1.3 transcript signing).
2. **Harmonious Synthesis:** No valuable technical content from Version A is lost, as Version B represents a strictly more rigorous, academically complete evolution of Version A.
3. **Comprehensive Closure:** The final merged report (`RSA_Real_World_Applications_Report_FINAL.docx`) will build directly on Version B, resolving the remaining Phase 6 items:
   - Formally defining the hard problem in Table 1 as "Integer Factorization (IFP) / RSA Inversion Problem".
   - Calibrating the MuSig2 aggregation statement.
   - Structuring Algorithm 1 with explicit trust boundaries.
   - Expanding the formal bibliography to 29 entries, providing authoritative citations for all referenced standards (RFC 8785, FIPS 140-3, OIDC, BIP 341, ERC-2098, EIP-198).
   - Preserving the flawless 5-page A4 presentation.
