# Final Technical Audit and Consistency Review Notes

**Project Title:** Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication  
**Author / Research Assistant:** Antigravity Academic Assistant  
**Date of Audit:** November 2026 (Final Targeted Polish)  
**Environment:** AMD Ryzen 5 7520U @ 2.80 GHz (4 cores / 8 threads), 16 GB RAM, Windows 11 Build 26200, Python 3.15.1, `cryptography` v50.0.2, OpenSSL 4.0.3  

---

## 1. Executive Summary of Consistency Resolutions & Targeted Polish

This document records the complete technical audit and targeted polish performed on the academic research artifact. All peer-review recommendations have been addressed without modifying the approved topic, altering the What–Why–How structure, or modifying the verified experimental benchmark dataset.

| Review Area | Initial Peer-Review Item | Final Technical Resolution | Verification Status |
|---|---|---|---|
| **Bitcoin Taproot (BIP 341)** | Clarification of Taproot Schnorr signature length variants. | Explained that BIP 341 signatures are **64 bytes** under `SIGHASH_DEFAULT` (0x00), but can be **65 bytes** when an explicit non-default sighash byte (e.g. `SIGHASH_ALL`, `SIGHASH_NONE`, `SIGHASH_SINGLE`, or with `ANYONECANPAY`) is appended. | **Verified** in Table 1, Section 3.1, and README. |
| **Ethereum Precompile (EIP-198)** | Precompile `0x05` conflated with a full RSA-PSS signature verifier. | Explicitly clarified that EVM precompile `0x05` performs **modular exponentiation ($B^E \bmod M$) only**. Complete RSA-PSS verification additionally requires separate smart-contract logic to execute MGF1 mask generation, extract and validate the encoded message ($EM$), and verify the salt, hash, and padding byte consistency. | **Verified** in Section 3.1 and README. |
| **RSA Security Countermeasures** | Implication that RSA blinding alone prevents Bellcore CRT fault attacks. | Delineated countermeasures: RSA base blinding ($x' = x \cdot r^e \bmod n$) specifically mitigates **timing side-channel attacks**. Defending against **hardware fault injection / Bellcore CRT attacks** requires separate countermeasures, such as post-computation signature verification ($s^e \bmod n \equiv m$) prior to release, or redundant fault-detection circuits. | **Verified** in Section 3.2 and README. |
| **Ethereum Signature Framing** | Conflation of flat 65-byte $r \parallel s \parallel v$ string with wire transaction serialization. | Differentiated representations: on-chain Ethereum wire envelopes (legacy, EIP-2930, EIP-1559) serialize signatures as discrete Recursive Length Prefix (RLP) fields. While off-chain APIs commonly concatenate these into a 65-byte $r \parallel s \parallel v$ format, standard **ERC-2098** defines a compact 64-byte representation ($r \parallel (yParity \ll 255 \mid s)$) to minimize calldata overhead. | **Verified** in Table 1, Section 3.1, and README. |
| **Abstract Phrasing** | Claimed "strict compliance with RFC 8017" and that replay caches "guarantee end-to-end security"; used "fault injection". | Precise phrasing: passed 108 selected Wycheproof vectors (63 valid accepted, 45 invalid rejected). Replaced "fault injection" with "adversarial security testing". Replaced absolute security guarantee with defense-in-depth explanation. Reported all ratios (RSA-2048: 13.45x, RSA-3072: 8.22x, RSA-4096: 5.40x) and identified RSA-3072 vs. ECDSA as 128-bit comparison. | **Verified** in Abstract & Executive Summary. |
| **Blockchain Economics & Fees** | Conflated Bitcoin miner fees with Ethereum gas; generic $>70\%$ transaction expansion without explicit assumptions. | Differentiated fee models: Bitcoin fees depend on virtual size (vSize) $\times$ feerate (sat/vB); Ethereum execution uses gas. Formulated BIP 141 calculation under explicit template: 1-input, 2-output P2WPKH (~141 vB baseline) adds ~102 vB (~72% expansion) assuming modulus and signature are both carried in each input; noted public-key registries substantially reduce this. | **Verified** in Section 3.1, Section 6, and README. |
| **Code Exception Handling** | Broad `except (InvalidSignature, Exception):` swallowed non-cryptographic errors. | Refactored `RSAVerifier.verify()` and `run_wycheproof_suite()` to catch specifically `(InvalidSignature, ValueError)`. Preserved verified benchmark datasets by default; added `--rerun-benchmarks` flag. | **Verified**: 108/108 Wycheproof cases and 5 scenarios pass cleanly. |
| **README & CSV Fields** | CSV column mislabeled as `public_key_length_bytes`. | Updated README field description to actual CSV header `modulus_length_bytes`. Replaced "fault injection" with "adversarial security tests". Detailed exact signature framing distinctions across Bitcoin, Ethereum, and generic formats. | **Verified** in `README.md`. |
| **Document Pagination** | Strict 5 A4 page maximum requirement. | Tuned margin (1.65 cm top/bottom, 1.75 cm left/right), image widths (3.8–3.95 in), and paragraph spacing. Verified via Word COM automation (`doc.ComputeStatistics(2)`). | **Exactly 5 A4 pages** (Word count: 3,493 words). |

---

## 2. Experimental Verification Details

### 2.1 Benchmark Results (Median Latencies & Ratios)
- **Hardware/Software:** AMD Ryzen 5 7520U, Python 3.15.1, `cryptography` v50.0.2, OpenSSL 4.0.3.
- **Dataset:** 840 individual measurements recorded in `raw_trials_all_algorithms.csv`.

| Algorithm | Security Strength | Keygen Median | Sign Median | Verify Median | Signature Size | Internal Asymmetry (Sign / Verify) | Relative Verify vs ECDSA |
|---|---|---:|---:|---:|---:|---:|---:|
| **RSA-2048** | 112 bits (NIST SP 800-56B) | 50.0708 ms | 0.9005 ms | 0.0462 ms | 256 B | 19.49x | **13.45x faster** |
| **RSA-3072** | 128 bits (NIST SP 800-56B) | 253.9132 ms | 2.7834 ms | 0.0756 ms | 384 B | 36.82x | **8.22x faster** |
| **RSA-4096** | 152 bits (NIST SP 800-56B) | 633.0616 ms | 6.5425 ms | 0.1150 ms | 512 B | 56.89x | **5.40x faster** |
| **ECDSA-secp256k1** | 128 bits (NIST SP 800-57) | 0.7158 ms | 0.7196 ms | 0.6214 ms | ~71 B (DER) | 1.16x | Baseline (1.0x) |

#### Analytical Synthesis:
1. **Asymmetric Verification Advantage:** RSA verification ($e = 65,537$) executes with minimal modular multiplications. At the approximately equivalent 128-bit security level, RSA-3072 verifies in $0.0756\text{ ms}$—**8.22x faster** than ECDSA-secp256k1 ($0.6214\text{ ms}$).
2. **Keygen & Signing Cost:** ECDSA signing is **3.87x faster** than RSA-3072 ($0.7196\text{ ms}$ vs. $2.7834\text{ ms}$), and ECDSA key generation is over **350x faster** than RSA-3072 ($0.7158\text{ ms}$ vs. $253.9132\text{ ms}$).
3. **Architectural Niche:** Public blockchain consensus mandates ECC due to compact signatures that minimize block serialization and storage costs. Conversely, off-chain withdrawal verification gateways—where signature verification is performed millions of times against pre-established keys—derive tangible throughput benefits from RSA's fast verification.

### 2.2 Operational Security Scenarios Tested
- **Scenario 1 (Valid Payload):** 12.5 ETH atomic withdrawal -> `ACCEPTED`.
- **Scenario 2 (Amount Tampering):** 12.5 ETH tampered to 50.0 ETH -> `REJECTED (Invalid Signature)`.
- **Scenario 3 (Recipient Tampering):** Destination address modified to attacker -> `REJECTED (Invalid Signature)`.
- **Scenario 4 (Rogue Public Key):** Evaluated against unauthorized key -> `REJECTED (Invalid Signature)`.
- **Scenario 5 (Replay Attack):** Exact payload resubmitted -> Cryptographic signature passed (`True`), but validation engine detected duplicate nonce `a8f9c10e-8215-4c07-b649-1d2e3f4a5b6c` -> `REJECTED BY APPLICATION STATE ENGINE`.

### 2.3 Wycheproof RFC 8017 Compliance
- **Suite:** `rsa_pss_2048_sha256_mgf1_32_test.json` (Google Security Research).
- **Result:** **108/108 passed** (63 valid accepted, 45 invalid rejected). Logged to `03_Experimental_Data/test_execution_logs/wycheproof_reproduction.log`.

---

## 3. Deliverable Verification & Pagination Audit

- **Document Path:** `01_Final_Report/RSA_Real_World_Applications_Report.docx`
- **Page Count:** **Exactly 5 A4 pages** (verified via `win32com.client` `doc.ComputeStatistics(2) == 5`).
- **Word Count:** 3,493 words.
- **Figures Included:** Figure 1 (RSA-PSS flow), Figure 2 (Withdrawal architecture), Figure 3 (Empirical latency distributions).
- **Tables Included:** Table 1 (Cryptographic comparison), Table 2 (Empirical benchmark results).
- **Code Artifacts:** Algorithm 1 (Withdrawal verification pipeline pseudocode).
- **References:** 12 IEEE-style citations, ending cleanly on Page 5.

---

## 4. Transparent Verification Logs Audit (Explanation of Non-Zero Exit Codes)

During development and automated auditing sessions, four specific commands returned exit code 1. To ensure complete academic transparency, each event was investigated and documented below:

1. **PowerShell Process Cleanup Command (`Exit Code 1`):**
   - *Command:* `Get-Process winword, wps -ErrorAction SilentlyContinue | Stop-Process -Force`
   - *Cause:* In PowerShell, piping `Get-Process` into `Stop-Process` emits exit code 1 when no processes named `winword` or `wps` are currently running on the host machine.
   - *Nature:* Routine shell diagnostic behavior; no application or test failure occurred.

2. **Word COM Dynamic Dispatch `.Quit()` Call (`Exit Code 1`):**
   - *Command:* Python COM test script executing `word.Quit()` via `win32com.client.Dispatch('Word.Application')`.
   - *Cause:* On the host environment running WPS Office (which registers as Word Application 12.0), `win32com.client.dynamic` dynamic dispatch did not bind `.Quit()` directly on the wrapper object, raising `AttributeError: Word.Application.Quit`.
   - *Resolution:* Replaced with `win32com.client.DispatchEx('Word.Application')` and wrapped the cleanup in a robust `try...finally` block.

3. **COM Paragraph Range Inspection Exception (`Exit Code 1`):**
   - *Command:* Python COM one-liner iterating `doc.Paragraphs` and querying `p.Range.Information(3)`.
   - *Cause:* Querying `Information(3)` across complex table borders and drawing canvas elements raised `pywintypes.com_error: (-2147352567, 'Exception occurred.')` when the COM server had not finished flushing background pagination caches.
   - *Resolution:* Indexed paragraph collections cleanly using 1-based indices and protected the inspection loop with individual exception guards.

4. **Raw Trials Dataset Validation Field Mismatch (`Exit Code 1`):**
   - *Command:* Python script checking raw trial dataset medians against aggregated CSV.
   - *Cause:* Script one-liner attempted to read dictionary key `row['elapsed_ms']`, raising `KeyError: 'elapsed_ms'`. The actual CSV column name is `latency_ms`.
   - *Resolution:* Corrected the column lookup to `row['latency_ms']`. The subsequent execution exited with **code 0**, confirming **100.0% mathematical agreement** across all 840 measurements.

**Conclusion:** None of the non-zero exit codes were caused by failures in the cryptographic implementation, operational test scenarios, or Wycheproof test-vector validations. All actual cryptographic and test suites executed with exit code 0 and 100% pass rates.
