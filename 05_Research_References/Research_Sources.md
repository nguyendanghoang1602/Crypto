# Authoritative Research Sources and Bibliographic Metadata

This document catalogs the primary standards, technical specifications, and official references utilized in the academic report **"Real-World Applications of RSA"**. The numbering matches the reference list in the Microsoft Word report (`RSA_Real_World_Applications_Report.docx`).

---

### [1] PKCS #1: RSA Cryptography Specifications Version 2.2
- **Document Title:** PKCS #1: RSA Cryptography Specifications Version 2.2
- **Authors:** Kathleen Moriarty, Burt Kaliski, Jakob Jonsson, and Andreas Rusch
- **Publishing Organization:** Internet Engineering Task Force (IETF)
- **Series & Number:** Request for Comments (RFC) 8017 (Standard Track)
- **Publication Date:** November 2016
- **Official URL:** https://www.rfc-editor.org/rfc/rfc8017
- **Usage in Report:** Definitive mathematical specification for RSA key representations, the RSASP1/RSAVP1 primitives, RSA-OAEP encryption padding constraints ($mLen \le k - 2hLen - 2$), and RSA-PSS digital signature encoding (EMSA-PSS) with tight security reduction in the Random Oracle Model.

---

### [2] The Transport Layer Security (TLS) Protocol Version 1.3
- **Document Title:** The Transport Layer Security (TLS) Protocol Version 1.3
- **Author:** Eric Rescorla
- **Publishing Organization:** Internet Engineering Task Force (IETF)
- **Series & Number:** Request for Comments (RFC) 8446 (Standards Track)
- **Publication Date:** August 2018
- **Official URL:** https://www.rfc-editor.org/rfc/rfc8446
- **Usage in Report:** Referenced in Sections 1, 2.3, and 4.3 to establish that TLS 1.3 deprecated static RSA key exchange in favor of ephemeral (EC)DHE, leaving RSA's modern role strictly to server identity authentication via X.509 certificates and `CertificateVerify` digital signatures with RSA-PSS.

---

### [3] Digital Signature Standard (DSS)
- **Document Title:** Digital Signature Standard (DSS)
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** Federal Information Processing Standards Publication (FIPS) 186-5
- **Publication Date:** February 2023
- **DOI / URL:** https://csrc.nist.gov/pubs/fips/186-5/final
- **Usage in Report:** Cited in Section 2.2 to document federal approval of the RSA-PSS signature scheme and its normative requirements regarding hash functions and salt generation parameters.

---

### [4] Recommendation for Pair-Wise Key-Establishment Schemes Using Integer Factorization Cryptography
- **Document Title:** Recommendation for Pair-Wise Key-Establishment Schemes Using Integer Factorization Cryptography
- **Authors:** Elaine Barker and Lily Chen
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** NIST Special Publication (SP) 800-56B Revision 2
- **Publication Date:** March 2019
- **DOI / URL:** https://csrc.nist.gov/pubs/sp/800/56b/r2/final
- **Usage in Report:** Cited specifically for Table 2 ("Security strengths of key-establishment schemes") and Appendix D, establishing the authoritative asymptotic security strengths for RSA moduli: RSA-2048 (112 bits), RSA-3072 (128 bits), and RSA-4096 (152 bits) derived from the General Number Field Sieve (GNFS).

---

### [5] Recommendation for Key Management: Part 1 – General
- **Document Title:** Recommendation for Key Management: Part 1 – General
- **Author:** Elaine Barker
- **Publishing Organization:** National Institute of Standards and Technology (NIST)
- **Series & Number:** NIST Special Publication (SP) 800-57 Part 1 Revision 5
- **Publication Date:** May 2020
- **DOI / URL:** https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
- **Usage in Report:** Cited in Section 3 and Table 1 for cryptographic algorithm equivalence, lifespan recommendations, and security strength comparisons for elliptic-curve cryptosystems (secp256k1 and Ed25519 providing 128-bit security).

---

### [6] Schnorr Signatures for secp256k1
- **Document Title:** Schnorr Signatures for secp256k1
- **Authors:** Pieter Wuille, Jonas Nick, and Tim Ruffing
- **Publishing Organization:** Bitcoin Improvement Proposals (BIP)
- **Series & Number:** BIP 340
- **Publication Date:** January 2020
- **Official URL:** https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
- **Usage in Report:** Cited in Sections 1, 3.1, and Table 1 to detail Bitcoin Taproot's 64-byte Schnorr signature standard over secp256k1, highlighting its mathematical linearity, batch verification efficiency, and why it is superior to RSA for consensus-layer transaction verification.

---

### [7] MuSig2 for BIP340-compatible Multi-Signatures
- **Document Title:** MuSig2 for BIP340-compatible Multi-Signatures
- **Authors:** Jonas Nick, Tim Ruffing, and Elliott Jin
- **Publishing Organization:** Bitcoin Improvement Proposals (BIP)
- **Series & Number:** BIP 327
- **Publication Date:** 2023
- **Official URL:** https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki
- **Usage in Report:** Cited in Section 3.1 to distinguish multi-signature aggregation from base BIP 340 Schnorr signatures, illustrating how two-round $n$-of-$n$ threshold signing compacts into a single 64-byte on-chain signature—a capability unattainable with standard RSA.

---

### [8] Segregated Witness (Consensus layer)
- **Document Title:** Segregated Witness (Consensus layer)
- **Authors:** Eric Lombrozo, Johnson Lau, and Pieter Wuille
- **Publishing Organization:** Bitcoin Improvement Proposals (BIP)
- **Series & Number:** BIP 141
- **Publication Date:** December 2015
- **Official URL:** https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
- **Usage in Report:** Cited in Section 3.1 to rigorously explain transaction weight ($\text{Weight} = (\text{Base} \times 3) + \text{Total}$) and virtual size ($\text{vSize} = \lceil \text{Weight} / 4 \rceil$), demonstrating how hypothetical RSA transaction signatures carrying both modulus and signature in each input would add $\approx 407$ witness bytes ($\approx 102\text{ vB}$) per input, expanding virtual transaction size by approximately $72\%$ for a standard 1-input, 2-output P2WPKH transaction (~141 vB baseline). Also notes that public-key caching or off-chain key registries would substantially reduce this overhead.

---

### [9] Edwards-Curve Digital Signature Algorithm (EdDSA)
- **Document Title:** Edwards-Curve Digital Signature Algorithm (EdDSA)
- **Authors:** Simon Josefsson and Ilari Liusvaara
- **Publishing Organization:** Internet Engineering Task Force (IETF)
- **Series & Number:** Request for Comments (RFC) 8032 (Standards Track)
- **Publication Date:** January 2017
- **Official URL:** https://www.rfc-editor.org/rfc/rfc8032
- **Usage in Report:** Cited in Table 1 as an authoritative point of comparison for modern high-performance 128-bit elliptic-curve signatures (Ed25519; 32-byte public key, 64-byte signature; marked as not empirically benchmarked in this study).

---

### [10] Bitcoin Developer Guide: Transactions
- **Document Title:** Bitcoin Developer Guide: Transactions
- **Authors / Organization:** Bitcoin Core Developers
- **Publication Year:** n.d. [Online; accessed 2026]
- **Official URL:** https://developer.bitcoin.org/devguide/transactions.html
- **Usage in Report:** Cited in Section 3.1 regarding standard P2WPKH transaction serialization, witness structure (~105 bytes witness), and consensus overhead.

---

### [11] Ethereum Developer Documentation: Transactions and Cryptographic Signatures
- **Document Title:** Ethereum Developer Documentation: Transactions and Cryptographic Signatures
- **Authors / Organization:** Ethereum Foundation
- **Publication Year:** n.d. [Online; accessed 2026]
- **Official URL:** https://ethereum.org/en/developers/docs/transactions/
- **Usage in Report:** Cited in Sections 1 and 3.1 to document Ethereum's use of ECDSA over secp256k1 for transaction signing, state transition verification, and gas cost economics.

---

### [12] Project Wycheproof: Cryptographic Test Vectors for Asymmetric Algorithms
- **Document Title:** Project Wycheproof: Cryptographic Test Vectors for Asymmetric Algorithms
- **Authors:** Google Security Research (Daniel Bleichenbacher, Thomas Holenstein, Quan Nguyen)
- **Publishing Organization:** Google Security Research
- **Publication Year:** n.d. [Online; accessed 2026]
- **Official URL:** https://github.com/google/wycheproof
- **Usage in Report:** Cited in Section 5.2 and reproduced in `rsa_pss_experiment.py` (test suite `rsa_pss_2048_sha256_mgf1_32_test.json`), validating 108 test vectors (63 valid accepted, 45 invalid rejected) with 100% agreement.
