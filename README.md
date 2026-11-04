# Real-World Applications of RSA: Academic Research & Evaluation Package

This self-contained repository contains the complete research deliverable, source code, experimental data, empirical benchmarks, and reference materials for an independent academic review of the research project:

**"Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication"**

---

## 1. Project Overview

The project provides an in-depth academic study addressing three core dimensions:
1. **WHAT (Theoretical Principles & Mechanics):** Mathematical formulation of RSA key generation ($n = p \cdot q$, $e \cdot d \equiv 1 \pmod{\phi(n)}$), contrasted with the vital operational distinction between asymmetric encryption (RSA-OAEP for confidentiality) and digital signatures (RSA-PSS for authenticity/integrity).
2. **WHY (Purpose & Algorithmic Comparison):** Security analysis across confidentiality, authenticity, and trust. Features an evidence-based comparison between RSA, ECDSA (`secp256k1`), Schnorr (`BIP340`), and `Ed25519`. Examines why public blockchains (Bitcoin, Ethereum) reject RSA for on-chain consensus transactions due to signature/public key size overhead, while off-chain exchange architectures benefit from RSA's rapid verification latency ($e = 65,537$).
3. **HOW (System Design, Implementation & Benchmarking):** An educational case study implementing an off-chain cryptocurrency exchange withdrawal authorization system using RSA-PSS and SHA-256 with deterministic JSON serialization. Includes adversarial security tests (tampering, rogue keys, replay attacks) and empirical benchmarks across RSA (2048, 3072, 4096 bits) and ECDSA (`secp256k1`).

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
│   └── benchmark_performance.png                    # Figure 3: Keygen, signing, and verification latency
│
├── 05_Research_References/
│   ├── Research_Sources.md                          # Annotated bibliography for all 12 authoritative references
│   └── Wycheproof_Test_Vector/
│       ├── rsa_pss_2048_sha256_mgf1_32_test.json    # Official Google Project Wycheproof test suite
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

- **`01_Final_Report/RSA_Real_World_Applications_Report.docx`**: The primary research deliverable. Editable Microsoft Word document formatted to A4 standard, 10.5 pt Times New Roman, 1.04 line spacing, with embedded diagrams and 12 IEEE citations. Verified via Word layout automation (`win32com.client`) to occupy **exactly 5 A4 pages** without overflow.
- **`02_Source_Code/rsa_pss_experiment.py`**: Python 3 implementation of the off-chain withdrawal system, deterministic JSON serializer, 5 security test scenarios, Wycheproof 108-test-case validation harness, and empirical RSA/ECDSA benchmark harness.
- **`03_Experimental_Data/benchmark_results.csv`**: Aggregated empirical benchmark measurements across RSA-2048, RSA-3072, RSA-4096, and ECDSA-secp256k1 derived directly from the raw trial dataset.
- **`03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv`**: Contains every individual trial timestamp (840 rows) recorded synchronously with `time.perf_counter_ns()`.
- **`05_Research_References/Research_Sources.md`**: Bibliographic breakdown detailing the role of RFC 8017, RFC 8446, NIST FIPS 186-5, NIST SP 800-56B Rev. 2, NIST SP 800-57, BIP 340, BIP 327, BIP 141, RFC 8032, and Project Wycheproof.
- **`FINAL_REVIEW_NOTES.md`**: Detailed technical audit log documenting all resolved review items.

---

## 4. Environment Setup and Dependency Installation

### Prerequisites
- Python 3.10+ (Python 3.12 or 3.15 recommended, 64-bit).
- OpenSSL runtime (standard in modern Python distributions).
- Microsoft Word (optional, only required if re-validating native `.docx` pagination).

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
To execute the five operational scenarios, reproduce the complete 108-case Wycheproof suite, and record empirical benchmarks:

```bash
cd 02_Source_Code
python rsa_pss_experiment.py
```

*Note: By default, `rsa_pss_experiment.py` executes the 108 Wycheproof test cases and 5 adversarial security scenarios while safely preserving the existing verified benchmark datasets (`benchmark_results.csv` and `raw_trials_all_algorithms.csv`). To force a re-execution of the benchmark trials and overwrite the CSVs, pass the `--rerun-benchmarks` flag.*

**Expected Terminal Output:**
1. Confirmation that all **108 Wycheproof test cases** passed (63 valid accepted, 45 invalid rejected).
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
- `security_strength_bits`: NIST security strength mapping per **NIST SP 800-56B Rev. 2 Table 2 & Appendix D** (for RSA) and **NIST SP 800-57 Part 1 Rev. 5** (for ECDSA).
- `keygen_median_ms`: Median key generation latency in milliseconds.
- `sign_median_ms`: Median signature generation latency in milliseconds.
- `verify_median_ms`: Median signature verification latency in milliseconds.
- `signature_length_bytes`: Encoded signature size in bytes (256–512 B for RSA; ~71 B DER for ECDSA).
- `modulus_length_bytes`: Public key / modulus size in bytes (256–512 B modulus for RSA; 33 B compressed public key for secp256k1).
- `internal_asymmetry_ratio`: Ratio of `sign_median_ms / verify_median_ms` illustrating internal algorithm asymmetry.

### Key Empirical Findings:
- **Verification Advantage:** RSA-3072 verification ($0.0756\text{ ms}$) is **$8.22\times$ faster** than ECDSA-secp256k1 verification ($0.6214\text{ ms}$); RSA-2048 verification ($0.0462\text{ ms}$) is **$13.45\times$ faster** than ECDSA; RSA-4096 verification ($0.1150\text{ ms}$) is **$5.40\times$ faster** than ECDSA.
- **Signing & Keygen Advantage:** ECDSA signing ($0.7196\text{ ms}$) is **$3.87\times$ faster** than RSA-3072 signing ($2.7834\text{ ms}$); ECDSA keygen ($0.7158\text{ ms}$) is over **$350\times$ faster** than RSA-3072 ($253.9132\text{ ms}$).

---

## 7. Hardware and Software Execution Environment

- **CPU:** AMD Ryzen 5 7520U with Radeon Graphics (4 Physical Cores, 8 Logical Threads @ 2.80 GHz)
- **RAM:** 16.0 GB LPDDR5
- **OS:** Windows 11 Build 26200 (64-bit AMD64)
- **Python:** 3.15.1 (tags/v3.15.1:c37e74c, 64-bit)
- **Cryptographic Backend:** `cryptography` v50.0.2 / OpenSSL 4.0.3 (29 Sep 2026)

---

## 8. Known Limitations and Cryptographic Distinctions

1. **Theoretical vs. System Throughput:** Throughput extrapolations (e.g., ~13,200 verifications/sec per core for RSA-3072 vs. ~1,600 for ECDSA) represent **theoretical isolated cryptographic-operation estimates**. End-to-end exchange throughput is constrained by TCP/TLS network roundtrips, database locks, and risk evaluation latency.
2. **Deterministic Serialization:** The `DeterministicJSONSerializer` implements application-level deterministic formatting (lexicographical key sorting, compact delimiters, UTF-8 encoding). It does not implement full IETF RFC 8785 (which requires ECMAScript IEEE 754 number representation and UTF-16 code unit ordering).
3. **Cryptographic Signature Framing Across Networks:**
   - **Benchmarked ECDSA:** Uses standard OpenSSL/cryptography ASN.1 DER framing (~70–72 bytes).
   - **Bitcoin Network:** Native legacy and SegWit inputs encode ECDSA signatures using strict DER serialization appended with a 1-byte sighash flag (e.g., `SIGHASH_ALL`), yielding a variable size of ~71–73 bytes. Taproot inputs (BIP 341) utilize BIP 340 Schnorr signatures: signatures are **exactly 64 bytes** ($r \parallel s$) when using `SIGHASH_DEFAULT` (0x00), or **65 bytes** when an explicit non-default sighash byte is appended, paired with 32-byte x-only public keys.
   - **Ethereum Network:** Externally Owned Account (EOA) transaction envelopes use secp256k1 ECDSA. In wire transactions (legacy, EIP-2930, and EIP-1559), signature components are serialized as discrete Recursive Length Prefix (RLP) fields encoding $r$, $s$, and $v$ (or `yParity`), rather than a single flat 65-byte string. While off-chain APIs commonly concatenate these into a 65-byte $r \parallel s \parallel v$ format, standard **ERC-2098** defines a compact 64-byte representation ($r \parallel (yParity \ll 255 \mid s)$) that saves gas in smart contracts. A generic fixed-width 64-byte $r \parallel s$ representation is distinct from both Bitcoin's DER encoding and Ethereum's RLP envelope.
4. **Native vs. Smart-Contract Execution (EIP-198 Limitations):** While public blockchain consensus rules mandate ECC for native transaction envelopes, smart contracts on Ethereum can execute big-integer modular arithmetic via the EVM precompile at address `0x05` (EIP-198). Crucially, precompile `0x05` performs **modular exponentiation ($B^E \bmod M$) only**; complete RSA-PSS verification requires separate smart-contract logic to execute MGF1 mask generation, EMSA-PSS padding validation, and SHA-256 digest comparison.
5. **RSA Side-Channel and Fault Countermeasures:** RSA base blinding ($x' = x \cdot r^e \bmod n$) mitigates timing side-channel attacks. However, blinding alone does not prevent hardware fault injection such as the Bellcore attack on Chinese Remainder Theorem (CRT) implementations (where an induced fault during one prime exponentiation yields $\gcd(s - s', n) \in \{p, q\}$, revealing a nontrivial prime factor of $n = p \times q$ depending on which CRT branch remains correct, where $s$ is the correct signature and $s'$ is the faulty signature); defending against CRT fault attacks requires separate countermeasures, such as post-computation signature verification ($s^e \bmod n \equiv m$) prior to release, or redundant fault-detection circuits.
6. **Bitcoin SegWit vs. Hypothetical RSA Witness Analysis:** A standard 1-input, 2-output P2WPKH transaction has a typical witness stack of ~107–109 bytes (1-byte stack item count, 1-byte signature length prefix, ~71–73 bytes DER signature plus sighash byte, 1-byte public key length prefix, and 33-byte compressed public key). For a hypothetical RSA-2048 witness carrying two separate stack items (256-byte modulus and 256-byte signature, each with a 3-byte CompactSize prefix for 256-byte items), the witness size equals $1 + 3 + 256 + 3 + 256 = 519\text{ bytes}$. Compared with standard P2WPKH, this adds approximately 410–412 witness bytes per input ($\approx 103\text{ additional virtual bytes}$, subject to transaction weight rounding), representing an approximately $73\%$ hypothetical virtual size expansion for a baseline 141-vB transaction. This analysis is strictly hypothetical; native Bitcoin RSA verification is not supported (Bitcoin script lacks native RSA verification opcodes), the model assumes both values are carried in each input, and alternative key-storage designs would alter the overhead.

---

## 9. Missing or Unavailable Files

- **None.** All source scripts, final Word documents, raw data tables, figures, execution logs, and official test vectors are present, verified, and self-contained within this archive.
