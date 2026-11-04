# TECHNICAL ISSUE REGISTER — RSA RESEARCH REPORT AUDIT

**Project Title:** *Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication*  
**Date of Register:** November 5, 2026  
**Auditing Panel:** Senior Cryptography Researcher, Blockchain Security Engineer, and Academic Reviewer  

---

## 1. COMPREHENSIVE TECHNICAL ISSUE REGISTER

### ISSUE-01 (Severity: CRITICAL)
- **Original Problem:** The tight EUF-CMA security reduction of RSA-PSS to the RSA inversion problem in the Random Oracle Model (ROM) was attributed to RFC 8017 [2].
- **Location:** Abstract, Section 2.2, Section 7.
- **Technical Explanation:** RFC 8017 is an IETF Informational memo that specifies engineering encoding and verification procedures. The foundational academic security proof was established by Mihir Bellare and Phillip Rogaway in their EUROCRYPT '96 paper (*"The Exact Security of Digital Signatures—How to Sign with RSA and Rabin"*). Citing RFC 8017 or TLS standards as the source of the security proof is an academic attribution error.
- **Correction Made:** Added reference [23] (Bellare and Rogaway, EUROCRYPT '96, LNCS 1070). Clarified that RFC 8017 [2] and NIST FIPS 186-5 [4] specify the standardized engineering scheme, while Bellare and Rogaway [23] provide the foundational theoretical security analysis proving an essentially tight reduction in ROM.
- **Verification Evidence:** Verified in `02_Source_Code/build_report_doc.py`, `Research_Sources.md`, and `REFERENCE_AUDIT.md`.

---

### ISSUE-02 (Severity: HIGH)
- **Original Problem:** Text suggested that applying SHA-256 hashing alone thwarts textbook RSA multiplicative homomorphic forgery.
- **Location:** Section 2.2.
- **Technical Explanation:** In textbook RSA, signature verification evaluates $s^e \equiv m \pmod n$. Because $(m_1)^e \cdot (m_2)^e \equiv (m_1 \cdot m_2)^e \pmod n$, multiplying two valid signatures produces a valid signature on the product of the messages. Merely hashing the message ($h = H(m)$) maps long messages to a fixed size, but if the raw hash were signed as $s = h^d \bmod n$, algebraic relations between digests could still be exploited. The EUF-CMA security of RSA-PSS relies on the structured probabilistic encoding of EMSA-PSS (MGF1 masking, randomized salt, and padding trailer), not simply on the hash function.
- **Correction Made:** Explicitly clarified: *"SHA-256 maps arbitrary-length messages to a fixed-length 256-bit digest, allowing RSA-PSS to operate on a fixed-length digest-derived encoding that fits the RSA modulus rather than applying RSA directly to the full message. However, SHA-256 itself does not eliminate textbook RSA's multiplicative homomorphism. While RFC 8017 [2] and NIST FIPS 186-5 [4] specify the standardized engineering scheme, Bellare and Rogaway [23] established its foundational theoretical security analysis, proving that RSA-PSS achieves an essentially tight EUF-CMA security reduction to the RSA inversion problem in the Random Oracle Model (ROM)."*
- **Verification Evidence:** Confirmed in `01_Final_Report/RSA_Real_World_Applications_Report_FINAL.docx`.

---

### ISSUE-03 (Severity: HIGH)
- **Original Problem:** Narrative used the phrase "preventing modular overflow" to describe the role of SHA-256.
- **Location:** Section 2.2.
- **Technical Explanation:** "Modular overflow" is technically imprecise in modular arithmetic, where reduction modulo $n$ always wraps into $\mathbb{Z}_n$. The genuine function of the hash and encoding pipeline is ensuring that the message representative $m = \text{OS2IP}(EM)$ satisfies $m < n$ (specifically $emBits = modBits - 1$) and maps arbitrary-length payloads into a standardized domain.
- **Correction Made:** Replaced "preventing modular overflow" with: *"allowing RSA-PSS to operate on a fixed-length digest-derived encoding that fits the RSA modulus rather than applying RSA directly to the full message."*
- **Verification Evidence:** Confirmed in `build_report_doc.py` and final Word document.

---

### ISSUE-04 (Severity: MEDIUM)
- **Original Problem:** Used "256-bit AES-GCM" and described RSA-OAEP as "encapsulating an ephemeral key", conflating key transport with KEM mechanisms.
- **Location:** Section 2.2, Section 2.3.
- **Technical Explanation:** AES-GCM is an authenticated cipher mode specified in NIST SP 800-38D [22], not a key type. Furthermore, RSA-OAEP is an asymmetric key transport (wrapping) mechanism where the sender generates a symmetric key and encrypts it under the recipient's public key; this differs from Key Encapsulation Mechanisms (KEMs, e.g., ML-KEM in RFC 10024 [19]) which internally generate shared secrets.
- **Correction Made:** Corrected terminology to: *"encrypting (wrapping) an ephemeral 256-bit AES key using RSA-OAEP to protect bulk data authenticated with AES-GCM (NIST SP 800-38D [22]), maintaining the distinction between RSA key transport and KEM encapsulation (such as ML-KEM in RFC 10024 [19])."*
- **Verification Evidence:** Confirmed in Section 2.2 and Section 2.3 of the final report.

---

### ISSUE-05 (Severity: HIGH)
- **Original Problem:** Text claimed: *"RSA X.509 certificates authenticate servers via RSA-PSS CertificateVerify messages."*
- **Location:** Section 2.3.
- **Technical Explanation:** This statement conflated the Certificate Authority's signature on the X.509 certificate with the server's signature on the TLS handshake transcript. In TLS 1.3: (1) The X.509 certificate binds the server's identity to a public key via a CA's digital signature; (2) The server proves possession of the private key by signing the handshake transcript in the `CertificateVerify` message; (3) When RSA keys are used for server authentication, RFC 9846 [3] mandates RSA-PSS for `CertificateVerify`, while the CA's certificate signature is a separate operation and not required to be RSA-PSS.
- **Correction Made:** Explicitly deconstructed all three concepts in Section 2.3.
- **Verification Evidence:** Confirmed in Section 2.3 of the final report.

---

### ISSUE-06 (Severity: HIGH)
- **Original Problem:** Conflated exact ECDSA nonce reuse with slight nonce bias, claiming both allow immediate algebraic key recovery via a two-signature formula.
- **Location:** Section 3.2.
- **Technical Explanation:** Exact reuse of nonce $k$ across two distinct message hashes $z_1, z_2$ produces the same curve $x$-coordinate $r$. The private key $d_A$ can be extracted algebraically from two signatures: $s_1 - s_2 \equiv k^{-1}(z_1 - z_2) \pmod n \implies k \equiv (z_1 - z_2)(s_1 - s_2)^{-1} \pmod n$, revealing $d_A \equiv (s_1 k - z_1)r^{-1} \pmod n$. However, slight nonce bias or partial leakage does NOT permit this direct two-signature calculation; exploiting bias requires collecting many signatures and solving the Hidden Number Problem (HNP) via lattice reduction algorithms (e.g., LLL / BKZ).
- **Correction Made:** Clearly separated exact reuse from slight bias, providing the two-signature algebraic recovery derivation while noting the lattice HNP requirement for nonce bias.
- **Verification Evidence:** Confirmed in Section 3.2 of the final report.

---

### ISSUE-07 (Severity: MEDIUM)
- **Original Problem:** Table 1 listed the mathematical hard problem for RSA simply as "Factoring".
- **Location:** Table 1, Row 1.
- **Technical Explanation:** While integer factorization of $n = p \cdot q$ breaks RSA, computing the $e$-th root modulo $n$ (the RSA Inversion Problem) is not proven to be strictly equivalent to factoring $n$. Presenting the foundation simply as "Factoring" ignores the RSA Problem and complexity-theoretic nuances.
- **Correction Made:** Updated Table 1 Row 1 to: *"Integer Factorization (IFP) / RSA Inversion Problem"*.
- **Verification Evidence:** Confirmed in Table 1 of the final report.

---

### ISSUE-08 (Severity: MEDIUM)
- **Original Problem:** Section 3.1 stated that GNFS requires modulus size to scale "super-linearly" without framing the comparison against Pollard's rho group complexity.
- **Location:** Section 3.1.
- **Technical Explanation:** GNFS has sub-exponential complexity $L_n[1/3, c] = \exp((c + o(1))(\ln n)^{1/3}(\ln \ln n)^{2/3})$, whereas solving ECDLP in a cyclic group of prime order $q$ via Pollard's rho algorithm has expected fully exponential complexity $\mathcal{O}(\sqrt{q})$. Differentiating modulus $n$ from group order $q$ is essential.
- **Correction Made:** Reformulated the cryptanalytic complexity comparison: factoring an RSA modulus $n = p \cdot q$ via GNFS has sub-exponential complexity, whereas solving ECDLP in a cyclic group of prime order $q$ via Pollard's rho has expected fully exponential complexity $\mathcal{O}(\sqrt{q})$, explaining why RSA requires 3072 bits for 128-bit security vs 256 bits for secp256k1 per NIST SP 800-56B [5] and SP 800-57 [6].
- **Verification Evidence:** Confirmed in Section 3.1 of the final report.

---

### ISSUE-09 (Severity: MEDIUM)
- **Original Problem:** Primitive operation counts (17 modular multiplications for RSA vs. ~256 point doublings/additions for ECC) were directly compared as if they had equivalent execution costs.
- **Location:** Section 3.2.
- **Technical Explanation:** A modular multiplication in $\mathbb{Z}_n$ and an elliptic curve point addition on a Weierstrass curve represent fundamentally distinct mathematical operations with vastly different underlying field operations.
- **Correction Made:** Added explicit qualification: *"While modular multiplications and ECC group additions represent distinct operations whose counts cannot be directly equated, the small algebraic exponent enables exceptionally fast verification, confirmed by our empirical benchmarks."*
- **Verification Evidence:** Confirmed in Section 3.2 of the final report.

---

### ISSUE-10 (Severity: HIGH)
- **Original Problem:** Bellcore CRT fault attack formulation failed to distinguish single-fault vs. two-signature fault conditions under randomized RSA-PSS.
- **Location:** Section 3.2.
- **Technical Explanation:** Accelerating RSA signing via CRT ($s_p = m^{d_p} \bmod p$, $s_q = m^{d_q} \bmod q$) is vulnerable if a hardware fault corrupts one branch (e.g., $s'_q$). In the two-signature formulation $\gcd(s - s', n) = p$, both correct $s$ and faulty $s'$ must be computed over the exact same encoded representative $m = \text{OS2IP}(EM)$. Because RSA-PSS randomizes $EM$ with salt, independent signatures on the same message $M$ yield $EM_1 \ne EM_2$, preventing the two-signature attack. In the single-fault formulation $p = \gcd((s')^e - m, n)$, the attacker must know the exact representative $m$ of that specific execution.
- **Correction Made:** Explicitly formulated both attack scenarios and explained why base blinding ($x' = x \cdot r^e \bmod n$) mitigates timing side-channels, whereas CRT fault mitigation mandates post-computation verification ($s^e \bmod n == m$).
- **Verification Evidence:** Confirmed in Section 3.2 of the final report.

---

### ISSUE-11 (Severity: MEDIUM)
- **Original Problem:** Bitcoin SegWit witness size calculation for hypothetical RSA-2048 ($1 + 3 + 256 + 3 + 256 = 519\text{ bytes}$) was presented without explicitly stating its underlying assumptions.
- **Location:** Section 3.1.
- **Technical Explanation:** A complete DER-encoded RSA public key spans $\approx 294\text{ bytes}$. The 256-byte payload model assumes an implicit or fixed public exponent $e = 65,537$. Furthermore, native Bitcoin consensus does not support RSA verification.
- **Correction Made:** Explicitly formulated: *"under the simplified assumption of a 256-byte modulus payload (treating public exponent $e = 65,537$ as implicit, rather than complete ~294-byte DER pubkeys) and a 256-byte RSA signature with 3-byte CompactSize prefixes... Native Bitcoin consensus does not support RSA verification; this hypothetical model illustrates why consensus layers mandate compact elliptic curve primitives."*
- **Verification Evidence:** Confirmed in Section 3.1 of the final report.

---

### ISSUE-12 (Severity: MEDIUM)
- **Original Problem:** Claim that multi-signature aggregation is "unattainable with RSA" was stated without qualification.
- **Location:** Section 3.1, Table 1.
- **Technical Explanation:** While specialized multisignature RSA schemes exist in the academic literature, standard RSASSA-PSS cannot natively aggregate multiple threshold signatures into a single compact 256/384-byte on-chain signature in the manner of Schnorr / MuSig2 (BIP 327 [10]).
- **Correction Made:** Scoped the claim specifically to native compact on-chain signature aggregation of the evaluated schemes.
- **Verification Evidence:** Confirmed in Section 3.1 and Table 1 of the final report.

---

### ISSUE-13 (Severity: MEDIUM)
- **Original Problem:** Algorithm 1 lacked clear annotations of architectural trust boundaries, private-key isolation, and edge verification steps.
- **Location:** Section 4.2 (Algorithm 1).
- **Technical Explanation:** In enterprise cryptocurrency architectures, key custody is isolated within secure signer enclaves or HSMs, while verification occurs at edge gateways.
- **Correction Made:** Annotated Algorithm 1 with explicit structural boundaries: (1) Internal Secure Signer Service Boundary; (2) Network Transit Boundary; and (3) Edge Verification Gateway Boundary.
- **Verification Evidence:** Confirmed in Algorithm 1 of the final report.

---

### ISSUE-14 (Severity: LOW)
- **Original Problem:** Scenario 1 described withdrawal amount as "12.5 ETH atomic units".
- **Location:** Section 5.1.
- **Technical Explanation:** ETH is the high-level unit; the atomic integer monetary unit of Ethereum is wei ($1\text{ ETH} = 10^{18}\text{ wei}$).
- **Correction Made:** Specified: *"Valid request of 12.5 ETH, represented as an integer amount in wei ($12,500,000,000,000,000,000$ wei) -> ACCEPTED"*.
- **Verification Evidence:** Confirmed in Section 5.1 of the final report.

---

### ISSUE-15 (Severity: MEDIUM)
- **Original Problem:** Abstract and Section 5.2 used language implying that passing the bundled 108 Wycheproof test vectors constitutes an authoritative certification.
- **Location:** Abstract, Section 5.2.
- **Technical Explanation:** Wycheproof test vectors provide empirical validation against selected known edge cases; passing them does not constitute formal FIPS or RFC compliance certification.
- **Correction Made:** Reframed with restrained language: demonstrates agreement with the selected 108 test vectors without claiming full protocol certification or complete absence of vulnerabilities.
- **Verification Evidence:** Confirmed in Abstract and Section 5.2 of the final report.

---

### ISSUE-16 (Severity: MEDIUM)
- **Original Problem:** FIPS 186-5 key separation was justified with an overbroad assertion that decryption queries automatically reveal signature information.
- **Location:** Section 2.2.
- **Technical Explanation:** Cross-protocol attacks depend on specific mathematical and padding vulnerabilities. FIPS 186-5 Section 5.1 normatively mandates key separation to prevent unintended protocol interactions, enforce purpose separation, and limit compromise impact.
- **Correction Made:** Grounded key separation in preventing cross-protocol interactions between disparate padding schemes, enforcing cryptographic purpose separation, and limiting compromise blast radius.
- **Verification Evidence:** Confirmed in Section 2.2 of the final report.

---

### ISSUE-17 (Severity: LOW)
- **Original Problem:** Section 4.3 presented FIPS 140-3 as an example of an HSM product ("HSMs, e.g., FIPS 140-3").
- **Location:** Section 4.3.
- **Technical Explanation:** FIPS 140-3 is a federal standard establishing security requirements for cryptographic modules, not a hardware product category.
- **Correction Made:** Corrected to: *"Hardware Security Modules (HSMs) implemented in cryptographic modules validated under FIPS 140-3 [25], where applicable"*.
- **Verification Evidence:** Confirmed in Section 4.3 of the final report.

---

### ISSUE-18 (Severity: LOW)
- **Original Problem:** Section 4.3 asserted that "production systems require..." distributed Redis/SQL mechanisms.
- **Location:** Section 4.3.
- **Technical Explanation:** System architecture requirements depend on operational scale and multi-instance concurrency models.
- **Correction Made:** Calibrated phrasing: *"production deployments with multiple gateway instances typically need durable, shared, atomic nonce check-and-insert mechanisms (e.g., Redis SETNX or SQL unique constraint transactions) with TTL expiration"*.
- **Verification Evidence:** Confirmed in Section 4.3 of the final report.

---

### ISSUE-19 (Severity: MEDIUM)
- **Original Problem:** Standards mentioned in the text (RFC 8785, FIPS 140-3, OpenID Connect, BIP 341, ERC-2098, EIP-198) lacked formal numbered bibliographic entries.
- **Location:** Section 3, Section 3.1, Section 4.2, Section 4.3, Section 7.
- **Technical Explanation:** Academic rigor requires every standard or specification mentioned in the text to carry a formal bibliographic citation.
- **Correction Made:** Expanded bibliography to 29 references, adding formal entries [24]–[29] with complete author rosters, DOIs, and URLs.
- **Verification Evidence:** Confirmed in `REFERENCE_AUDIT.md`, `Research_Sources.md`, and final Word document.

---

### ISSUE-20 (Severity: HIGH)
- **Original Problem:** Prior draft reviews erroneously misattributed course topics across Sessions 1 to 7.
- **Location:** Script header, document comments, methodology narrative.
- **Technical Explanation:** The authentic USTH Introduction to Cryptography syllabus covers: Session 1 (Modular Arithmetic), Session 2 (Cryptanalysis & Symmetric Cryptography), Session 3 (Stream Ciphers), Session 4 (Block Ciphers & Modes), Session 5 (Public-Key Cryptography & Trapdoors), Session 6 (RSA & Diffie-Hellman), and Session 7 (Digital Signatures & Hash Functions).
- **Correction Made:** Mapped every foundational topic directly to its authentic session number, integrating concepts naturally without artificial insertions or false claims.
- **Verification Evidence:** Confirmed in `build_report_doc.py` docstring and Section 1–2 narratives.
