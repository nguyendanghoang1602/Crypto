# Real-World Applications of RSA: Academic Research & Evaluation Package

This self-contained repository contains the complete research deliverable, source code, experimental data, empirical benchmarks, and reference materials for an independent academic review of the research project:

**"Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication"**

---

## 1. Project Overview

The project provides an in-depth academic study addressing three core dimensions:
1. **WHAT (Theoretical Principles & Mechanics):** Mathematical formulation of RSA key generation ($n = p \cdot q$, $e \cdot d \equiv 1 \pmod{\lambda(n)}$ or $\phi(n)$), contrasted with the vital operational distinction between asymmetric encryption (RSA-OAEP in the Random Oracle Model for hybrid key transport, with foundational proofs from Bellare-Rogaway 1994 [17], Shoup 2001 [15], and Fujisaki et al. 2001 [16]) and digital signatures (RSA-PSS per RFC 8017 Section 8.1/9.1 and NIST FIPS 186-5 with explicit primitives: message octet string $M$, message digest $mHash = \text{Hash}(M)$, encoded message $EM = \text{EMSA-PSS-ENCODE}(M, \text{emBits})$, integer representative $m = \text{OS2IP}(EM)$, signature generation $s = \text{RSASP1}(SK, m)$, and signature octets $S = \text{I2OSP}(s, k)$; verification executes $s = \text{OS2IP}(S) \to m = \text{RSAVP1}(PK, s) = s^e \bmod n \to EM = \text{I2OSP}(m, \text{emLen}) \to \text{EMSA-PSS-VERIFY}(M, EM, \text{emBits})$, establishing that modular exponentiation alone does not prove validity without EMSA-PSS decoding), enforcing NIST FIPS 186-5 Section 5.1 key separation.
2. **WHY (Purpose & Algorithmic Comparison):** Security analysis across confidentiality, authenticity, and trust. Features an evidence-based comparison between RSA, ECDSA (`secp256k1`), Schnorr (`BIP340`), and `Ed25519`. Examines why public blockchains (Bitcoin, Ethereum) mandate elliptic-curve cryptography for on-chain consensus transactions due to signature and public key compactness, while off-chain exchange architectures benefit from RSA's rapid verification latency ($e = 65,537$).
3. **HOW (System Design, Implementation & Benchmarking):** An educational case study implementing an off-chain cryptocurrency exchange withdrawal authorization system using RSA-PSS and SHA-256 with deterministic JSON serialization. Includes adversarial security tests (payload tampering, rogue keys, replay attacks) and empirical benchmarks across RSA (2048, 3072, 4096 bits) and ECDSA (`secp256k1`).

---

## 2. Directory Structure

```text
RSA_Project_Review_Final/
│
├── 01_Final_Report/
│   └── RSA_Real_World_Applications_Report.docx       # Primary audited Word report (strictly 5 A4 pages)
│
├── 02_Source_Code/
│   ├── rsa_pss_experiment.py                        # Executable experiment suite, scenarios & benchmarks
│   ├── build_report_doc.py                          # Compiles the publication-grade Word report
│   └── generate_figures.py                          # Generates high-resolution academic diagrams
│
├── 03_Experimental_Data/
│   ├── benchmark_results.csv                        # Final aggregated benchmark statistics (median, mean, std)
│   ├── raw_benchmark_logs/
│   │   └── raw_trials_all_algorithms.csv            # Verbatim 840 individual trial timing records
│   └── test_execution_logs/
│       ├── test_scenarios_and_benchmarks.log        # Full console execution transcript
│       └── wycheproof_reproduction.log              # Official Wycheproof 108-test-case validation log
│
├── 04_Figures/
│   ├── rsa_pss_workflow.png                         # Figure 1: RSA-PSS EMSA encoding and verification flow
│   ├── withdrawal_architecture.png                  # Figure 2: Off-chain exchange withdrawal authorization
│   └── benchmark_performance.png                    # Figure 3: Median latency comparison for RSA and ECDSA
│
├── 05_Research_References/
│   ├── Research_Sources.md                          # Annotated bibliography for all 17 authoritative references
│   └── Wycheproof_Test_Vector/
│       ├── rsa_pss_2048_sha256_mgf1_32_test.json    # Bundled Wycheproof test suite snapshot (v0.9, 108 cases)
│       └── README_wycheproof.md                     # Test vector metadata and reproduction notes
│
├── 06_Environment/
│   ├── requirements.txt                             # Exact pinned Python package dependencies
│   └── environment_info.txt                         # Detailed hardware and operating system specifications
│
├── FINAL_REVIEW_NOTES.md                            # Comprehensive technical audit and consistency log
├── SHA256SUMS.txt                                   # Cryptographic integrity manifest for all package files
└── README.md                                        # This documentation file
```

---

## 3. Description of Core Files

- **`01_Final_Report/RSA_Real_World_Applications_Report.docx`**: The primary research deliverable. Editable Microsoft Word document formatted to A4 standard, 9.5 pt Times New Roman, 1.0 line spacing, with embedded diagrams and 17 IEEE citations. Verified via Word layout automation (`win32com.client` using Kingsoft WPS Office 12.1.0.29162) to occupy **exactly 5 A4 pages** without overflow.
- **`02_Source_Code/rsa_pss_experiment.py`**: Python 3 implementation of the off-chain withdrawal system, deterministic JSON serializer, 5 security test scenarios, Wycheproof 108-test-case validation harness, and empirical RSA/ECDSA benchmark harness.
- **`03_Experimental_Data/benchmark_results.csv`**: Aggregated empirical benchmark measurements across RSA-2048, RSA-3072, RSA-4096, and ECDSA-secp256k1 derived directly from the raw trial dataset.
- **`03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv`**: Contains every individual trial timestamp (840 rows) recorded synchronously with `time.perf_counter_ns()`.
- **`05_Research_References/Research_Sources.md`**: Complete bibliographic breakdown detailing the role of 17 primary technical sources: Rivest-Shamir-Adleman (CACM 1978 / MIT 1977), RFC 8017, RFC 9846 (TLS 1.3) / RFC 9963, NIST FIPS 186-5, NIST SP 800-56B Rev. 2, NIST SP 800-57, Boneh et al. (Bellcore fault attack), BIP 340, BIP 141, BIP 327, RFC 8032, Bitcoin Dev Guide, Ethereum Dev Documentation, Project Wycheproof (v0.9 snapshot), Shoup (OAEP Reconsidered), Fujisaki et al. (RSA-OAEP Security), and Bellare & Rogaway (Optimal Asymmetric Encryption).
- **`FINAL_REVIEW_NOTES.md`**: Detailed technical audit log documenting all resolved review items.

---

## 4. Environment Setup and Dependency Installation

### Prerequisites
- Python 3.10+ (Python 3.12 or 3.15 recommended, 64-bit).
- OpenSSL runtime (standard in modern Python distributions).
- Microsoft Word or compatible word processor (optional, only required if re-validating native `.docx` pagination).

### Installation Steps
Open a terminal in the root directory:

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Linux / macOS:
source venv/bin/activate

# 2. Install dependencies
pip install -r 06_Environment/requirements.txt
```

---

## 5. How to Run the Experiments and Reproduce Benchmarks

### Step 1: Run the Complete Security and Benchmark Suite
To execute the five operational scenarios, reproduce the bundled 108-case Wycheproof suite, and review empirical benchmarks:

```bash
cd 02_Source_Code
python rsa_pss_experiment.py
```

*Note: By default, `rsa_pss_experiment.py` executes the 108 Wycheproof test cases and 5 adversarial security scenarios while safely preserving the existing verified benchmark datasets (`benchmark_results.csv` and `raw_trials_all_algorithms.csv`). To force a re-execution of the benchmark trials and overwrite the CSVs, pass the `--rerun-benchmarks` flag.*

**Expected Terminal Output:**
1. Confirmation that all **108 bundled Wycheproof test cases** passed (63 valid accepted, 45 invalid rejected). Validates execution against this selected verification test set (version 0.9 snapshot); does not claim exhaustive mathematical proof of all RFC 8017 edge cases. (Active upstream C2SP repository contains an expanded number of test vectors).
2. Execution and approval of **Scenario 1** (Valid withdrawal request with integer atomic units).
3. Detection and rejection of **Scenario 2** (Tampered amount 12.5 ETH $\rightarrow$ 50.0 ETH equivalent).
4. Detection and rejection of **Scenario 3** (Tampered recipient address).
5. Detection and rejection of **Scenario 4** (Rogue public key).
6. Detection and rejection of **Scenario 5** (Replay attack blocked by application-level state engine).

### Step 2: Regenerate Figures (Optional)
```bash
python generate_figures.py
```

### Step 3: Rebuild the Word Document Report (Optional)
```bash
python build_report_doc.py
```

---

## 6. Interpretation of `benchmark_results.csv`

The CSV contains the following columns:
- `algorithm`: The evaluated cryptographic scheme (`RSA-2048`, `RSA-3072`, `RSA-4096`, `ECDSA-secp256k1`).
- `key_size_bits`: Modulus size in bits for RSA; curve order bit-length for ECDSA.
- `security_strength_bits`: NIST security strength mapping per **NIST SP 800-56B Rev. 2 Table 2 & Appendix D** (for RSA) and generic 256-bit EC mapping per **NIST SP 800-57 Part 1 Rev. 5** (for ECDSA).
- `keygen_median_ms`: Median key generation latency in milliseconds.
- `sign_median_ms`: Median signature generation latency in milliseconds.
- `verify_median_ms`: Median signature verification latency in milliseconds.
- `signature_length_bytes`: Encoded signature size in bytes (256–512 B for RSA; sample 71 B DER for ECDSA, which varies between 70–72 B).
- `modulus_length_bytes`: Public key / modulus size in bytes (256–512 B modulus for RSA; 33 B compressed public key for secp256k1).
- `internal_asymmetry_ratio`: Ratio of `sign_median_ms / verify_median_ms` illustrating internal algorithm asymmetry.

### Key Empirical Findings:
- **Equivalent 128-bit Comparison:** Comparing equivalent 128-bit classical security strengths (RSA-3072 vs. ECDSA-secp256k1), RSA-3072 verification ($0.0756\text{ ms}$) is **$8.22\times$ faster** than ECDSA-secp256k1 verification ($0.6214\text{ ms}$). Conversely, ECDSA signing ($0.7196\text{ ms}$) is **$3.87\times$ faster** than RSA-3072 signing ($2.7834\text{ ms}$), and ECDSA keygen ($0.7158\text{ ms}$) is over **$350\times$ faster** than RSA-3072 ($253.9132\text{ ms}$).
- **Different-Security Configurations:** RSA-2048 verification ($0.0462\text{ ms}$) is **$13.45\times$ faster** than ECDSA, but provides only ~112-bit security. RSA-4096 verification ($0.1150\text{ ms}$) is **$5.40\times$ faster** than ECDSA, but provides ~152-bit security.
- **Environment Specificity:** Performance ratios reflect the measured Python 3.15 / OpenSSL 4.0.3 execution environment on an AMD Ryzen 5 7520U; relative performance may vary across different CPU instruction sets (such as AVX-512) and compiled cryptographic libraries.

---

## 7. Hardware and Software Execution Environment

- **CPU:** AMD Ryzen 5 7520U with Radeon Graphics (4 Physical Cores, 8 Logical Threads @ 2.80 GHz)
- **RAM:** 16.0 GB LPDDR5
- **OS:** Windows 11 Build 26200 (64-bit AMD64)
- **Python:** 3.15.1 (tags/v3.15.1:c37e74c, 64-bit)
- **Cryptographic Backend:** `cryptography` v50.0.2 / OpenSSL 4.0.3 (29 Sep 2026)

---

## 8. Known Limitations and Cryptographic Distinctions

1. **Theoretical vs. System Throughput:** Throughput extrapolations (e.g., ~13,200 verifications/sec per core for RSA-3072 vs. ~1,600 for ECDSA) represent **isolated cryptographic-operation estimates**, not an end-to-end exchange gateway throughput benchmark. Real-world system throughput is constrained by TCP/TLS network roundtrips, database locks, and business-tier evaluation latency.
2. **Prototype Scope and Boundaries:**
   - **In-Memory Nonce Cache:** The educational prototype verifies and stores processed nonces sequentially in an in-memory Python set. While appropriate for educational demonstration, production systems require strictly atomic check-and-insert logic (e.g., Redis SETNX or SQL unique constraint transactions) to prevent race conditions under concurrent requests, backed by a persistent datastore with TTL expiry across distributed instances.
   - **Address Validation Sanity Check:** Destination address verification in the prototype is a basic format sanity check (verifying 0x hex prefix and length). Production systems require full checksum validation (EIP-55 for Ethereum, Bech32/Bech32m for Bitcoin) alongside account balance checks, withdrawal thresholds, and AML screening.
   - **Deterministic Serialization:** The `DeterministicJSONSerializer` implements application-level deterministic formatting (lexicographical key sorting, compact delimiters, UTF-8 encoding). It does not implement full IETF RFC 8785 (which requires ECMAScript IEEE 754 number representation and UTF-16 code unit ordering).
   - **Key Lifecycle & Custody:** Signing private keys reside in process memory for educational demonstration. Production financial gateways deploy appropriately validated HSMs or secure hardware—preferring active FIPS 140-3 validated modules for new procurements, while recognizing legacy FIPS 140-2 modules (transitioned to the NIST CMVP Historical List in September 2026) for existing systems—based on the operational threat model, regulatory environment, and institutional key-management policies, integrated with a complete PKI for certificate revocation (CRLs/OCSP) and key rotation.
3. **Cryptographic Signature Framing Across Networks:**
   - **Benchmarked ECDSA:** Uses standard OpenSSL/cryptography ASN.1 DER framing (~70–72 bytes; recorded sample 71 bytes).
   - **Bitcoin Network:** Native legacy and SegWit inputs encode ECDSA signatures using strict DER serialization appended with a 1-byte sighash flag (e.g., `SIGHASH_ALL`), yielding a variable size of ~71–73 bytes. Taproot inputs (BIP 341) utilize BIP 340 Schnorr signatures: signatures are **exactly 64 bytes** ($r \parallel s$) when using `SIGHASH_DEFAULT` (0x00), or **65 bytes** when an explicit non-default sighash byte is appended, paired with 32-byte x-only public keys.
   - **Ethereum Network:** Externally Owned Account (EOA) transaction envelopes use secp256k1 ECDSA. In wire transactions (legacy, EIP-2930, and EIP-1559), signature components are serialized as discrete Recursive Length Prefix (RLP) fields encoding $r$, $s$, and $v$ (or `yParity`), rather than a single flat 65-byte string. While off-chain APIs commonly concatenate these into a 65-byte $r \parallel s \parallel v$ format, standard **ERC-2098** defines a compact 64-byte representation ($r \parallel (yParity \ll 255 \mid s)$) that saves calldata gas.
4. **Native vs. Smart-Contract Execution (EIP-198 Limitations):** While public blockchain consensus rules mandate ECC for native transaction envelopes, smart contracts on Ethereum can execute big-integer modular arithmetic via the EVM precompile at address `0x05` (EIP-198). Crucially, precompile `0x05` performs **modular exponentiation ($B^E \bmod M$) only**; complete RSA-PSS verification requires separate smart-contract logic to execute MGF1 mask generation, EMSA-PSS padding validation, and SHA-256 digest comparison.
5. **RSA Side-Channel and Bellcore CRT Fault Countermeasures:**
   - In CRT-based signing, the signer computes $s_p = m^{d_p} \bmod p$ and $s_q = m^{d_q} \bmod q$, where $m = \text{OS2IP}(EM)$ is the integer message representative produced by `EMSA-PSS-ENCODE(M)` (RFC 8017 Section 8.1 / 9.1). Correct signature $s$ satisfies $s^e \equiv m \pmod n$. Bellcore fault attacks operate under two distinct formulations:
     - **Two-Signature Formulation:** Requires one correct signature $s$ and one faulty signature $s'$ generated from the **exact same** encoded message representative $m = \text{OS2IP}(EM)$ (identical salt and padding). If a fault corrupts $s_q$ into $s'_q$ while $s_p$ remains uncorrupted, $s' \equiv s \pmod p$ and $s' \not\equiv s \pmod q$, yielding $\gcd(s - s', n) = p$ (or $q$ if $s_p$ is faulted); thus $\gcd(s - s', n) \in \{p, q\}$. Crucially, because RSA-PSS randomizes the salt, independent signing executions on message $M$ yield differing encodings ($EM_1 \ne EM_2 \implies m_1 \ne m_2$); two signatures with differing salts do NOT satisfy this condition.
     - **Single-Fault Formulation:** An attacker knowing the exact representative $m$ of faulty signature $s'$ factors $n$ via $\gcd((s')^e - m, n) \in \{p, q\}$. This requires knowledge of the exact encoded representative $m$ of that specific faulty execution, not merely application message $M$. While any valid signature reveals its own representative via $s^e \bmod n$, it does not reveal the representative of an independently salted faulty execution.
   - **Countermeasure Delineation:** Countermeasures must remain strictly differentiated: (1) RSA base blinding ($x' = x \cdot r^e \bmod n$) mitigates timing side-channel attacks by randomizing intermediate modular values; crucially, base blinding does NOT prevent CRT fault injection; (2) Defending against CRT fault attacks requires post-computation signature verification—where the signer verifies $m_{check} = s^e \bmod n$ against $m = \text{OS2IP}(EM)$ and validates EMSA-PSS consistency before releasing $s$—or (3) redundant dual-rail fault-detection hardware.
6. **TLS 1.3 Standards (RFC 9846, RFC 9963, RFC 10024):** In TLS 1.3 (RFC 9846, published July 2026, Standards Track, superseding RFC 8446), static RSA key exchange was entirely removed. Forward Secrecy is provided by ephemeral key exchange ((EC)DHE) and PSK-DHE (`psk_dhe_ke`). In contrast, PSK-only mode (`psk_ke`) does not provide Forward Secrecy against compromised pre-shared keys, and 0-RTT early data lacks Forward Secrecy and is vulnerable to replay attacks. Post-quantum hybrid protection depends on negotiating a supported hybrid mechanism (RFC 10024, pairing classical curves with ML-KEM). Modern TLS 1.3 server authentication with RSA keys strictly mandates RSA-PSS for `CertificateVerify` messages; RFC 9963 introduces a restricted legacy exception for client certificate authentication with PKCS#1 v1.5 in specialized enterprise environments.
7. **Bitcoin SegWit vs. Hypothetical RSA Witness Analysis:** A standard 1-input, 2-output P2WPKH transaction has a typical witness stack of ~107–109 bytes (1-byte stack item count, 1-byte signature length prefix, ~70–72 bytes DER signature plus sighash byte, 1-byte public key length prefix, and 33-byte compressed public key). For a hypothetical RSA-2048 witness carrying two separate stack items (256-byte modulus and 256-byte signature, each with a 3-byte CompactSize prefix for 256-byte items), the witness size equals $1 + 3 + 256 + 3 + 256 = 519\text{ bytes}$. Compared with standard P2WPKH, this adds approximately 410–412 witness bytes per input ($\approx 103\text{ additional virtual bytes}$, subject to transaction weight rounding), representing an approximately $73\%$ hypothetical virtual size expansion for a baseline 141-vB transaction. This analysis is strictly hypothetical; native Bitcoin RSA verification is not supported (Bitcoin script lacks native RSA verification opcodes), the model assumes both values are carried in each input, and alternative key-storage designs would alter the overhead.

8. **RSA-OAEP Security & Maximum Payload:** Modern systems deploy RSA-OAEP (RFC 8017 Section 7.1; RFC 8017 is an Informational RFC). In the Random Oracle Model (ROM), Bellare and Rogaway (1994) [17] introduced OAEP and established semantic security against chosen-plaintext attacks (IND-CPA) and plaintext awareness (implying IND-CCA1 for general trapdoor permutations). Shoup (2001) [15] demonstrated that the general IND-CCA2 security proof claim could not be established for arbitrary trapdoor permutations via standard black-box reductions, identified the critical relevance of partial-domain one-wayness, and proposed the provably secure variant OAEP+. Fujisaki, Okamoto, Pointcheval, and Stern (2001) [16] established IND-CCA2 security specifically for RSA-OAEP in the ROM under the standard RSA one-wayness assumption by demonstrating that partial-domain one-wayness is mathematically equivalent to full-domain one-wayness for the RSA permutation, though the concrete security reduction is non-tight for practical RSA key lengths. Plaintext length is bounded by $mLen \le k - 2hLen - 2$ (maximum 190 bytes for RSA-2048 with SHA-256); industrial architectures deploy it within hybrid encryption for RSA key transport (encapsulating ephemeral symmetric keys per NIST SP 800-56B Rev. 2).
9. **Cryptographic Key Separation (NIST FIPS 186-5 Section 5.1):** NIST FIPS 186-5 Section 5.1 explicitly dictates that an RSA key pair designated for digital signatures shall not be used for key establishment or encryption (RSA-OAEP). Multi-purpose key reuse exposes systems to cross-protocol interaction attacks. Separate key pairs, distinct certificates, and independent policies are strictly enforced.
10. **Public Exponent $e = 65537$ Operation Count:** $e = 65537 = 2^{16} + 1 = 10000000000000001_2$ (17 bits, Hamming weight 2). Straightforward binary square-and-multiply exponentiation executes in exactly 16 squarings and 1 modular multiplication (total 17 operations), qualifying as an algorithmic operation count rather than an implementation-independent latency guarantee.
11. **EMSA-PSS General Specification ($	ext{emBits} = 	ext{modBits} - 1$):** Per RFC 8017 Section 9.1, EMSA-PSS defines $\text{emBits} = \text{modBits} - 1$ to guarantee that the integer message representative satisfies $m = \text{OS2IP}(EM) < n$. For a 2048-bit modulus, $\text{emBits} = 2047$ bits and $\text{emLen} = 256$ bytes, with salt length $sLen \le \text{emLen} - hLen - 2$ ($32 \le 222$).

---

## 9. Academic Course Alignment & Lecture Slide Reference Materials

The research project aligns directly with the seven university lecture slide collections:
- **Verified University Lecture Syllabus (Sessions 1–7):** The seven course slide collections represent the complete verified instructional sequence:
  - *Session 1:* Cryptography concepts, security objectives (confidentiality, integrity, authenticity), and classical cipher foundations.
  - *Session 2:* Mathematical foundations (modular arithmetic, Euclidean / Extended Euclidean algorithms, prime fields $\mathbb{Z}_p$).
  - *Session 3:* Symmetric encryption, Feistel ciphers, DES, AES structure, and block cipher operational modes.
  - *Session 4:* Asymmetric public-key cryptography, Diffie-Hellman key exchange, RSA key generation ($n = p \cdot q$, $\phi(n)$), and modular exponentiation.
  - *Session 5:* Cryptographic hash functions (MD5, SHA-1, SHA-256), collision resistance, and preimage resistance properties.
  - *Session 6:* Digital signature schemes, message authentication, and existential unforgeability under chosen-message attacks (EUF-CMA).
  - *Session 7:* Elliptic Curve Cryptography (ECC), elliptic-curve discrete logarithm problem (ECDLP), ECDSA, and performance/size trade-offs relative to RSA.
- All seven available lecture collections were inspected and cross-referenced to ensure consistent mathematical definitions, exponent derivations ($e \cdot d \equiv 1 \pmod{\phi(n)}$ or $\lambda(n)$), and pedagogical alignment across the report and implementation.

---

## 10. Missing or Unavailable Files

- **None.** All source scripts, final Word documents, raw data tables, figures, execution logs, and official test vectors are present, verified, and self-contained within this repository.
