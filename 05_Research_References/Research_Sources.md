# Authoritative Technical References and Primary Research Sources

This document catalogs the primary technical standards, specifications, and foundational research sources utilized in the academic report **"Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication"**. The numbering corresponds directly to Section 7 (References) in the primary Word deliverable (`RSA_Real_World_Applications_Report.docx`).

---

### [1] A Method for Obtaining Digital Signatures and Public-Key Cryptosystems
- **Document Title:** A Method for Obtaining Digital Signatures and Public-Key Cryptosystems
- **Authors:** Ronald L. Rivest, Adi Shamir, and Leonard Adleman
- **Publication Venue:** *Communications of the ACM* (CACM), vol. 21, no. 2, pp. 120–126, Feb. 1978. (Originally released as MIT Laboratory for Computer Science Technical Memorandum MIT/LCS/TM-82, April 1977).
- **DOI / URL:** https://doi.org/10.1145/359340.359342
- **Usage in Report:** Cited in Section 1 and Section 2.1 as the original academic formulation of public-key cryptography and digital signatures based on the integer factorization problem ($n = p \cdot q$).

---

### [2] PKCS #1: RSA Cryptography Specifications Version 2.2
- **Document Title:** PKCS #1: RSA Cryptography Specifications Version 2.2
- **Authors:** Kathleen Moriarty, Burt Kaliski, Jakob Jonsson, and Andreas Rusch
- **Publishing Organization:** Internet Engineering Task Force (IETF)
- **Series & Number:** Request for Comments (RFC) 8017 (Informational)
- **Publication Date:** November 2016
- **Official URL:** https://www.rfc-editor.org/rfc/rfc8017
- **Usage in Report:** Definitive technical specification for RSA key representations, cryptographic primitives (`RSASP1`, `RSAVP1`, `OS2IP`, `I2OSP`), RSA-OAEP encryption key transport constraints ($mLen \le k - 2hLen - 2$; 190 bytes for RSA-2048 with SHA-256), and RSA-PSS digital signature encoding (`EMSA-PSS-ENCODE`, `EMSA-PSS-VERIFY`). Documents that RSA-OAEP achieves IND-CCA2 security in the Random Oracle Model (Bellare-Rogaway 1994, Shoup 2001, Fujisaki et al. 2001) under RSA partial-domain one-wayness (though the concrete reduction is non-tight), whereas RSA-PSS achieves a tight EUF-CMA reduction in the ROM. Crucially, establishes the complete signing and verification sequences, emphasizing that modular exponentiation (`RSAVP1`, computing $s^e \bmod n$) alone does not establish signature validity without full `EMSA-PSS-VERIFY` salt unmasking and padding verification.

---

### [3] The Transport Layer Security (TLS) Protocol Version 1.3
- **Document Title:** The Transport Layer Security (TLS) Protocol Version 1.3
- **Author:** Eric Rescorla
- **Publishing Organization:** Internet Engineering Task Force (IETF)
- **Series & Number:** Request for Comments (RFC) 9846 (Standards Track; supersedes RFC 8446)
- **Publication Date:** July 2026
- **Official URL:** https://www.rfc-editor.org/rfc/rfc9846
- **Complementary Standards:** RFC 9963 ("Legacy RSASSA-PKCS1-v1_5 Code Points for TLS 1.3", April 2026) and RFC 10024 ("Post-Quantum Traditional (PQ/T) Hybrid Key Agreement Mechanisms for TLS 1.3", August 2026)
- **Usage in Report:** Referenced in Sections 1, 2.3, 4.3, and 6 to establish that TLS 1.3 removed static RSA key exchange. Clarifies that Forward Secrecy is provided by ephemeral key exchange ((EC)DHE) and PSK-DHE (`psk_dhe_ke`), whereas PSK-only mode (`psk_ke`) lacks forward secrecy against compromised pre-shared keys, and 0-RTT early data lacks forward secrecy and is vulnerable to replay attacks. Post-quantum hybrid protection depends on negotiating a supported hybrid mechanism (e.g., RFC 10024). Establishes that RSA's modern TLS 1.3 role is strictly endpoint authentication, where RSA-PSS is required for server `CertificateVerify` messages (RFC 9846), with RFC 9963 providing a restricted legacy exception for client certificate authentication.

---

### [4] Digital Signature Standard (DSS)
- **Document Title:** Digital Signature Standard (DSS)
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** Federal Information Processing Standards Publication (FIPS) 186-5
- **Publication Date:** February 2023
- **DOI / URL:** https://doi.org/10.6028/NIST.FIPS.186-5
- **Usage in Report:** Cited in Section 2.2 to document federal approval of the RSA-PSS signature scheme and its normative requirements regarding hash functions and salt generation parameters. Crucially cited for Section 5.1 ("Key Pair Usage"), which strictly mandates cryptographic key separation: an RSA key pair designated for digital signatures shall not be used for key establishment or encryption (such as RSA-OAEP).

---

### [5] Recommendation for Pair-Wise Key-Establishment Schemes Using Integer Factorization Cryptography
- **Document Title:** Recommendation for Pair-Wise Key-Establishment Schemes Using Integer Factorization Cryptography
- **Authors:** Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev, and Richard Davis
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** NIST Special Publication (SP) 800-56B Revision 2
- **Publication Date:** March 2019
- **DOI / URL:** https://doi.org/10.6028/NIST.SP.800-56Br2
- **Usage in Report:** Cited specifically for Table 2 ("Security strengths of key-establishment schemes") and Appendix D, establishing the authoritative asymptotic security strengths for RSA moduli: RSA-2048 (112 bits), RSA-3072 (128 bits), and RSA-4096 (152 bits) derived from the General Number Field Sieve (GNFS).

---

### [6] Recommendation for Key Management: Part 1 – General
- **Document Title:** Recommendation for Key Management: Part 1 – General
- **Author:** Elaine Barker
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** NIST Special Publication (SP) 800-57 Part 1 Revision 5
- **Publication Date:** May 2020
- **DOI / URL:** https://doi.org/10.6028/NIST.SP.800-57pt1r5
- **Usage in Report:** Cited in Section 3 and Table 1 for cryptographic algorithm equivalence, lifespan recommendations, and generic security strength classifications for 256-bit elliptic curves (~128-bit security category).

---

### [7] On the Importance of Eliminating Errors in Cryptographic Computations
- **Document Title:** On the Importance of Eliminating Errors in Cryptographic Computations
- **Authors:** Dan Boneh, Richard A. DeMillo, and Richard J. Lipton
- **Publication Venue:** *Journal of Cryptology*, vol. 14, no. 2, pp. 101–119, 2001 (preliminary version in *Eurocrypt 1997*).
- **DOI / URL:** https://doi.org/10.1007/s001450010016
- **Usage in Report:** Cited in Section 3.2 to formulate the Bellcore hardware fault-injection attack on Chinese Remainder Theorem (CRT) RSA implementations. Details both the two-signature formulation ($\gcd(s - s', n) \in \{p, q\}$) when a valid signature $s$ is available, and the single-fault formulation ($\gcd((s')^e - m, n) \in \{p, q\}$) when message representative $m = \text{OS2IP}(EM)$ is known. Clarifies that the PSS salt is unmasked during verification (not a secret), but because $m$ is randomized, $m$ cannot be precomputed from $M$ alone without the salt; once a valid signature $s$ is observed, $m = s^e \bmod n$ is recovered. Highlights that base blinding ($x' = x \cdot r^e \bmod n$) mitigates timing side channels, NOT CRT fault attacks, which require post-computation signature verification or fault-detection circuitry.

---

### [8] Schnorr Signatures for secp256k1
- **Document Title:** Schnorr Signatures for secp256k1
- **Authors:** Pieter Wuille, Jonas Nick, and Tim Ruffing
- **Publishing Organization:** Bitcoin Improvement Proposals (BIP)
- **Series & Number:** BIP 340
- **Publication Date:** January 2020
- **Official URL:** https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
- **Usage in Report:** Cited in Sections 1, 3.1, and Table 1 to detail Bitcoin Taproot's 64-byte Schnorr signature standard over secp256k1, highlighting its mathematical linearity, batch verification efficiency, and why it is superior to RSA for consensus-layer transaction verification.

---

### [9] Segregated Witness (Consensus Layer)
- **Document Title:** Segregated Witness (Consensus layer)
- **Authors:** Eric Lombrozo, Johnson Lau, and Pieter Wuille
- **Publishing Organization:** Bitcoin Improvement Proposals (BIP)
- **Series & Number:** BIP 141
- **Publication Date:** December 2015
- **Official URL:** https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
- **Usage in Report:** Cited in Section 3.1 to rigorously explain transaction weight ($\text{Weight} = (\text{Base} \times 3) + \text{Total}$) and virtual size ($\text{vSize} = \lceil \text{Weight} / 4 \rceil$). A typical P2WPKH witness stack totals approximately $107\text{–}109\text{ bytes}$ (1-byte count, 1-byte signature length, $\sim 70\text{–}72\text{ byte}$ DER signature plus sighash, 1-byte pubkey length, and 33-byte compressed pubkey). For a hypothetical RSA-2048 witness carrying two separate stack items (256-byte modulus and 256-byte signature, each with a 3-byte CompactSize prefix), the witness size equals $1 + 3 + 256 + 3 + 256 = 519\text{ bytes}$, adding approximately $410\text{–}412\text{ witness bytes}$ per input ($\approx 103\text{ additional virtual bytes}$). For a representative 141-vB baseline transaction, this hypothetical expansion is approximately $73\%$. The report explicitly notes that this is a hypothetical format, native Bitcoin RSA verification is not supported, the model assumes both values are carried in each input, and alternative key-storage designs would substantially alter the overhead.

---

### [10] MuSig2 for BIP340-compatible Multi-Signatures
- **Document Title:** MuSig2 for BIP340-compatible Multi-Signatures
- **Authors:** Jonas Nick, Tim Ruffing, and Elliott Jin
- **Publishing Organization:** Bitcoin Improvement Proposals (BIP)
- **Series & Number:** BIP 327
- **Publication Date:** 2023
- **Official URL:** https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki
- **Usage in Report:** Cited in Section 3.1 to distinguish multi-signature aggregation from base BIP 340 Schnorr signatures, illustrating how two-round $n$-of-$n$ threshold signing compacts into a single 64-byte on-chain signature—a capability unattainable with standard RSA.

---

### [11] Edwards-Curve Digital Signature Algorithm (EdDSA)
- **Document Title:** Edwards-Curve Digital Signature Algorithm (EdDSA)
- **Authors:** Simon Josefsson and Ilari Liusvaara
- **Publishing Organization:** Internet Engineering Task Force (IETF)
- **Series & Number:** Request for Comments (RFC) 8032 (Standards Track)
- **Publication Date:** January 2017
- **Official URL:** https://www.rfc-editor.org/rfc/rfc8032
- **Usage in Report:** Cited in Table 1 as an authoritative point of comparison for modern high-performance 128-bit elliptic-curve signatures (Ed25519; 32-byte public key, 64-byte signature; marked as not empirically benchmarked in this study).

---

### [12] Bitcoin Developer Guide: Transactions
- **Document Title:** Bitcoin Developer Guide: Transactions
- **Authors / Organization:** Bitcoin Core Developers
- **Publication Year:** n.d. [Online; accessed 2026]
- **Official URL:** https://developer.bitcoin.org/devguide/transactions.html
- **Usage in Report:** Cited in Section 3.1 regarding standard P2WPKH transaction serialization, typical witness stack composition (~107–109 bytes: 1-byte count, 1-byte signature length, ~70–72 byte DER signature + sighash, 1-byte pubkey length, 33-byte compressed pubkey), and consensus overhead.

---

### [13] Ethereum Developer Documentation: Transactions and Cryptographic Signatures
- **Document Title:** Ethereum Developer Documentation: Transactions and Cryptographic Signatures
- **Authors / Organization:** Ethereum Foundation
- **Publication Year:** n.d. [Online; accessed 2026]
- **Official URL:** https://ethereum.org/en/developers/docs/transactions/
- **Usage in Report:** Cited in Sections 1 and 3.1 to document Ethereum's use of ECDSA over secp256k1 for transaction signing, state transition verification, RLP signature serialization ($v, r, s$), ERC-2098 compact 64-byte signatures, EVM precompile 0x05 modular exponentiation (EIP-198), and gas cost economics.

---

### [14] Project Wycheproof: Cryptographic Test Vectors for Asymmetric Algorithms (Bundled Snapshot)
- **Document Title:** Project Wycheproof: Cryptographic Test Vectors for Asymmetric Algorithms
- **Authors:** Google Security Research (Daniel Bleichenbacher, Thomas Holenstein, Quan Nguyen)
- **Publishing Organization:** Google Security Research
- **Repository Snapshot:** Version 0.9 snapshot (`rsa_pss_2048_sha256_mgf1_32_test.json`, 108 test cases)
- **Upstream Project Notice:** The active upstream repository maintained by C2SP contains an expanded number of test vectors; the bundled version 0.9 snapshot is preserved intact in this repository (`05_Research_References/Wycheproof_Test_Vector/`) for experimental determinism and reproducibility.
- **Official URL:** https://github.com/google/wycheproof
- **Usage in Report:** Cited in Section 5.2 and executed in `rsa_pss_experiment.py`, validating all 108 test vectors (63 expected-valid accepted, 45 expected-invalid rejected) with 100% agreement.
