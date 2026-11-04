# REFERENCE AND CITATION AUDIT — RSA RESEARCH DELIVERABLES

**Project Title:** *Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication*  
**Audit Date:** November 5, 2026  
**Auditing Panel:** Senior Cryptography Researcher & Technical Editor  
**Total References Audited:** 29 Primary Technical Standards, Specifications, and Peer-Reviewed Papers  

---

## 1. AUDIT PROTOCOL & VERIFICATION PRINCIPLES

In strict accordance with academic integrity requirements:
1. **Primary Source Priority:** Priority is assigned to official IETF RFCs, NIST Federal Information Processing Standards (FIPS), NIST Special Publications (SP), Bitcoin Improvement Proposals (BIPs), Ethereum Improvement Proposals (EIPs/ERCs), and original peer-reviewed conference/journal proceedings.
2. **Metadata Authenticity:** Every publication venue, publication date, author roster, and identifier (DOI, RFC number, BIP/EIP number) has been cross-checked against authoritative repositories.
3. **Citation Synchronization:** Every numbered entry in Section 7 corresponds to an active in-text citation, and every standard or paper referenced in the narrative carries an explicit numerical citation tag.
4. **Zero Fabrication:** No synthetic, secondary, or unverified DOIs or RFC numbers are utilized.

---

## 2. COMPREHENSIVE 29-REFERENCE AUDIT CATALOG

| Ref | Document Title | Authors / Issuing Body | Venue / Series | Date | Official Identifier / URL | Primary Role & In-Text Context | Status |
|:---:|:---|:---|:---|:---:|:---|:---|:---:|
| **[1]** | A Method for Obtaining Digital Signatures and Public-Key Cryptosystems | R. L. Rivest, A. Shamir, and L. Adleman | *Communications of the ACM* (MIT/LCS/TM-82) | 1978 / 1977 | https://doi.org/10.1145/359340.359342 | Original academic formulation of public-key cryptography, integer factorization, and RSA digital signatures (Sections 1, 2.1). | **VERIFIED** |
| **[2]** | PKCS #1: RSA Cryptography Specifications Version 2.2 | K. Moriarty, B. Kaliski, J. Jonsson, A. Rusch | IETF RFC 8017 (Informational) | Nov. 2016 | https://www.rfc-editor.org/rfc/rfc8017 | Standardized engineering specifications for RSA-OAEP, RSA-PSS, EMSA-PSS, and primitives RSASP1/RSAVP1 (Sections 1, 2.1, 2.2). | **VERIFIED** |
| **[3]** | The Transport Layer Security (TLS) Protocol Version 1.3 | E. Rescorla | IETF RFC 9846 (Standards Track; supersedes RFC 8446) | July 2026 | https://www.rfc-editor.org/rfc/rfc9846 | Removal of static RSA key exchange; mandate of RSA-PSS for server CertificateVerify (Sections 1, 2.3). | **VERIFIED** |
| **[4]** | Digital Signature Standard (DSS) | National Institute of Standards and Technology | NIST FIPS 186-5 | Feb. 2023 | https://doi.org/10.6028/NIST.FIPS.186-5 | Federal standard approving RSA-PSS; Section 5.1 normative key separation rule (Section 2.2). | **VERIFIED** |
| **[5]** | Recommendation for Pair-Wise Key-Establishment Schemes Using Integer Factorization Cryptography | E. Barker, L. Chen, A. Roginsky, A. Vassilev, R. Davis, S. Simon | NIST SP 800-56B Rev. 2 | Mar. 2019 | https://doi.org/10.6028/NIST.SP.800-56Br2 | RSA key transport specification; security strength classifications: RSA-2048 (112b), RSA-3072 (128b), RSA-4096 (152b) (Sections 2.2, 2.3, 3, Tables 1 & 2). | **VERIFIED** |
| **[6]** | Recommendation for Key Management: Part 1 – General | E. Barker | NIST SP 800-57 Part 1 Rev. 5 | May 2020 | https://doi.org/10.6028/NIST.SP.800-57pt1r5 | Generic 256-bit elliptic-curve strength mapping (~128-bit security category) and key lifecycle (Section 3, Tables 1 & 2). | **VERIFIED** |
| **[7]** | On the Importance of Eliminating Errors in Cryptographic Computations | D. Boneh, R. A. DeMillo, and R. J. Lipton | *Journal of Cryptology*, vol. 14, no. 2, pp. 101–119 | 2001 | https://doi.org/10.1007/s001450010016 | Bellcore hardware fault-injection attack on CRT-based RSA; single-fault and two-signature equations (Section 3.2). | **VERIFIED** |
| **[8]** | Schnorr Signatures for secp256k1 | P. Wuille, J. Nick, and T. Ruffing | Bitcoin Improvement Proposal (BIP) 340 | Jan. 2020 | https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki | 64-byte Schnorr signature standard for Bitcoin Taproot; batch verification (Sections 1, 3, 3.1, Table 1). | **VERIFIED** |
| **[9]** | Segregated Witness (Consensus Layer) | E. Lombrozo, J. Lau, and P. Wuille | Bitcoin Improvement Proposal (BIP) 141 | Dec. 2015 | https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki | Transaction weight and virtual size formulation: $\text{Weight} = (\text{Base} \times 3) + \text{Total}$; witness discount (Section 3.1). | **VERIFIED** |
| **[10]** | MuSig2 for BIP340-compatible Multi-Signatures | J. Nick, T. Ruffing, and E. Jin | Bitcoin Improvement Proposal (BIP) 327 | 2023 | https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki | Two-round threshold Schnorr multi-signature aggregation into a single 64-byte on-chain signature (Section 3.1, Table 1). | **VERIFIED** |
| **[11]** | Edwards-Curve Digital Signature Algorithm (EdDSA) | S. Josefsson and I. Liusvaara | IETF RFC 8032 (Standards Track) | Jan. 2017 | https://www.rfc-editor.org/rfc/rfc8032 | 128-bit Ed25519 signature standard (32 B pubkey, 64 B signature) benchmark point of comparison (Section 3, Table 1). | **VERIFIED** |
| **[12]** | Bitcoin Developer Guide: Transactions | Bitcoin Core Developers | Bitcoin Project | n.d. [2026] | https://developer.bitcoin.org/devguide/transactions.html | P2WPKH transaction witness stack composition (~107–109 bytes) and serialization rules (Sections 1, 3, 3.1, Table 1). | **VERIFIED** |
| **[13]** | Ethereum Developer Documentation: Transactions and Signatures | Ethereum Foundation | Ethereum Foundation Docs | n.d. [2026] | https://ethereum.org/en/developers/docs/transactions/ | Ethereum ECDSA-secp256k1 transaction signatures ($v, r, s$), RLP encoding, and verification overhead (Sections 1, 3, 3.1, Table 1). | **VERIFIED** |
| **[14]** | Project Wycheproof: Cryptographic Test Vectors for Asymmetric Algorithms | Google Security Research (D. Bleichenbacher et al.) | GitHub repository (v0.9 snapshot) | n.d. [2026] | https://github.com/google/wycheproof | 108 test vectors for RSASSA-PSS-2048-SHA256 (63 valid accepted, 45 invalid rejected) (Section 5.2). | **VERIFIED** |
| **[15]** | OAEP Reconsidered | V. Shoup | *Journal of Cryptology*, vol. 15, no. 4, pp. 223–249 (CRYPTO 2001) | Sep. 2002 | https://doi.org/10.1007/s00145-002-0133-9 | Theoretical analysis exposing gap in general OAEP IND-CCA2 reduction; introduction of OAEP+ (Section 2.2). | **VERIFIED** |
| **[16]** | RSA-OAEP is Secure under the RSA Assumption | E. Fujisaki, T. Okamoto, D. Pointcheval, and J. Stern | *Journal of Cryptology*, vol. 17, no. 2, pp. 81–104 (CRYPTO 2001) | Mar. 2004 | https://doi.org/10.1007/s00145-002-0204-y | Definitive proof that RSA-OAEP achieves IND-CCA2 security in ROM under standard RSA one-wayness (Section 2.2). | **VERIFIED** |
| **[17]** | Optimal Asymmetric Encryption — How to Encrypt with RSA | M. Bellare and P. Rogaway | *Advances in Cryptology – EUROCRYPT '94*, LNCS 950, pp. 92–111 | 1995 | https://doi.org/10.1007/BFb0053428 | Original OAEP specification; IND-CPA and plaintext awareness (IND-CCA1) for general trapdoor permutations (Section 2.2). | **VERIFIED** |
| **[18]** | Legacy RSASSA-PKCS1-v1_5 Code Points for TLS 1.3 | D. Benjamin and A. Popov | IETF RFC 9963 (Standards Track) | April 2026 | https://doi.org/10.17487/RFC9963 | Restricted legacy exception permitting client certificate authentication with PKCS#1 v1.5 in constrained environments (Section 2.3). | **VERIFIED** |
| **[19]** | Post-Quantum Traditional (PQ/T) Hybrid Key Agreement for TLS 1.3 | K. Kwiatkowski, P. Kampanakis, B. Westerbaan, D. Stebila | IETF RFC 10024 (Standards Track) | August 2026 | https://doi.org/10.17487/RFC10024 | Hybrid post-quantum key agreement combining post-quantum KEMs (ML-KEM) with traditional ECDHE (Section 2.3). | **VERIFIED** |
| **[20]** | Module-Lattice-Based Digital Signature Standard | National Institute of Standards and Technology | NIST FIPS 204 | August 2024 | https://doi.org/10.6028/NIST.FIPS.204 | Post-quantum signature standard ML-DSA (CRYSTALS-Dilithium) for quantum-resistant migration (Section 6). | **VERIFIED** |
| **[21]** | Stateless Hash-Based Digital Signature Standard | National Institute of Standards and Technology | NIST FIPS 205 | August 2024 | https://doi.org/10.6028/NIST.FIPS.205 | Post-quantum signature standard SLH-DSA (SPHINCS+) providing minimal cryptographic assumptions (Section 6). | **VERIFIED** |
| **[22]** | Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) | M. Dworkin | NIST SP 800-38D | Nov. 2007 | https://doi.org/10.6028/NIST.SP.800-38D | Definitive specification for AES-GCM authenticated symmetric encryption in hybrid cryptosystems (Sections 2.2, 2.3). | **VERIFIED** |
| **[23]** | The Exact Security of Digital Signatures—How to Sign with RSA and Rabin | M. Bellare and P. Rogaway | *Advances in Cryptology – EUROCRYPT '96*, LNCS 1070, pp. 399–416 | 1996 | https://doi.org/10.1007/3-540-68339-9_34 | Original specification of RSA-PSS and foundational proof establishing tight EUF-CMA reduction in ROM (Section 2.2). | **VERIFIED** |
| **[24]** | JSON Canonicalization Scheme (JCS) | A. Rundgren, B. Jordan, and S. Erdtman | IETF RFC 8785 (Standards Track) | June 2020 | https://doi.org/10.17487/RFC8785 | Authoritative standard for canonical JSON serialization; baseline for evaluating custom deterministic encoding (Section 4.2). | **VERIFIED** |
| **[25]** | Security Requirements for Cryptographic Modules | National Institute of Standards and Technology | NIST FIPS 140-3 | March 2019 | https://doi.org/10.6028/NIST.FIPS.140-3 | Federal standard specifying security requirements for cryptographic modules hosting private signing keys (Section 4.3). | **VERIFIED** |
| **[26]** | OpenID Connect Core 1.0 incorporating errata set 1 | N. Sakimura, J. Bradley, M. Jones, B. de Medeiros, C. Mortimore | OpenID Foundation Standard | Nov. 2014 | https://openid.net/specs/openid-connect-core-1_0.html | Standard for customer identity authentication, distinguished from transaction payload authorization (Section 4.3). | **VERIFIED** |
| **[27]** | Taproot: SegWit version 1 spending rules | P. Wuille, J. Nick, and A. Towns | Bitcoin Improvement Proposal (BIP) 341 | Jan. 2020 | https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki | Taproot consensus specification integrating BIP 340 Schnorr signatures into Bitcoin (Section 3.1, Table 1). | **VERIFIED** |
| **[28]** | Compact Signature Representation | R. Moore | Ethereum Improvement Proposal (ERC) 2098 | March 2019 | https://eips.ethereum.org/EIPS/eip-2098 | 64-byte compact representation for Ethereum ECDSA signatures (Section 3.1, Table 1). | **VERIFIED** |
| **[29]** | Big Integer Modular Exponentiation Precompile | V. Buterin and M. H. Swende | Ethereum Improvement Proposal (EIP) 198 | March 2017 | https://eips.ethereum.org/EIPS/eip-198 | EVM precompile at address 0x05 for big integer modular exponentiation (Section 3.1). | **VERIFIED** |

---

## 3. CITATION VERIFICATION & DISCOVERY CHECKLIST

- [x] All 29 references exist as active, verified academic publications or official standards.
- [x] DOIs resolve to Springer, ACM, or NIST official digital libraries.
- [x] RFC URLs resolve to the official IETF RFC Editor.
- [x] BIP and EIP URLs resolve to official Bitcoin and Ethereum repository specifications.
- [x] No orphaned references exist; every reference has at least one in-text citation callout.
- [x] In-text citations and Section 7 entries match with 100% numbering fidelity.
