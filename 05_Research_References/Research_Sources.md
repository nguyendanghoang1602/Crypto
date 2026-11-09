# Authoritative Technical References and Primary Research Sources

This document catalogs the 22 primary technical standards, specifications, and foundational research sources utilized in the academic report **"Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication"** (comprising the 17 core references embedded in the primary Word deliverable `RSA_Real_World_Applications_Report.docx` and 5 supplementary normative standards [18]–[22] establishing full formal provenance).

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
- **Usage in Report:** Definitive technical specification for RSA key representations, cryptographic primitives (`RSASP1`, `RSAVP1`, `OS2IP`, `I2OSP`), RSA-OAEP encryption key transport constraints ($mLen \le k - 2hLen - 2$; 190 bytes for RSA-2048 with SHA-256), and RSA-PSS digital signature encoding (`EMSA-PSS-ENCODE`, `EMSA-PSS-VERIFY`). As an IETF Informational document, RFC 8017 specifies the concrete engineering implementation of these schemes; the underlying theoretical security proofs are established in the academic research literature (with RSA-OAEP proven IND-CCA2 in the Random Oracle Model under the standard RSA one-wayness assumption by Fujisaki et al. [16] following Shoup's analysis [15] of Bellare-Rogaway [17], while RSA-PSS achieves a tight EUF-CMA reduction in the ROM [3], [4]). Crucially, establishes the complete signing and verification sequences, emphasizing that modular exponentiation (`RSAVP1`, computing $s^e \bmod n$) alone does not establish signature validity without full `EMSA-PSS-VERIFY` salt unmasking and padding verification.

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
- **Usage in Report:** Cited in Section 3.2 to formulate the Bellcore hardware fault-injection attack on Chinese Remainder Theorem (CRT) RSA implementations. Explicitly delineates: (1) The two-signature formulation ($\gcd(s - s', n) \in \{p, q\}$) which strictly requires that both correct signature $s$ and faulty signature $s'$ were generated from the exact same encoded message representative $m = \text{OS2IP}(EM)$ (identical salt and padding); independent RSA-PSS executions on message $M$ yield differing salts ($EM_1 \ne EM_2 \implies m_1 \ne m_2$) and do NOT satisfy this condition; (2) The single-fault formulation ($\gcd((s')^e - m, n) \in \{p, q\}$) which assumes knowledge of the exact encoded representative $m$ of that specific faulty execution (which cannot be obtained merely from $M$ or a separate signature with a differing salt). Crucially differentiates countermeasures: base blinding ($x' = x \cdot r^e \bmod n$) mitigates timing side-channel attacks, NOT CRT fault injection, which requires post-computation signature verification or redundant fault-detection hardware.

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


---

### [15] OAEP Reconsidered
- **Document Title:** OAEP Reconsidered
- **Author:** Victor Shoup
- **Publication Venue:** *Journal of Cryptology*, vol. 15, no. 4, pp. 223–249, September 2002. (Extended abstract in *Advances in Cryptology – CRYPTO 2001*, Lecture Notes in Computer Science (LNCS), vol. 2139, pp. 239–259, Springer, 2001).
- **DOI / URL:** https://doi.org/10.1007/s00145-002-0133-9
- **Usage in Report:** Cited in Section 2.2 to document the foundational theoretical audit of OAEP. Shoup demonstrated that the claimed general IND-CCA2 security proof could not be established for arbitrary trapdoor permutations via standard black-box reductions under standard one-wayness (exposing a gap in the original general reduction), and proposed the provably secure variant OAEP+ to achieve IND-CCA2 security for arbitrary permutations.

---

### [16] RSA-OAEP is Secure under the RSA Assumption
- **Document Title:** RSA-OAEP is Secure under the RSA Assumption
- **Authors:** Eiichiro Fujisaki, Tatsuaki Okamoto, David Pointcheval, and Jacques Stern
- **Publication Venue:** *Journal of Cryptology*, vol. 17, no. 2, pp. 81–104, March 2004. (Extended abstract in *Advances in Cryptology – CRYPTO 2001*, Lecture Notes in Computer Science (LNCS), vol. 2139, pp. 260–274, Springer, 2001).
- **DOI / URL:** https://doi.org/10.1007/s00145-002-0204-y
- **Usage in Report:** Cited in Section 2.2 as the definitive proof establishing that RSA-OAEP achieves IND-CCA2 security in the Random Oracle Model under the standard RSA one-wayness assumption. Fujisaki, Okamoto, Pointcheval, and Stern introduced the concept of partial-domain one-wayness, proved that OAEP is IND-CCA2 secure if the underlying permutation is partial-domain one-way, and demonstrated that for the specific algebraic structure of the RSA permutation, partial-domain one-wayness is mathematically equivalent to full-domain one-wayness. This resolved the security gap for RSA-OAEP implementations (such as PKCS #1 / RFC 8017), while noting that the concrete security reduction is non-tight for practical RSA parameter lengths.

---

### [17] Optimal Asymmetric Encryption — How to Encrypt with RSA
- **Document Title:** Optimal Asymmetric Encryption — How to Encrypt with RSA
- **Authors:** Mihir Bellare and Phillip Rogaway
- **Publication Venue:** *Advances in Cryptology – EUROCRYPT '94*, Lecture Notes in Computer Science (LNCS), vol. 950, pp. 92–111, Springer-Verlag, 1995.
- **DOI / URL:** https://doi.org/10.1007/BFb0053428
- **Usage in Report:** Cited in Section 2.2 as the original academic formulation of Optimal Asymmetric Encryption Padding (OAEP). Bellare and Rogaway introduced OAEP and established semantic security against chosen-plaintext attacks (IND-CPA) and plaintext awareness (implying chosen-ciphertext security IND-CCA1 for general trapdoor permutations in the Random Oracle Model), without establishing general IND-CCA2 security under standard one-wayness.

---

### [18] The Exact Security of Digital Signatures: How to Sign with RSA and Rabin
- **Document Title:** The Exact Security of Digital Signatures: How to Sign with RSA and Rabin
- **Authors:** Mihir Bellare and Phillip Rogaway
- **Publication Venue:** *Advances in Cryptology – EUROCRYPT '96*, Lecture Notes in Computer Science (LNCS), vol. 1070, pp. 399–416, Springer, 1996.
- **DOI / URL:** https://doi.org/10.1007/3-540-68339-9_34
- **Usage in Report:** Cited in Section 2.2 to provide the rigorous academic foundation for the Probabilistic Signature Scheme (PSS). Bellare and Rogaway introduced PSS and proved that it achieves tight existential unforgeability under adaptive chosen-message attack (EUF-CMA) in the Random Oracle Model (ROM), demonstrating that forging an RSA-PSS signature is as hard as inverting the RSA permutation itself, overcoming the loose reductions of legacy padding schemes.

---

### [19] Secure Hash Standard (SHS)
- **Document Title:** Secure Hash Standard (SHS)
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** Federal Information Processing Standards Publication (FIPS) 180-4
- **Publication Date:** August 2015
- **DOI / URL:** https://doi.org/10.6028/NIST.FIPS.180-4
- **Usage in Report:** Cited in Section 2.2, Section 4.2, and Section 5.1 as the authoritative normative specification for the SHA-256 cryptographic hash function utilized to compute the payload digest `mHash` and the hash evaluations within Mask Generation Function 1 (`MGF1-SHA256`).

---

### [20] SEC 2: Recommended Elliptic Curve Domain Parameters
- **Document Title:** SEC 2: Recommended Elliptic Curve Domain Parameters
- **Publishing Organization:** Standards for Efficient Cryptography Group (SECG) / Certicom Corp.
- **Series & Number:** Standards for Efficient Cryptography (SEC) Version 2.0
- **Publication Date:** January 2010
- **Official URL:** https://www.secg.org/sec2-v2.pdf
- **Usage in Report:** Cited in Section 3.1 and Section 5.1 to define the standard mathematical parameters of the Koblitz elliptic curve `secp256k1` ($y^2 = x^3 + 7 \bmod p$), its field modulus $p$, order $n$, base point $G$, and ECDSA signing equation $s = k^{-1}(z + r \cdot d_A) \bmod n$, providing the exact baseline for comparing RSA-3072 and ECDSA at the 128-bit security tier.

---

### [21] EIP-712: Typed Structured Data Hashing and Signing
- **Document Title:** EIP-712: Typed Structured Data Hashing and Signing
- **Authors:** Remco Bloemen, Leonid Logvinov, and Jacob Evans
- **Publishing Organization:** Ethereum Improvement Proposals (EIP)
- **Publication Date:** September 2017
- **Official URL:** https://eips.ethereum.org/EIPS/eip-712
- **Usage in Report:** Cited in Section 4.1 to contextualize off-chain cryptographic request authorization. Establishes the standard industry design pattern for deterministic structured payload encoding prior to signing, supporting the architectural rationale behind our off-chain RSA-PSS withdrawal authorization prototype before on-chain settlement.

---

### [22] Digital Identity Guidelines: Authentication and Lifecycle Management
- **Document Title:** Digital Identity Guidelines: Authentication and Lifecycle Management
- **Authors:** Paul A. Grassi, Michael E. Garcia, and James L. Fenton
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** NIST Special Publication (SP) 800-63B
- **Publication Date:** June 2017 (Updated March 2020)
- **DOI / URL:** https://doi.org/10.6028/NIST.SP.800-63B
- **Usage in Report:** Cited in Section 4.2 and Section 4.3 to establish formal technical requirements for replay resistance, timestamp freshness windows ($\pm 300\text{s}$ tolerance for clock skew), and cryptographically random nonce generation in secure transaction authorization workflows.

