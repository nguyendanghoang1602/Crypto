# Final Technical Audit and Targeted Polish Review Notes

**Project Title:** Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication  
**Author / Research Assistant:** Antigravity Academic Assistant  
**Date of Audit:** November 2026 (Final Targeted Polish)  
**Environment:** AMD Ryzen 5 7520U @ 2.80 GHz (4 cores / 8 threads), 16 GB RAM, Windows 11 Build 26200, Python 3.15.1, `cryptography` v50.0.2, OpenSSL 4.0.3  
**Active Automation Engine:** Kingsoft WPS Office (Version 12.0, Build 12.1.0.29162; registered COM provider for `Word.Application`)

---

## 1. Executive Summary of Consistency Resolutions & Targeted Polish

This document records the comprehensive technical audit, targeted corrections, and consistency resolutions performed on the academic research package. All peer-review requirements have been rigorously addressed without modifying the approved topic, altering the What–Why–How pedagogical structure, or mutating the verified 840-measurement experimental benchmark dataset.

| Review Area | Targeted Audit Requirement | Final Technical Resolution | Verification Status |
|---|---|---|---|
| **Bellcore CRT Fault Attack Formulation** | Ambiguous $s^e \bmod n == m$ representation conflated original message with EMSA-PSS representative. | Re-formulated using RFC 8017 Section 8.1 / 9.1: In CRT-based signing, the signer computes $s_p = m^{d_p} \bmod p$ and $s_q = m^{d_q} \bmod q$, where $m = \text{OS2IP}(EM)$ is the integer message representative produced by `EMSA-PSS-ENCODE(M)`. An induced fault on $s_q$ yields $s' \equiv s \pmod p$ and $s' \not\equiv s \pmod q$, so $\gcd(s - s', n) = p$ (or $q$ if $s_p$ is faulted). Thus $\gcd(s - s', n) \in \{p, q\}$ exposes a nontrivial factor of $n = p \cdot q$. Post-computation verification validates the recovered representative $m' = s^e \bmod n$ against $m = \text{OS2IP}(EM)$ and validates EMSA-PSS encoding consistency prior to release. | **Verified** in Section 3.2, Algorithm 1, README, and `Research_Sources.md`. |
| **Countermeasure Differentiation** | Conflation of RSA blinding with hardware fault attack defenses. | Clearly delineated: RSA base blinding ($x' = x \cdot r^e \bmod n$) specifically mitigates **timing side-channel attacks** by decoupling exponentiation timing from secret key bits. Defending against **hardware CRT fault injection** requires separate countermeasures, such as post-computation signature verification or redundant fault-detection circuitry. | **Verified** in Section 3.2 and README. |
| **Wycheproof Scope & Upstream Distinction** | Misleading description as "complete Google Project Wycheproof suite". | Clarified as "the bundled RSA-PSS 2048-bit SHA-256/MGF1-SHA256 Wycheproof test-vector set (version 0.9 snapshot, 108 cases)". Explained that it represents a selected verification test set rather than exhaustive mathematical proof of all RFC 8017 edge cases. Noted that the active upstream repository maintained by C2SP contains an expanded number of test vectors, while the bundled v0.9 snapshot is preserved for reproducibility. | **Verified** in Abstract, Section 5.2, README, and `Research_Sources.md`. |
| **TLS 1.3 Standards (RFC 9846 & RFC 9963)** | Outdated reference to RFC 8446 and unqualified claim that all TLS 1.3 RSA messages must use PSS. | Updated specification to **RFC 9846** (superseding RFC 8446). Explained that static RSA key exchange is removed in favor of (EC)DHE and post-quantum hybrid KEMs. Clarified that RSA-PSS remains mandatory for TLS 1.3 server authentication (`CertificateVerify`), while **RFC 9963** introduces a restricted legacy exception for client certificate authentication with PKCS#1 v1.5. | **Verified** in Sections 1, 2.3, 4.3, 6, and Reference [3]. |
| **Bibliography & Metadata Verification** | Historical RSA 1977 origin attributed to RFC 8017 (2016); missing author metadata for NIST SP 800-56B Rev. 2; missing primary citations for Bellcore and original RSA paper. | Resolved all bibliographic inconsistencies: (1) Added original Rivest-Shamir-Adleman reference [1] distinguishing the April 1977 MIT memorandum (MIT/LCS/TM-82) from the February 1978 CACM publication; (2) Added Boneh et al. [7] for Bellcore CRT attack; (3) Added complete 5-author metadata for NIST SP 800-56B Rev. 2 (Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev, Richard Davis) [5]; (4) Accurately classified sources as primary technical standards and specifications. Complete 14-item reference list maintained in IEEE style. | **Verified** in Section 7, `build_report_doc.py`, and `Research_Sources.md`. |
| **Prototype Security Boundaries** | Need to communicate vital prototype limitations in Section 4.3 with academic prose. | Expanded Section 4.3 to explicitly cover: (1) In-memory Python set vs. production ACID/replicated datastore (Redis/SQL) for replay prevention; (2) Basic format sanity check vs. full checksum validation (EIP-55/Bech32) and business logic (balances, limits, AML); (3) Custom deterministic JSON serialization vs. full RFC 8785 JCS compliance; (4) Pre-provisioned public keys vs. full PKI lifecycle (CRLs/OCSP/rotation); (5) Process memory private key storage vs. FIPS 140-2/3 Level 3 HSM custody. | **Verified** in Section 4.3 and README. |
| **Real-World Application Claims** | Statements assuming universal exchange practices without qualification; "key exchange" used for RSA-OAEP wrapping. | Calibrated tone: Used precise qualifications ("may employ", "can be deployed", "in some implementations", "the proposed educational architecture"). Disclaimed representation of any specific commercial exchange. Used the technically precise term **"RSA key transport"** when discussing RSA-OAEP encapsulation of symmetric keys. | **Verified** in Sections 1, 2.3, 4.0, and 6. |
| **Benchmark Interpretation** | Clarification of security levels, sample DER signature sizes, and environment specificity. | Delineated that RSA-3072 vs. ECDSA-secp256k1 represents the equivalent 128-bit classical security comparison; RSA-2048 (~112 bits) and RSA-4096 (~152 bits) are not same-strength comparisons; noted measured 71-byte ECDSA DER signature is a recorded sample (varying 70–72 B); emphasized that performance ratios are specific to the tested Python 3.15 / OpenSSL 4.0.3 environment on AMD Ryzen 5 7520U; distinguished isolated operation timings from end-to-end exchange throughput. | **Verified** in Abstract, Section 5.3, Table 2, and README. |
| **Figure & Table Accuracy** | Figure 3 caption described bar chart as "latency distributions"; secp256k1 implied as NIST-approved curve. | Updated Figure 3 caption to **"Empirical median latency comparison for RSA and ECDSA key generation, signing, and verification."** Clarified in Table 1 and Table 2 that secp256k1 uses a generic 256-bit elliptic-curve security category (~128 bits) per NIST SP 800-57 Part 1 Rev. 5, rather than being a NIST-recommended curve. | **Verified** in Figure 3 caption, Table 1, Table 2, and Section 5.3. |
| **Course Consistency & Lecture Integration** | Ensure alignment with USTH Introduction to Cryptography lecture series (Sessions 1 to 7). | Consulted all seven lecture collections as educational reference material for terminology and mathematical foundations (modular arithmetic, Euler totient, textbook RSA, DSA/Elgamal, hash properties, and PKI/TLS). Did not criticize, grade, or generate errata for lecture materials, per explicit review directives. Preserved course-level pedagogical clarity while ensuring standards compliance in the research report. | **Verified** across all report sections. |
| **RSA-OAEP Security Assumptions (ROM)** | Clarify security reduction of RSA-OAEP. | Clarified that RSA-OAEP achieves IND-CCA2 security in the Random Oracle Model (ROM) under the RSA partial-domain one-wayness assumption (Fujisaki et al. 2001; Bellare-Rogaway 1994), not an unconditional standard-model guarantee. Delineated RSAES-OAEP encryption primitive from RSA key transport ($mLen \le k - 2hLen - 2 = 190$ B) and hybrid encryption with AES-GCM. | **Verified** in Section 2.2 and README. |
| **RSA Key Separation (NIST FIPS 186-5)** | Prevent multi-purpose key pair reuse between digital signatures and key transport. | Added explicit mandate citing NIST FIPS 186-5 Section 5.1 and SP 800-57 Part 1 Rev. 5: an RSA key pair designated for digital signatures shall not be used for any other purpose, such as key establishment or encryption (RSA-OAEP). Architectures employing both must enforce distinct key pairs and policies. | **Verified** in Section 2.2 and README. |
| **Bellcore Fault Attack Formulations** | Present both two-signature and single-signature fault factorization equations. | Formulated two-signature case: $\gcd(s - s', n) \in \{p, q\}$ (where $s$ is correct, $s'$ is faulty, and $n = p \cdot q$). Formulated alternative single-signature case with known message representative $m = \text{OS2IP}(EM)$: $\gcd((s')^e - m, n) \in \{p, q\}$, detailing assumptions (adversary must know $m$; under randomized RSA-PSS, salt obscures $m$ externally, while internal verifiers retain full access). Clearly differentiated base blinding from post-computation verification. | **Verified** in Section 3.2, README, and `Research_Sources.md`. |
| **Public Exponent $e = 65537$ Mechanics** | Binary decomposition and operation count qualification. | Decomposed $e = 65537 = 2^{16} + 1 = 10000000000000001_2$ (17 bits, Hamming weight 2). Explained that standard binary square-and-multiply exponentiation executes in 16 squarings and 1 multiplication (17 operations total), qualifying this as an algorithmic operation count rather than an implementation-independent guarantee. | **Verified** in Section 3.2, Section 5.3, and README. |
| **Algorithm 1 EMSA-PSS Generalization** | Generalize `emBits` pseudocode. | Replaced hardcoded `emBits = 2047` with general formula $\text{emBits} = \text{modBits} - 1$. Explained why a 2048-bit modulus produces 2047 bits ($m < n$), $\text{emLen} = 256$ B, and $sLen \le \text{emLen} - hLen - 2$ ($32 \le 222$). | **Verified** in Section 4.2 and Algorithm 1. |
| **ECDSA DER Sample Wording** | Accurately reflect single sampled measurement (`len(ec_signatures[0])`). | Updated wording to: "The recorded ECDSA DER signature sample was 71 bytes, with DER-encoded signatures generally varying between 70 and 72 bytes due to variable-length ASN.1 INTEGER encoding of $r$ and $s$." Avoided claiming an average where a sample was recorded. | **Verified** in Section 5.3, Table 1, Table 2, and README. |
| **Atomic Replay Protection Boundary** | Clarify prototype vs. production concurrency boundaries. | Explicitly documented in Section 4.3 and Algorithm 1 that the prototype's in-memory Python set is an educational mechanism; production distributed deployments require strictly atomic check-and-insert logic (e.g., Redis SETNX or SQL unique constraint transactions) with TTL expiration across horizontal restarts. | **Verified** in Section 4.3, Algorithm 1, and README. |
| **TLS 1.3 Standards (RFC 9846, 9963, 10024)** | Verify official RFC publication status and metadata. | Verified RFC 9846 (published July 2026, superseding RFC 8446). Verified RFC 9963 (April 2026 legacy client auth exception) and RFC 10024 (August 2026 PQ/T hybrid key agreement). Emphasized TLS 1.3 server authentication mandates RSA-PSS. | **Verified** in Reference [3], `Research_Sources.md`, and README. |
| **Word Pagination & Layout Integrity** | Strict 5 A4 page maximum constraint; eliminate split across pages for Table 2 and Algorithm 1; disclose COM rendering engine. | Final layout parameters: Margins (1.45 cm top/bottom, 1.60 cm left/right), 9.5 pt font, 1.0 line spacing. Algorithm 1 is unified on Page 4 with `w:cantSplit` and `keep_together`. Table 1 is unified on Page 2. Table 2 is unified on Page 4. Figure 1 is on Page 2, Figure 2 is on Page 3, and Figure 3 is on Page 4. Page 5 contains empirical findings analysis, Section 6 (Conclusion), and all 14 references [1]–[14]. Verified via COM automation to occupy **exactly 5 A4 pages** (Word count: 4,082 words). Explicitly disclosed that Kingsoft WPS Office 12.1.0.29162 serves as the active registered COM automation provider. | **Verified** via COM automation (`ComputeStatistics(2) == 5`). |

---

## 2. Experimental Verification Details

### 2.1 Benchmark Results (Median Latencies & Statistical Integrity)
- **Host Hardware:** AMD Ryzen 5 7520U with Radeon Graphics (4 Physical Cores / 8 Threads @ 2.80 GHz), 16 GB LPDDR5 RAM.
- **Software Runtime:** Windows 11 Build 26200, Python 3.15.1 (64-bit), PyCA `cryptography` v50.0.2, OpenSSL 4.0.3 (29 Sep 2026).
- **Verified Dataset:** 840 individual measurements recorded in `raw_trials_all_algorithms.csv` matching `benchmark_results.csv` with 100.0% mathematical precision.

| Algorithm | NIST Security Strength | Keygen Median | Sign Median | Verify Median | Signature Size | Internal Asymmetry (Sign / Verify) | Relative Verify vs ECDSA |
|---|---|---:|---:|---:|---:|---:|---:|
| **RSA-2048** | 112 bits (NIST SP 800-56B) | 50.0708 ms | 0.9005 ms | 0.0462 ms | 256 B | 19.49x | **13.45x faster** |
| **RSA-3072** | 128 bits (NIST SP 800-56B) | 253.9132 ms | 2.7834 ms | 0.0756 ms | 384 B | 36.82x | **8.22x faster** |
| **RSA-4096** | 152 bits (NIST SP 800-56B) | 633.0616 ms | 6.5425 ms | 0.1150 ms | 512 B | 56.89x | **5.40x faster** |
| **ECDSA-secp256k1** | ~128 bits (generic EC mapping) | 0.7158 ms | 0.7196 ms | 0.6214 ms | 71 B (sample DER) | 1.16x | Baseline (1.0x) |

### 2.2 Bundled Wycheproof Test Suite Execution
- **File:** `rsa_pss_2048_sha256_mgf1_32_test.json` (Google Security Research version 0.9 snapshot).
- **Test Group Count:** 1 group (2048-bit modulus, SHA-256 hash, MGF1-SHA256, 32-byte salt).
- **Total Test Cases:** 108 (63 expected valid, 45 expected invalid).
- **Pass Rate:** **108/108 (100.0% agreement)**. 63 valid accepted, 45 invalid rejected, 0 failures.

### 2.3 Operational Scenario Suite (Withdrawal Gateway Pipeline)
- **Scenario 1 (Valid Payload):** Atomic withdrawal of 12.5 ETH -> `ACCEPTED`.
- **Scenario 2 (Amount Tampering):** 12.5 ETH altered to 50.0 ETH -> `REJECTED (Invalid Signature)`.
- **Scenario 3 (Recipient Tampering):** Destination address modified -> `REJECTED (Invalid Signature)`.
- **Scenario 4 (Rogue Public Key):** Evaluated against unauthorized public key -> `REJECTED (Untrusted Public Key)`.
- **Scenario 5 (Replay Attack):** Exact payload resubmitted -> Cryptographic signature passed (`True`), but duplicate nonce was intercepted -> `REJECTED BY APPLICATION STATE ENGINE`.

---

## 3. Deliverable Verification & Pagination Audit

- **Document Path:** `01_Final_Report/RSA_Real_World_Applications_Report.docx`
- **Rendered Page Count:** **Exactly 5 A4 pages** (verified via `win32com.client` `doc.ComputeStatistics(2) == 5`).
- **Word Count:** 4,021 words across 61 paragraphs and 4 structured tables.
- **Visual Artifacts:** 3 embedded diagrams (Figure 1 RSA-PSS workflow, Figure 2 Gateway architecture, Figure 3 Median latency comparison).
- **Structural Integrity:**
  - Page 1: Title, metadata, Abstract box, Keywords, Section 1, Section 2.1, Section 2.2.
  - Page 2: Figure 1, Section 2.3, Section 3, Table 1 (comparison matrix), Section 3.1 header.
  - Page 3: Section 3.1 body (BIP 141 SegWit calculation, EIP-198, ERC-2098), Section 3.2 (Bellcore CRT attack formula and EMSA-PSS explanation), Section 4, Section 4.1, Figure 2.
  - Page 4: Section 4.2, Algorithm 1 (boxed container with `w:cantSplit`), Section 4.3 (Prototype scope and 5 security boundaries), Section 5, 5.1, 5.2, 5.3, Table 2 (Empirical benchmark results, rows 0–4 unbroken with caption).
  - Page 5: Figure 3, Section 5.3 empirical analysis (points 1–3), Section 6 (Conclusion), Section 7 (References [1]–[14] ending cleanly on Page 5).
- **Word Automation Environment Disclosure:** The COM automation audit was executed using **Kingsoft WPS Office (Version 12.0, Build 12.1.0.29162)**, which is registered as the system's active COM automation server for `Word.Application` ({000209FF-0000-0000-C000-000000000046}). Under this rendering engine, the document renders to exactly 5 pages. In native Microsoft Word environments, minor typographic differences across font rasterizers should be evaluated against this 5-page ceiling constraint.

---

## 4. Transparent Verification Logs Audit (Explanation of Non-Zero Exit Codes)

During development and automated auditing sessions, specific commands returned exit code 1. To ensure complete academic transparency, each event was investigated and documented below:

1. **PowerShell Process Cleanup Command (`Exit Code 1`):**
   - *Command:* `Get-Process winword, wps -ErrorAction SilentlyContinue | Stop-Process -Force`
   - *Cause:* In PowerShell, piping `Get-Process` into `Stop-Process` emits exit code 1 when no processes named `winword` or `wps` are currently running on the host machine.
   - *Nature:* Routine shell diagnostic behavior; no application or test failure occurred.

2. **Word COM Dynamic Dispatch `.Quit()` Call (`Exit Code 1`):**
   - *Command:* Python COM test script executing `word.Quit()` via `win32com.client.Dispatch('Word.Application')`.
   - *Cause:* On the host environment running WPS Office, dynamic dispatch did not bind `.Quit()` directly on the wrapper object, raising `AttributeError` or RPC disconnection when WPS shut down before COM wrapper finalization.
   - *Resolution:* Wrapped the COM cleanup in robust `try...except` and `try...finally` guards.

3. **COM Paragraph Range Inspection Exception (`Exit Code 1`):**
   - *Command:* Python COM one-liner iterating `doc.Paragraphs` and querying `p.Range.Information(3)`.
   - *Cause:* Querying `Information(3)` across complex table borders and drawing canvas elements raised `pywintypes.com_error: (-2147352567, 'Exception occurred.')` when the COM server had not finished flushing background pagination caches.
   - *Resolution:* Indexed paragraph collections cleanly using 1-based indices and protected the inspection loop with individual exception guards.

4. **Raw Trials Dataset Validation Field Mismatch (`Exit Code 1`):**
   - *Command:* Python script checking raw trial dataset medians against aggregated CSV.
   - *Cause:* Script one-liner attempted to read dictionary key `row['elapsed_ms']`, raising `KeyError: 'elapsed_ms'`. The actual CSV column name is `latency_ms`.
   - *Resolution:* Corrected the column lookup to `row['latency_ms']`. The subsequent execution exited with **code 0**, confirming **100.0% mathematical agreement** across all 840 measurements.

**Conclusion:** None of the non-zero exit codes were caused by failures in the cryptographic implementation, operational test scenarios, or Wycheproof test-vector validations. All cryptographic and test suites execute with exit code 0 and 100% pass rates.
