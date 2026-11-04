# CONTENT MERGE CHANGELOG — RSA RESEARCH REPORT

**Project Title:** *Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication*  
**Date:** November 5, 2026  
**Auditing Panel:** Academic Research Paper Reviewer and Technical Editor  
**Input Revisions:**  
- **Version A:** Local review baseline (`D:\Crypto\RSA_Real_World_Applications_Report.docx`, 3,860 words, 22 references)  
- **Version B:** GitHub release candidate (`D:\Crypto_repo\01_Final_Report\RSA_Real_World_Applications_Report.docx`, 4,094 words, 23 references)  
**Output Deliverable:** `RSA_Real_World_Applications_Report_FINAL.docx` (4,750+ words, 29 references)  

---

## 1. STRATEGIC MERGE METHODOLOGY

Rather than a mechanical concatenation of text blocks, the synthesis was conducted under three guiding principles:
1. **Academic Maximization:** Retain the most rigorous theoretical explanation and exact mathematical formulations.
2. **Pedagogical Integrity:** Preserve the established WHAT–WHY–HOW structural narrative.
3. **Standards Strictness:** Ensure 100% compliance with authoritative IETF, NIST, and blockchain specifications, with every referenced standard carrying an official citation.

---

## 2. SECTION-BY-SECTION MERGE RECORD

### Preamble & Abstract
- **Title & Metadata:** Preserved the approved title: *"Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication"*.
- **Abstract Synthesis:**
  - *Version A Text:* Claimed "validating execution against this selected verification suite".
  - *Version B Text:* Adopted restrained wording: *"demonstrating agreement with this test set without establishing complete protocol certification"*.
  - *Merged Result:* Retained Version B's calibrated framing, exact empirical ratios (RSA-2048 13.45x faster verification; RSA-3072 8.22x faster verification vs. ECDSA), and 128-bit security comparison.

### Section 1: Introduction and Research Scope
- *Merge Action:* Fully incorporated Version B's introductory framing of the four core information assurance goals (Confidentiality, Integrity, Authenticity, Non-Repudiation Evidence) and Kerckhoffs's principle.
- *Preserved Elements:* Historical attribution of RSA (April 1977 MIT memorandum / 1978 CACM publication [1]), PKI authentication requirements, and the three-pillar research roadmap (WHAT, WHY, HOW).

### Section 2: RSA Fundamentals and Real-World Applications
- **Section 2.1 (Mathematical Foundations & Operating Mechanics):**
  - *From Version B:* Added the Extended Euclidean Algorithm solving Bézout's identity $e \cdot d + k \cdot \phi(n) = 1$, Chinese Remainder Theorem (CRT) parameter quintuple $(p, q, d_p, d_q, q_{inv})$ providing $\approx 4\times$ modular exponentiation acceleration, and Euler's totient theorem.
  - *From Version B:* Formulated the multiplicative homomorphic flaw of textbook RSA: $(m_1)^e \cdot (m_2)^e \equiv (m_1 \cdot m_2)^e \pmod n$.
  - *Enhancement:* Explicitly distinguished the Integer Factorization Problem (IFP) from the RSA Inversion Problem (RSAP).
- **Section 2.2 (Distinction Between RSA Encryption and RSA Digital Signatures):**
  - *RSA-OAEP Key Transport:* Retained the IND-CCA2 security reduction history in the Random Oracle Model (Bellare-Rogaway 1994/1995 [17], Shoup 2001/2002 [15], Fujisaki et al. 2001/2004 [16]), maximum payload boundary ($mLen \le k - 2hLen - 2 = 190\text{ bytes}$ for RSA-2048 with SHA-256), and hybrid key transport terminology: *"encrypting (wrapping) an ephemeral 256-bit AES key using RSA-OAEP to protect bulk data authenticated with AES-GCM (NIST SP 800-38D [22]), maintaining the distinction between RSA key transport and KEM encapsulation (such as ML-KEM in RFC 10024 [19])"*.
  - *RSA-PSS Digital Signatures:* Replaced "preventing modular overflow" with exact modulus fitting explanation; cited Bellare and Rogaway (EUROCRYPT '96 [23]) for the tight EUF-CMA security reduction in ROM; detailed full EMSA-PSS verification versus modular exponentiation alone.
  - *Key Separation:* Grounded NIST FIPS 186-5 Section 5.1 [4] in cross-protocol interaction defense and purpose separation.
- **Section 2.3 (Real-World Application Breadth):**
  - Disentangled X.509 identity binding, `CertificateVerify` transcript signing, and the RFC 9846 [3] RSA-PSS server mandate, while preserving RFC 9963 [18] client legacy exceptions.

### Section 3: Why RSA? Security Purpose and Comparative Evaluation
- **Table 1 (Comparison Matrix):**
  - *Enhancement:* Updated Row 1 ("Hard Problem") from simple "Factoring" to *"Integer Factorization (IFP) / RSA Inversion Problem"*.
  - *Enhancement:* Explicitly cited BIP 341 [27], ERC-2098 [28], and RFC 8032 [11] in Table 1 cells.
  - *Enhancement:* Calibrated MuSig2 [10] cell to specify native compact threshold aggregation.
- **Section 3.1 (Storage and Verification Trade-Offs in Blockchains):**
  - Sub-exponential GNFS vs. fully exponential Pollard's rho $\mathcal{O}(\sqrt{q})$ in cyclic group of prime order $q$.
  - Formulated the explicit simplified assumption for the hypothetical 256-byte modulus payload ($1 + 3 + 256 + 3 + 256 = 519\text{ bytes}$, $+410\text{–}412\text{ bytes}$, $+103\text{ vB}$, $\approx 73\%$ increase over 141-vB baseline P2WPKH).
  - Explicitly cited BIP 341 [27], ERC-2098 [28], and EIP-198 [29] (EVM precompile 0x05).
- **Section 3.2 (Operational Value in Off-Chain Systems):**
  - Clarified that 17 modular operations vs. ~256 ECC point operations are distinct operation types whose performance is verified empirically via benchmarks.
  - Delineated the algebraic recovery formula for exact ECDSA nonce reuse from lattice HNP attacks for slight bias.
  - Formulated both single-fault and two-signature Bellcore CRT fault attack scenarios (Boneh et al. [7]), clarifying why base blinding protects against timing attacks but not CRT faults.

### Section 4: Proposed System Design and Implementation
- **Section 4.1 & Figure 2:** Preserved off-chain withdrawal architecture and 4-tier component decomposition.
- **Section 4.2 & Algorithm 1:**
  - Integrated formal citation to RFC 8785 [24] for JSON canonicalization principles.
  - Refined Algorithm 1 with explicit structural annotations:
    - *Internal Secure Signer Service Boundary* (private key isolation).
    - *Network Transit Boundary* (payload and signature transmission).
    - *Edge Verification Gateway Boundary* (public key retrieval, signature verification, timestamp freshness, and replay interception).
- **Section 4.3 (Prototype Scope & Security Considerations):**
  - Grounded private key custody in cryptographic modules validated under FIPS 140-3 [25].
  - Calibrated distributed replay protection to durable shared atomic mechanisms (Redis SETNX / SQL unique constraints).
  - Refined customer authentication terminology to MFA and OpenID Connect [26].

### Section 5: Experimental Results and Analysis
- **Section 5.1 (Adversarial Security Scenarios):** Explicitly expressed withdrawal amount in Scenario 1 as *"12.5 ETH, represented as an integer amount in wei ($12,500,000,000,000,000,000$ wei)"*.
- **Section 5.2 (Wycheproof Validation):** Preserved 108/108 pass rate with calibrated academic interpretation.
- **Section 5.3 & Table 2:** Preserved empirical benchmark values (840 measurements total) with unified table formatting.

### Section 6: Conclusion
- Preserved findings and post-quantum migration recommendations to NIST FIPS 204 (ML-DSA [20]) and FIPS 205 (SLH-DSA [21]).

### Section 7: References
- Expanded from 22/23 references to **29 verified primary technical references** ([1]–[29]), resolving all uncited standards across the entire document.

---

## 3. SUMMARY OF ELIMINATED DEFICIENCIES

| Deficient Phrasing / Inaccuracy | Version Found In | Final Corrected Resolution |
|---|:---:|---|
| "preventing modular overflow" | Version A & early B | "allowing RSA-PSS to operate on a fixed-length digest-derived encoding that fits the RSA modulus" |
| Tight PSS proof attributed to RFC 8017 | Version A | Attributed to Bellare & Rogaway (EUROCRYPT '96 [23]) in ROM |
| "256-bit AES-GCM" | Version A | "a 256-bit AES key used with AES-GCM (NIST SP 800-38D [22])" |
| "encapsulating an ephemeral key" (for RSA-OAEP) | Version A & early B | "encrypting (wrapping) an ephemeral 256-bit AES key using RSA-OAEP" |
| Conflation of X.509 CA signature with `CertificateVerify` | Version A | Disentangled CA identity binding, transcript signing, and RFC 9846 mandate |
| Conflation of ECDSA nonce reuse with slight bias | Version A | Separated algebraic two-signature recovery from lattice HNP attacks |
| Direct equivalence of modular vs. ECC primitive counts | Version A | Explicitly qualified as distinct operation types; validated via benchmarks |
| "12.5 ETH atomic units" | Version A | "12.5 ETH, represented as an integer amount in wei ($12,500,000,000,000,000,000$ wei)" |
| "HSMs, e.g., FIPS 140-3" | Version A | "Hardware Security Modules (HSMs) implemented in cryptographic modules validated under FIPS 140-3 [25]" |
| Unreferenced standards (RFC 8785, FIPS 140-3, OIDC, BIP 341, ERC-2098, EIP-198) | Both | Added formal bibliographic entries [24]–[29] with complete metadata |
