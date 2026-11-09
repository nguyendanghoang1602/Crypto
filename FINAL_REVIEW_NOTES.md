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
| **Bibliography & Metadata Verification** | Historical RSA 1977 origin attributed to RFC 8017 (2016); missing author metadata for NIST SP 800-56B Rev. 2; missing primary citations for Bellcore and original RSA paper. | Resolved all bibliographic inconsistencies: (1) Added original Rivest-Shamir-Adleman reference [1] distinguishing the April 1977 MIT memorandum (MIT/LCS/TM-82) from the February 1978 CACM publication; (2) Added Boneh et al. [7] for Bellcore CRT attack; (3) Added complete 5-author metadata for NIST SP 800-56B Rev. 2 (Elaine Barker, Lily Chen, Allen Roginsky, Apostol Vassilev, Richard Davis) [5]; (4) Accurately classified sources as primary technical standards and specifications. Complete 17-item reference list maintained in IEEE style, with references [1]–[17] consistently synchronized across the final report, source code, README, and research bibliography. | **Verified** in Section 7, `build_report_doc.py`, and `Research_Sources.md`. |
| **Prototype Security Boundaries** | Need to communicate vital prototype limitations in Section 4.3 with academic prose. | Expanded Section 4.3 to explicitly cover: (1) In-memory Python set vs. production ACID/replicated datastore (Redis/SQL) for replay prevention; (2) Basic format sanity check vs. full checksum validation (EIP-55/Bech32) and business logic (balances, limits, AML); (3) Custom deterministic JSON serialization vs. full RFC 8785 JCS compliance; (4) Pre-provisioned public keys vs. full PKI lifecycle (CRLs/OCSP/rotation); (5) Process memory private key storage vs. FIPS 140-2/3 Level 3 HSM custody. | **Verified** in Section 4.3 and README. |
| **Real-World Application Claims** | Statements assuming universal exchange practices without qualification; "key exchange" used for RSA-OAEP wrapping. | Calibrated tone: Used precise qualifications ("may employ", "can be deployed", "in some implementations", "the proposed educational architecture"). Disclaimed representation of any specific commercial exchange. Used the technically precise term **"RSA key transport"** when discussing RSA-OAEP encapsulation of symmetric keys. | **Verified** in Sections 1, 2.3, 4.0, and 6. |
| **Benchmark Interpretation** | Clarification of security levels, sample DER signature sizes, and environment specificity. | Delineated that RSA-3072 vs. ECDSA-secp256k1 represents the equivalent 128-bit classical security comparison; RSA-2048 (~112 bits) and RSA-4096 (~152 bits) are not same-strength comparisons; noted measured 71-byte ECDSA DER signature is a recorded sample (varying 70–72 B); emphasized that performance ratios are specific to the tested Python 3.15 / OpenSSL 4.0.3 environment on AMD Ryzen 5 7520U; distinguished isolated operation timings from end-to-end exchange throughput. | **Verified** in Abstract, Section 5.3, Table 2, and README. |
| **Figure & Table Accuracy** | Figure 3 caption described bar chart as "latency distributions"; secp256k1 implied as NIST-approved curve. | Updated Figure 3 caption to **"Empirical median latency comparison for RSA and ECDSA key generation, signing, and verification."** Clarified in Table 1 and Table 2 that secp256k1 uses a generic 256-bit elliptic-curve security category (~128 bits) per NIST SP 800-57 Part 1 Rev. 5, rather than being a NIST-recommended curve. | **Verified** in Figure 3 caption, Table 1, Table 2, and Section 5.3. |
| **Course Consistency & Lecture Integration** | Ensure alignment with USTH Introduction to Cryptography lecture series (Sessions 1 to 7). | Consulted all seven lecture collections as educational reference material for terminology and mathematical foundations (modular arithmetic, Euler totient, textbook RSA, DSA/Elgamal, hash properties, and PKI/TLS). Did not criticize, grade, or generate errata for lecture materials, per explicit review directives. Preserved course-level pedagogical clarity while ensuring standards compliance in the research report. | **Verified** across all report sections. |
| **RSA-OAEP Security Assumptions (ROM)** | Clarify security reduction of RSA-OAEP. | Delineated the foundational theoretical analysis of OAEP in the Random Oracle Model (ROM): Bellare & Rogaway (1994) [17] formulated OAEP and proved semantic security against chosen-plaintext attacks (IND-CPA) and plaintext awareness (implying IND-CCA1 for general trapdoor permutations); Shoup (2001) [15] demonstrated that general IND-CCA2 security cannot be proven for arbitrary permutations via standard black-box reductions from standard one-wayness, and proposed OAEP+; Fujisaki, Okamoto, Pointcheval, and Stern (2001) [16] established IND-CCA2 security specifically for RSA-OAEP under the standard RSA one-wayness assumption by introducing partial-domain one-wayness and proving its mathematical equivalence to full-domain one-wayness for the RSA permutation (with non-tight concrete reduction). Delineated RSAES-OAEP encryption primitive from RSA key transport ($mLen \le k - 2hLen - 2 = 190$ B) and hybrid encryption with AES-GCM. | **Verified** in Section 2.2 and README. |
| **RSA Key Separation (NIST FIPS 186-5)** | Prevent multi-purpose key pair reuse between digital signatures and key transport. | Added explicit mandate citing NIST FIPS 186-5 Section 5.1 and SP 800-57 Part 1 Rev. 5: an RSA key pair designated for digital signatures shall not be used for any other purpose, such as key establishment or encryption (RSA-OAEP). Architectures employing both must enforce distinct key pairs and policies. | **Verified** in Section 2.2 and README. |
| **Bellcore Fault Attack Formulations** | Present both two-signature and single-signature fault factorization equations. | Formulated two-signature case: $\gcd(s - s', n) \in \{p, q\}$ (where $s$ is correct, $s'$ is faulty, and $n = p \cdot q$). Formulated alternative single-signature case with known message representative $m = \text{OS2IP}(EM)$: $\gcd((s')^e - m, n) \in \{p, q\}$, detailing assumptions (adversary must know $m$; under randomized RSA-PSS, salt obscures $m$ externally, while internal verifiers retain full access). Clearly differentiated base blinding from post-computation verification. | **Verified** in Section 3.2, README, and `Research_Sources.md`. |
| **Public Exponent $e = 65537$ Mechanics** | Binary decomposition and operation count qualification. | Decomposed $e = 65537 = 2^{16} + 1 = 10000000000000001_2$ (17 bits, Hamming weight 2). Explained that standard binary square-and-multiply exponentiation executes in 16 squarings and 1 multiplication (17 operations total), qualifying this as an algorithmic operation count rather than an implementation-independent guarantee. | **Verified** in Section 3.2, Section 5.3, and README. |
| **Algorithm 1 EMSA-PSS Generalization** | Generalize `emBits` pseudocode. | Replaced hardcoded `emBits = 2047` with general formula $\text{emBits} = \text{modBits} - 1$. Explained why a 2048-bit modulus produces 2047 bits ($m < n$), $\text{emLen} = 256$ B, and $sLen \le \text{emLen} - hLen - 2$ ($32 \le 222$). | **Verified** in Section 4.2 and Algorithm 1. |
| **ECDSA DER Sample Wording** | Accurately reflect single sampled measurement (`len(ec_signatures[0])`). | Updated wording to: "The recorded ECDSA DER signature sample was 71 bytes, with DER-encoded signatures generally varying between 70 and 72 bytes due to variable-length ASN.1 INTEGER encoding of $r$ and $s$." Avoided claiming an average where a sample was recorded. | **Verified** in Section 5.3, Table 1, Table 2, and README. |
| **Atomic Replay Protection Boundary** | Clarify prototype vs. production concurrency boundaries. | Explicitly documented in Section 4.3 and Algorithm 1 that the prototype's in-memory Python set is an educational mechanism; production distributed deployments require strictly atomic check-and-insert logic (e.g., Redis SETNX or SQL unique constraint transactions) with TTL expiration across horizontal restarts. | **Verified** in Section 4.3, Algorithm 1, and README. |
| **TLS 1.3 Standards (RFC 9846, 9963, 10024)** | Verify official RFC publication status and metadata. | Verified RFC 9846 (published July 2026, superseding RFC 8446). Verified RFC 9963 (April 2026 legacy client auth exception) and RFC 10024 (August 2026 PQ/T hybrid key agreement). Emphasized TLS 1.3 server authentication mandates RSA-PSS. | **Verified** in Reference [3], `Research_Sources.md`, and README. |
| **Word Pagination & Layout Integrity** | Strict 5 A4 page maximum constraint; eliminate split across pages for Table 2 and Algorithm 1; disclose COM rendering engine. | Final layout parameters: Margins (1.45 cm top/bottom, 1.60 cm left/right), 9.5 pt font, 1.0 line spacing. Algorithm 1 is unified on Page 4 with `w:cantSplit` and `keep_together`. Table 1 is unified on Page 2. Table 2 is unified on Page 4. Figure 1 is on Page 2, Figure 2 is on Page 3, and Figure 3 is on Page 5. Page 5 contains empirical findings analysis, Section 6 (Conclusion), and all references (expanded to 17 references [1]–[17] in Round 5). Verified via COM automation to occupy **exactly 5 A4 pages** (Word count: 4,758 words in final release deliverable; superseded early draft measured 4,021 words, and Round 4 measured 4,747 words prior to OAEP attribution text refinement). Explicitly disclosed that Kingsoft WPS Office 12.1.0.29162 serves as the active registered COM automation provider. | **Verified** via COM automation (`ComputeStatistics(2) == 5`). |

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

### 2.4 Artifact Immutability & Reproduction Log Disclosure
- **Immutable Protected Experimental Artifacts:**
  - `03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv`: 840 individual measurements, byte-for-byte identical to baseline.
  - `03_Experimental_Data/benchmark_results.csv`: Aggregated benchmark statistics, byte-for-byte identical to baseline.
  - `05_Research_References/Wycheproof_Test_Vector/rsa_pss_2048_sha256_mgf1_32_test.json`: Google Security Research v0.9 test vector suite (108 cases), byte-for-byte identical to baseline.
  - `03_Experimental_Data/test_execution_logs/test_scenarios_and_benchmarks.log`: Full console execution transcript, byte-for-byte identical to baseline.
- **Wycheproof Reproduction Execution Log Disclosure (`wycheproof_reproduction.log`):**
  - When the verification test suite (`rsa_pss_experiment.py`) is executed to independently confirm test cases, it writes an execution log recording the run timestamp (line 4: `Timestamp: YYYY-MM-DD HH:MM:SS UTC`).
  - While all 108 PASS result lines and the final 108/108 summary remain identical, the file content changes at the byte level due to this timestamp update.
  - Consequently, `wycheproof_reproduction.log` is an actively generated reproduction log reflecting the latest verification run, distinct from the immutable benchmark datasets and official test vectors.

---

## 3. Deliverable Verification & Pagination Audit

- **Document Path:** `01_Final_Report/RSA_Real_World_Applications_Report.docx`
- **Rendered Page Count:** **Exactly 5 A4 pages** (verified via `win32com.client` `doc.ComputeStatistics(2) == 5`).
- **Word Count:** 4,758 words across 144 paragraphs in the final release deliverable (superseding the initial 4,021-word baseline draft).
- **Visual Artifacts:** 3 embedded diagrams (Figure 1 RSA-PSS workflow, Figure 2 Gateway architecture, Figure 3 Median latency comparison).
- **Structural Integrity:**
  - Page 1: Title, metadata, Abstract box, Keywords, Section 1, Section 2.1, Section 2.2.
  - Page 2: Figure 1, Section 2.3, Section 3, Table 1 (comparison matrix), Section 3.1 header.
  - Page 3: Section 3.1 body (BIP 141 SegWit calculation, EIP-198, ERC-2098), Section 3.2 (Bellcore CRT attack formula and EMSA-PSS explanation), Section 4, Section 4.1, Figure 2.
  - Page 4: Section 4.2, Algorithm 1 (boxed container with `w:cantSplit`), Section 4.3 (Prototype scope and 5 security boundaries), Section 5, 5.1, 5.2, 5.3, Table 2 (Empirical benchmark results, rows 0–4 unbroken with caption).
  - Page 5: Figure 3, Section 5.3 empirical analysis (points 1–3), Section 6 (Conclusion), Section 7 (References ending cleanly on Page 5; expanded to [1]–[17] in Round 5).
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


---

## 5. Round 3 Final Polish — Cryptographic Technical Corrections & Consistency Audit

During the final technical polishing round (November 2026), six targeted cryptographic issues and documentation alignments were addressed across the repository:

### 5.1 Summary of Targeted Corrections

1. **RFC 8017 Section 8.1 / 9.1 Signing & Verification Sequence (Issue 1):**
   - *Correction:* Replaced generalized modular expressions ($S = (EM)^d mod n$ and $EM \equiv S^e mod n$) with explicit RFC 8017 primitives:
     - **Signing:** $EM = \text{EMSA-PSS-ENCODE}(M, \text{emBits} = \text{modBits} - 1)$, $m = \text{OS2IP}(EM)$, $s = \text{RSASP1}(SK, m)$ (via private exponent $d$ or CRT parameters), $S = \text{I2OSP}(s, k)$.
     - **Verification:** $s = \text{OS2IP}(S)$, $m = \text{RSAVP1}(PK, s) = s^e mod n$, $EM = \text{I2OSP}(m, \text{emLen})$, $\text{EMSA-PSS-VERIFY}(M, EM, \text{emBits})$.
   - *Technical Rigor:* Emphasized that RSA public-key modular exponentiation ($\text{RSAVP1}$, computing $s^e mod n$) alone does **not** establish signature validity; it merely recovers the integer representative $m$. The verifier must convert $m$ to octet string $EM$ and execute `EMSA-PSS-VERIFY` to inspect `maskedDB`, unmask the randomized salt via MGF1, check padding bytes, and confirm hash consistency.
   - *Location:* Updated in Section 2.2 of `build_report_doc.py`, `README.md`, and `Research_Sources.md`.

2. **RSA-OAEP Security Reduction & Attribution (Issue 2):**
   - *Correction:* Refined the theoretical security claims for RSA-OAEP. Distinguished Bellare and Rogaway (1994, which proved IND-CCA1 security for general trapdoor permutations in ROM) from subsequent analyses by Shoup (2001) and Fujisaki, Okamoto, Pointcheval, and Stern (2001, proving IND-CCA2 security in ROM under the RSA partial-domain one-wayness assumption).
   - *Concrete Reduction:* Clarified that while theoretical IND-CCA2 security is proven in the Random Oracle Model, the concrete security reduction is not tight for practical RSA key lengths.
   - *Engineering Context:* Maintained the plaintext payload bound $mLen \le k - 2hLen - 2$ (RFC 8017 Section 7.1.1; 190 bytes for RSA-2048 with SHA-256) and deployment in hybrid key transport encapsulating ephemeral 256-bit AES-GCM symmetric keys per NIST SP 800-56B Rev. 2.
   - *Location:* Updated in Section 2.2 of `build_report_doc.py`, `README.md`, and `Research_Sources.md`.

3. **RFC 8017 Bibliographic Classification (Issue 3):**
   - *Correction:* Corrected the categorization of RFC 8017 in `Research_Sources.md` and `README.md` from `Standards Track` to `Informational` (published November 2016 as an Informational RFC by the IETF).
   - *Location:* Updated in `Research_Sources.md` [2] and `README.md`.

4. **Hardware Security Module (HSM) Deployment Language (Issue 4):**
   - *Correction:* Calibrated the private-key custody discussion in Section 4.3. Removed the blanket assertion that all production gateways require FIPS 140-2/3 Level 3 HSMs.
   - *Refined Statement:* Stated that production financial systems deploy appropriately validated HSMs or secure hardware (e.g., FIPS 140-2/3 validated HSMs, cloud HSM services, or secure enclaves) based on the organization's specific threat model, regulatory environment, and institutional key-management policies.
   - *Location:* Updated in Section 4.3 of `build_report_doc.py`, `README.md`, and `FINAL_REVIEW_NOTES.md`.

5. **Precision on TLS 1.3 Forward Secrecy & Protocol Nuances (Issue 5):**
   - *Correction:* Added precise architectural nuances to the TLS 1.3 discussion:
     - Clarified that Forward Secrecy (FS) is guaranteed by ephemeral Diffie-Hellman ((EC)DHE) and PSK-DHE (`psk_dhe_ke`).
     - Noted that PSK-only mode (`psk_ke`) does not provide Forward Secrecy against compromised pre-shared keys.
     - Noted that 0-RTT early data lacks Forward Secrecy and is vulnerable to replay attacks.
     - Noted that post-quantum forward secrecy depends on negotiating a supported hybrid mechanism (RFC 10024).
     - Reasserted that static RSA key exchange was entirely removed in TLS 1.3, restricting RSA strictly to endpoint authentication (RSA-PSS server auth per RFC 9846, legacy client auth exception per RFC 9963).
   - *Location:* Updated in Section 2.3 of `build_report_doc.py`, `README.md`, and `Research_Sources.md`.

6. **Bellcore CRT Fault Attack Formulation & RSA-PSS Salt (Issue 6):**
   - *Correction:* Refined the Bellcore CRT fault attack explanation in Section 3.2:
     - Clarified that the PSS salt is randomized, but **not a secret** (it is unmasked and checked during verification).
     - Explained that representative $m = \text{OS2IP}(EM)$ is not deterministically computable from message $M$ alone without knowing the salt, but is recovered from any valid signature via $s^e mod n$.
     - Delineated the two-signature formulation ($\gcd(s - s', n) \in \{p, q\}$) which directly factors $n$ when a valid signature $s$ is available, from the single-fault formulation ($\gcd((s')^e - m, n) \in \{p, q\}$) which requires the attacker to know $m$.
     - Reasserted that base blinding ($x' = x \cdot r^e mod n$) mitigates timing side channels, NOT CRT fault attacks. Defending against CRT fault injection requires separate countermeasures: post-computation verification or redundant fault detection.
   - *Location:* Updated in Section 3.2 of `build_report_doc.py`, `README.md`, and `Research_Sources.md`.

7. **Lecture Slide Reference Materials & Course Alignment:**
   - *Curriculum Alignment (Historical Audit Note; Superseded):* Early review audited 8 course slide collections; subsequent verification established that the official verified syllabus consists of Sessions 1 to 7 (foundational cryptographic mechanics, modular arithmetic, RSA, hash functions, digital signatures, and ECC). Sessions 1–7 form the verified core syllabus. Notation and formulas ($n = p \cdot q$, $e$, $d$, $\lambda(n)$, $\phi(n)$) were cross-checked and found fully aligned.

8. **Word Layout & Pagination Verification:**
   - *Rendering Engine:* Kingsoft WPS Office 12.1.0.29162 (active COM provider for `Word.Application`).
   - *Status:* **Exactly 5 A4 pages** (verified via `doc.ComputeStatistics(2) == 5`).
   - *Layout Integrity:* Algorithm 1 is unified on Page 4 (`w:cantSplit`, `keep_together`). Table 1 is unified on Page 2. Table 2 is unified on Page 4. Figure 1 on Page 2, Figure 2 on Page 3, and Figure 3 on Page 5. All references conclude cleanly on Page 5 (expanded to [1]–[17] in Round 5).


---

## 6. Final Correction Round — Cryptographic Technical Audit & Synchronized Release

In November 2026, an independent cryptographic audit cross-checked the repository against primary academic literature, official NIST standards, and rendering layout constraints. The following five narrowly scoped technical corrections were implemented:

### 6.1 Summary of Targeted Corrections

1. **RSA-OAEP Security Proof Historical & Theoretical Attribution:**
   - *Correction:* Delineated the three foundational milestones in the security analysis of OAEP in Section 2.2:
     - **Bellare & Rogaway (1994):** Introduced OAEP and established the original IND-CCA1 security result for general trapdoor permutations in the Random Oracle Model (ROM).
     - **Shoup (2001) [15]:** Demonstrated that the general IND-CCA2 security proof claim could not be established for arbitrary trapdoor permutations using standard black-box reductions under standard one-wayness (exposing a proof gap), and proposed the provably secure variant OAEP+.
     - **Fujisaki, Okamoto, Pointcheval, & Stern (2001) [16]:** Resolved the security of RSA-OAEP, introducing the concept of partial-domain one-wayness to prove that OAEP achieves IND-CCA2 security in the ROM when the permutation is partial-domain one-way, and demonstrating that for the specific algebraic structure of the RSA permutation, partial-domain one-wayness is mathematically equivalent to full-domain one-wayness (the standard RSA assumption), while establishing that the concrete reduction is non-tight for practical RSA parameters.
   - *Bibliography:* Added complete primary citations for Shoup (*Journal of Cryptology*, 2002 / CRYPTO 2001) [15] and Fujisaki et al. (*Journal of Cryptology*, 2004 / CRYPTO 2001) [16] in Section 7, `Research_Sources.md`, and `README.md`.

2. **Bellcore CRT Fault Attack with Randomized RSA-PSS:**
   - *Correction:* Corrected a logical omission regarding randomized salt in Section 3.2. Because RSA-PSS incorporates a randomized salt, independent signing executions on message $M$ yield differing encodings ($EM_1 \ne EM_2$) and representatives ($m_1 \ne m_2$).
   - *Formulations Delineated:*
     - **Two-Signature Formulation:** $\gcd(s - s', n) \in \{p, q\}$ strictly requires that both correct signature $s$ and faulty signature $s'$ were computed from the **exact same** encoded message representative $m = \text{OS2IP}(EM)$ (identical salt and padding). Two signatures on $M$ with differing salts do NOT satisfy this condition.
     - **Single-Fault Formulation:** $\gcd((s')^e - m, n) \in \{p, q\}$ requires knowledge of the exact representative $m$ of that specific faulty execution, which cannot be obtained merely from $M$ or a separate valid signature with a differing salt.
   - *Countermeasure Delineation:* Delineated that base blinding ($x' = x \cdot r^e \bmod n$) mitigates timing side-channel attacks, NOT CRT fault injection; defending against CRT fault injection requires post-computation signature verification or redundant dual-rail fault-detection hardware.

3. **RSA-PSS Input Notation Alignment:**
   - *Correction:* Followed RFC 8017 Section 8.1 / 9.1 notation in Section 2.2: original message octet string $M$, message digest $mHash = \text{Hash}(M)$, encoded message octet string $EM = \text{EMSA-PSS-ENCODE}(M, \text{emBits} = \text{modBits} - 1)$, integer message representative $m = \text{OS2IP}(EM)$, signature representative $s = \text{RSASP1}(SK, m)$, and signature octet string $S = \text{I2OSP}(s, k)$.
   - *Verification Sequence:* Retained $s = \text{OS2IP}(S) \to m = \text{RSAVP1}(PK, s) = s^e \bmod n \to EM = \text{I2OSP}(m, \text{emLen}) \to \text{EMSA-PSS-VERIFY}(M, EM, \text{emBits})$, emphasizing that modular exponentiation alone does not establish signature validity without EMSA-PSS decoding.

4. **FIPS 140-2 / FIPS 140-3 HSM Validation Status:**
   - *Correction:* Updated Section 4.3 and `README.md` to reflect the official NIST Cryptographic Module Validation Program (CMVP) status: all FIPS 140-2 validation certificates transitioned to the CMVP Historical List upon the standard's sunset on September 22, 2026. Production systems prefer active FIPS 140-3 validated modules for new procurements, while recognizing legacy FIPS 140-2 modules for existing systems under institutional risk management.

5. **University Lecture Session Verification:**
   - *Correction:* Strictly limited verified claims to Sessions 1–7 (the core university lecture syllabus collections inspected and verified). Removed unsupported claims of an 8th session across all documentation.

6. **Word Document Pagination & Layout Integrity:**
   - *Automation Engine:* Kingsoft WPS Office (Version 12.0, Build 12.1.0.29162; active registered COM provider for `Word.Application`).
   - *Rendered Pages:* **Exactly 5 A4 pages** (`doc.ComputeStatistics(2) == 5`).
   - *Layout Verification (Historical Draft Test Note; Superseded):* An earlier intermediate draft layout tested Table 1 on Page 1 and Table 2 on Page 2. In the verified final release deliverable, the layout map is: Table 1 (Page 2), Table 2 Benchmarks (Page 4), Algorithm 1 (Page 4, unified boxed container with `w:cantSplit`), Figure 1 (Page 2), Figure 2 (Page 3), and Figure 3 (Page 5). All 17 references [1]–[17] conclude cleanly on Page 5 with ample bottom margin clearance.

---

## 7. Round 5 Final Micro-Fix — Cryptographic Academic Audit & Harmonization

In November 2026, a final academic accuracy and documentation consistency review was performed. The following specific items were resolved and synchronized across all deliverables:

### 7.1 Summary of Targeted Corrections

1. **Bellare & Rogaway (1994) Dedicated Citation ([17]) & Theoretical Scope:**
   - *Rationale:* Section 2.2 delineates the historical progression of OAEP proofs: Bellare & Rogaway (1994), Shoup (2001), and Fujisaki et al. (2001). To ensure academic rigor and complete bibliographic traceability, a dedicated entry for Bellare & Rogaway was added as reference `[17]`.
   - *Citation Details:* M. Bellare and P. Rogaway, "Optimal Asymmetric Encryption," in *Advances in Cryptology – EUROCRYPT '94*, Lecture Notes in Computer Science, vol. 950, pp. 92–111, Springer, 1995. DOI: `10.1007/BFb0053428`.
   - *Theoretical Scope:* Accurately attributed semantic security against chosen-plaintext attacks (IND-CPA) and plaintext awareness (implying chosen-ciphertext security IND-CCA1 for general trapdoor permutations in the Random Oracle Model), avoiding any unsupported claims of general IND-CCA2 security under standard one-wayness.

2. **Shoup (2001/2002) DOI & Conference Proceedings Metadata ([15]):**
   - *Publisher-Verified DOI:* Independently audited against Springer Nature registry metadata and verified that the official DOI for Victor Shoup's *OAEP Reconsidered* in the *Journal of Cryptology* (vol. 15, no. 4, pp. 223–249, 2002) is **`10.1007/s00145-002-0133-9`** (replacing the previous unverified suffix `...0109-1`).
   - *Conference Proceedings:* Corrected the conference proceedings page range in *Advances in Cryptology – CRYPTO 2001*, Lecture Notes in Computer Science (LNCS), vol. 2139, from `pp. 133–159` to the authoritative publisher page range **`pp. 239–259`**.
   - *Full Citation:* V. Shoup, "OAEP Reconsidered," *Journal of Cryptology*, vol. 15, no. 4, pp. 223–249, Sep. 2002 (extended abstract in *Advances in Cryptology – CRYPTO 2001*, LNCS 2139, pp. 239–259, Springer). DOI: `10.1007/s00145-002-0133-9`.
   - *Theoretical Attribution:* Correctly attributed Shoup's result: demonstrated that the claimed general IND-CCA2 security proof cannot be established for arbitrary trapdoor permutations via standard black-box reductions under standard (full-domain) one-wayness, and proposed the provably secure variant OAEP+.

3. **Fujisaki et al. (2001/2004) DOI & Partial-Domain One-Wayness Attribution ([16]):**
   - *DOI Correction:* In reference [16], verified and retained the official Springer Digital Object Identifier (DOI) **`10.1007/s00145-002-0204-y`** (ending in `-y`).
   - *Full Citation:* E. Fujisaki, T. Okamoto, D. Pointcheval, and J. Stern, "RSA-OAEP is Secure under the RSA Assumption," *Journal of Cryptology*, vol. 17, no. 2, pp. 81–104, Mar. 2004 (extended abstract in *Advances in Cryptology – CRYPTO 2001*, LNCS 2139, pp. 260–274, Springer). DOI: `10.1007/s00145-002-0204-y`.
   - *Theoretical Attribution:* Correctly attributed the introduction and establishment of **partial-domain one-wayness** to Fujisaki, Okamoto, Pointcheval, and Stern (2001). They showed that OAEP is IND-CCA2 secure in the ROM if the permutation is partial-domain one-way, and proved that for the specific algebraic structure of the RSA permutation, partial-domain one-wayness is mathematically equivalent to full-domain one-wayness (the standard RSA assumption), thereby establishing IND-CCA2 security specifically for RSA-OAEP under the RSA assumption (with non-tight concrete reduction).

4. **Reference [2] (RFC 8017) Attribution Demarcation:**
   - *Scope:* Explicitly clarified that IETF RFC 8017 is an Informational document defining concrete engineering formats and encoding algorithms (such as RSAES-OAEP and RSASSA-PSS); the underlying mathematical security reductions belong to academic peer-reviewed literature, avoiding any misattribution of formal security proofs to RFC 8017 itself.

5. **Reference Count & Documentation Harmonization:**
   - *Harmonization:* Synchronized all active references to reflect exactly **17 primary references** [1]–[17] across `RSA_Real_World_Applications_Report.docx`, `02_Source_Code/build_report_doc.py`, `05_Research_References/Research_Sources.md`, `README.md`, and `FINAL_REVIEW_NOTES.md`.
   - *Lecture Course Scope:* Reaffirmed that the verified academic lecture syllabus encompasses **Sessions 1–7**. Any earlier references to an 8th session in historical draft logs are explicitly noted as superseded.

6. **Word Document Pagination & Margin Safety Verification:**
   - *Rendering Engine:* Kingsoft WPS Office (Version 12.0, Build 12.1.0.29162; active registered COM provider for `Word.Application`).
   - *Rendered Pages:* **Strictly 5 A4 pages** (`doc.ComputeStatistics(2) == 5`; word count: 4,758 words).
   - *Vertical Clearance Calculation & Measurement:* Verified via Word COM automation on A4 page geometry ($297\text{ mm} \times 210\text{ mm}$; PageHeight: 841.90 pt, TopMargin: 41.10 pt, BottomMargin: 41.10 pt / 1.45 cm). The actual printable page boundary ($PageHeight - BottomMargin$) is **800.80 pt**. The final paragraph (Reference [17]) concludes at vertical position **773.25 pt** on Page 5. The exact safety clearance to the bottom margin is $800.80\text{ pt} - 773.25\text{ pt} = \mathbf{27.55\text{ pt}}$ (and 26.75 pt when measured against the nominal 800.0 pt printable limit), providing robust vertical safety margin against cross-rasterizer overflow.

7. **Wycheproof Reproduction Execution Log Disclosure:**
   - *Status:* Documented that while the primary experimental datasets (`raw_trials_all_algorithms.csv`, `benchmark_results.csv`, `rsa_pss_2048_sha256_mgf1_32_test.json`, and `test_scenarios_and_benchmarks.log`) remain strictly immutable and byte-for-byte identical to baseline, `03_Experimental_Data/test_execution_logs/wycheproof_reproduction.log` is an actively generated reproduction log. When `rsa_pss_experiment.py` executes, it records the current execution timestamp on line 4 (`Timestamp: YYYY-MM-DD HH:MM:SS UTC`). While all 108 PASS lines and the 108/108 summary are identical, the file content changes at the byte level due to this timestamp update. The release manifest (`SHA256SUMS.txt`) correctly reflects the active hash of this reproduction run.

---

## 8. Milestone M01 — Repository Audit & Baseline Assessment

### 8.1 Repository Baseline & Project Identity
- **Working Model:** Confirmed strictly Report-First Development. The single primary deliverable is `01_Final_Report/RSA_Real_World_Applications_Report.docx` (strictly 4–5 A4 pages).
- **Supporting Evidence Role:** All code, benchmarks, logs, figures, and reference vectors serve strictly as supporting evidence for claims in the final report, not standalone product deliverables.
- **Repository Structure:** Validated 6 standard subdirectories (`01_Final_Report`, `02_Source_Code`, `03_Experimental_Data`, `04_Figures`, `05_Research_References`, `06_Environment`) and root governance files (`README.md`, `FINAL_REVIEW_NOTES.md`, `SHA256SUMS.txt`, `SPEC.md`, `TASKS.md`, `AGENTS.md`).

### 8.2 Key Identified Artifacts
- **Primary Report Deliverable:** `01_Final_Report/RSA_Real_World_Applications_Report.docx` (Word report deliverable).
- **Core Implementation & Test Suite:** `02_Source_Code/rsa_pss_experiment.py` (RSA-PSS signing/verification, canonical JSON serializer, 5 adversarial scenarios, benchmark runner, Wycheproof runner).
- **Report Compiler & Figure Generators:** `02_Source_Code/build_report_doc.py`, `02_Source_Code/generate_figures.py`.
- **Primary Benchmark Datasets:** `03_Experimental_Data/benchmark_results.csv` (aggregated stats) and `03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv` (840 raw measurements).
- **Execution & Reproduction Logs:** `03_Experimental_Data/test_execution_logs/test_scenarios_and_benchmarks.log` and `wycheproof_reproduction.log`.
- **Architectural & Benchmark Figures:** `04_Figures/benchmark_performance.png`, `rsa_pss_workflow.png`, `withdrawal_architecture.png`.
- **Authoritative References & Vectors:** `05_Research_References/Research_Sources.md` (17 synchronized references) and `05_Research_References/Wycheproof_Test_Vector/rsa_pss_2048_sha256_mgf1_32_test.json` (108 cases, v0.9 snapshot).
- **Environment Specifications:** `06_Environment/environment_info.txt`, `requirements.txt`.

### 8.3 Missing Files or Structural Anomalies
- **Missing Files:** 0 missing files. All 18 files listed in `SHA256SUMS.txt` are physically present on disk.
- **Structural Anomalies:** No unexpected files or misplaced directories found within the inspected scope.

### 8.4 Integrity Manifest Verification (`SHA256SUMS.txt`)
- **Total Manifest Entries:** 18 files.
- **Binary & Log Artifacts (6/18):** `RSA_Real_World_Applications_Report.docx`, 3 PNG figures, and 2 `.log` files match the manifest hashes byte-for-byte in raw binary mode (`MATCH_RAW`).
- **Source & Text Artifacts (12/18):** All 12 text files (`.py`, `.csv`, `.md`, `.json`, `.txt`) match 100% when evaluated with Unix LF line-endings (`MATCH_LF`). The difference in raw byte hashes is attributable to Git's automatic CRLF newline conversion on Windows checkouts. Manifest was preserved untouched.

### 8.5 Technical Risks for M02–M07
1. **Environment & Dependency Compatibility (M02):** Python 3.15.x / OpenSSL 4.x environment requirements and C-extension dependencies (`cryptography`) must be verified for reproducibility.
2. **Cryptographic Assumptions & Parameter Conflation (M03):** Ensure RSA-PSS (RSASSA-PSS, MGF1, salt length 32) is never conflated with RSA-OAEP key transport, and verify that custom JSON serialization is not erroneously claimed as full RFC 8785 JCS compliance.
3. **Application State & Replay Boundaries (M04):** The in-memory Python set for nonce deduplication must be explicitly bounded as educational, not an atomic distributed store.
4. **Adversarial & Wycheproof Test Execution (M05):** Need independent execution of the 5 adversarial scenarios and the 108 Wycheproof test cases.
5. **Empirical Benchmark Reproduction (M06):** Independent re-measurement needed to compare against the recorded 840 trials and median ratios.
6. **Figure & Reference Alignment (M07):** Ensure 17 IEEE references and figure diagrams remain 100% synchronized with the report text.

### 8.6 Limitations Unverified at M01
- Code correctness, test scenario pass rates, and benchmark latencies have NOT been independently re-run in M01 (strictly prohibited per M01 scope).
- Exact Word document page count and layout have not been re-rendered via COM in M01; they remain documented based on prior baseline notes.

---

## 9. Milestone M02 — Environment & Reproducibility Audit (Resolved via M02-R1)

### 9.1 Isolated Virtual Environment & Runtime
- **Virtual Environment Location:** Isolated local environment at `.venv/` (`c:\Users\daohi\OneDrive\Máy tính\CryptoReport\Crypto\.venv`), strictly ignored by git (`.gitignore`).
- **Active Python Executable:** `c:\Users\daohi\OneDrive\Máy tính\CryptoReport\Crypto\.venv\Scripts\python.exe` (Python 3.13.14, 64-bit AMD64).
- **Cryptographic Backend:** `cryptography==50.0.2` with native OpenSSL 4.0.3 backend (29 Sep 2026).
- **Environment Isolation:** Provisioned per Architect authorization in M02-R1 without modifying system Python or altering dependency versions in `06_Environment/requirements.txt`.

### 9.2 Dependency Verification Status
- **Declared Dependencies (`06_Environment/requirements.txt`):**
  - `cryptography==50.0.2`: Verified installed and operational in `.venv/`.
  - `cffi==2.1.1`: Verified installed as core dependency of cryptography in `.venv/`.
  - `python-docx==1.2.0`, `matplotlib==3.11.2`, `numpy==2.5.3`, `lxml==6.1.3`: Available in base environment.

### 9.3 Verification Commands & Execution Results
1. **Dependency Verification:**
   - Command: `.\.venv\Scripts\python.exe -m pip show cryptography`
   - Exit Code: `0`
   - Output: `Version: 50.0.2`, `Location: ...\.venv\Lib\site-packages`
2. **Cryptographic Import Verification:**
   - Command: `.\.venv\Scripts\python.exe -c "import cryptography, cryptography.hazmat.backends.openssl.backend as ossl; print(cryptography.__version__, ossl.openssl_version_text())"`
   - Exit Code: `0`
   - Output: `50.0.2 OpenSSL 4.0.3 29 Sep 2026`
3. **Prototype & Scenario Execution:**
   - Command: `.\.venv\Scripts\python.exe 02_Source_Code\rsa_pss_experiment.py`
   - Exit Code: `0`
   - **Wycheproof Suite:** 108/108 passed (63 expected-valid accepted, 45 expected-invalid rejected, 0 failed).
   - **Operational Scenarios:** 5/5 passed (Valid request accepted, Amount tampering rejected, Recipient tampering rejected, Rogue public key rejected, Replay attack rejected).
   - **Benchmark Preservation:** Verified datasets preserved without re-running.

### 9.4 Acceptance & Readiness for M03
- **Milestone M02 Status:** **PASS**. All environment requirements and executable prototype verification criteria have been successfully satisfied.
- **Next Milestone:** M03 (Cryptographic Implementation Audit) is queued for dedicated review.

---

## 10. Milestone M03 — RSA Cryptographic Implementation Audit

### 10.1 Verified RSA-PSS Parameters
- **Public Exponent:** $e = 65,537 = 2^{16} + 1$ ($F_4$, 17 bits, Hamming weight 2) generated via OpenSSL CSPRNG.
- **Modulus Sizes:** 2048-bit prototype key size (`rsa_pss_experiment.py:694`), with 2048, 3072, and 4096-bit evaluated in benchmarks.
- **Hash Function:** `hashes.SHA256()` ($hLen = 32$ bytes / 256 bits).
- **Mask Generation Function (MGF):** `padding.MGF1(hashes.SHA256())` per RFC 8017 Appendix B.2.1.
- **PSS Salt Length:** `salt_length = hashes.SHA256().digest_size` = 32 bytes ($sLen = hLen = 32$ bytes), strictly conforming to RFC 8017 Section 8.1 recommended default.
- **Parameter Symmetry:** `RSASigner.sign` (`rsa_pss_experiment.py:103-110`) and `RSAVerifier.verify` (`rsa_pss_experiment.py:120-128`) instantiate identical padding structures and hash algorithms.

### 10.2 Signing and Verification Behavior
- **Signed Message Octet String ($M$):** Compact canonical UTF-8 JSON bytes from `DeterministicJSONSerializer.serialize(req.to_dict())`.
- **Signing Pipeline:** Computes $mHash = \text{SHA-256}(M)$, applies $\text{EMSA-PSS-ENCODE}(M, \text{emBits} = \text{modBits} - 1)$ with 32-byte randomized salt, converts to integer representative $m = \text{OS2IP}(EM)$, computes signature representative $s = m^d \bmod n$ via $\text{RSASP1}$, and exports octets $S = \text{I2OSP}(s, k)$.
- **Verification Pipeline:** Evaluates signature octets $S$ with $s = \text{OS2IP}(S)$, recovers representative $m = s^e \bmod n$ via $\text{RSAVP1}$, decodes $EM = \text{I2OSP}(m, \text{emLen})$, and validates consistency via $\text{EMSA-PSS-VERIFY}(M, EM, \text{emBits})$ with recovered salt.
- **Error Handling:** `RSAVerifier.verify` catches `(InvalidSignature, ValueError)`. Returns `False` on bit-flips, tampering, truncated signatures, or wrong public keys. Returns `True` strictly when verification passes OpenSSL validation without raising. Verification failure cannot be mistaken for success.
- **Cryptographic Demarcation:** Strictly RSASSA-PSS digital signature verification. No RSA-OAEP encryption, decryption, or key transport is conflated.

### 10.3 Deterministic JSON Serialization: Guarantees & Boundaries
- **Guarantees:**
  - `sort_keys=True`: Guarantees lexicographical ordering of keys (`rsa_pss_experiment.py:90`).
  - `separators=(',', ':')`: Eliminates all optional whitespace, neutralizing whitespace malleability.
  - `.encode('utf-8')`: Guarantees deterministic UTF-8 byte serialization.
  - Integer Monetary Amounts: `amount_atomic_units` uses native Python integers (e.g., wei/satoshis), avoiding IEEE 754 floating-point serialization hazards.
- **Boundaries / RFC 8785 (JCS) Distinction:**
  - Emits non-ASCII characters as `\uXXXX` escape sequences due to Python's default `ensure_ascii=True` in `json.dumps`. RFC 8785 Section 3.2.2.2 mandates direct UTF-8 octet emission.
  - Does not implement ECMAScript IEEE 754 float formatting rules or UTF-16 code unit surrogate ordering (safe for the current schema as amounts are integers and keys are pure ASCII).
  - Appropriately documented in code (`rsa_pss_experiment.py:83-87`) as application-level schema determinism rather than full RFC 8785 compliance.

### 10.4 Key Handling Findings & Boundaries
- **Generation & Memory Lifecycle:** Keys generated via `rsa.generate_private_key(65537, 2048)` reside entirely in Python process memory.
- **Leakage Prevention:** Private key objects are never logged or serialized to disk; only public keys and hex-encoded signature previews are emitted.
- **Architectural Boundary:** In-memory key retention does not provide HSM custody, FIPS 140-3 boundary isolation, or memory zeroization on process termination. Documented as an educational prototype constraint.

### 10.5 Executed Audit Tests
1. **Operational Scenarios (5/5 PASS):**
   - Command: `.\.venv\Scripts\python.exe -c "..."` (Scenario 1 Valid accepted, Scenario 2 Amount tamper rejected, Scenario 3 Recipient tamper rejected, Scenario 4 Rogue key rejected, Scenario 5 Replay intercepted). Exit code: `0`.
2. **Wycheproof RSA-PSS Suite (108/108 PASS):**
   - Evaluated `rsa_pss_2048_sha256_mgf1_32_test.json`: 63 expected-valid accepted, 45 expected-invalid rejected, 0 failures. Exit code: `0`.
3. **Malleability & Corruption Test Suite (PASS):**
   - Verified that bit-flipped signatures, truncated signatures, zero-filled signatures, and empty signatures evaluate strictly to `False`.

### 10.6 Security Findings & Severity Classification
- **Critical (0):** None.
- **High (0):** None.
- **Medium (1):**
  - *Finding M03-SEC-01 (In-Memory Key Management):* `RSASigner` holds unencrypted private key instances in process memory without HSM/KMS protection or memory zeroization.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:97-110` (`RSASigner`).
    - *Impact:* Memory dump or local host compromise could expose private key.
    - *Status & Proposal:* Expected for educational research prototype. Document boundary explicitly in report Section 4.3; production would require PKCS#11 / HSM integration.
- **Low (2):**
  - *Finding M03-SEC-02 (Unicode Serialization Escape Divergence):* `DeterministicJSONSerializer` defaults to `ensure_ascii=True`, producing `\uXXXX` escape sequences for non-ASCII characters instead of raw UTF-8 octets per RFC 8785 Section 3.2.2.2.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:89-90` (`DeterministicJSONSerializer.serialize`).
    - *Impact:* Safe for current ASCII schema, but would diverge from RFC 8785 if non-ASCII strings are introduced.
    - *Status & Proposal:* Retain documentation distinction or pass `ensure_ascii=False` if RFC 8785 alignment is desired in a future revision.
  - *Finding M03-SEC-03 (Input Type Hardening in Verifier):* `RSAVerifier.verify` catches `(InvalidSignature, ValueError)`. If non-bytes are passed (e.g., `None`), a `TypeError` will bubble up.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:118-131` (`RSAVerifier.verify`).
    - *Impact:* Potential uncaught exception if untrusted caller passes non-byte arguments.
    - *Status & Proposal:* Recommend catching `(InvalidSignature, ValueError, TypeError)` or adding explicit type validation.

### 10.7 Milestone M03 Acceptance
- All cryptographic parameters, signing/verification routines, and serialization properties have been thoroughly audited and tested. No critical vulnerabilities or blockers detected.
- Milestone M03 status: **PASS**.

---

## 11. Milestone M04 — Request Validation, Timestamp & Replay Protection Audit

### 11.1 Actual End-to-End Execution Flow
1. **Request Construction:** `WithdrawalRequest` instantiated with `request_id`, `network`, `recipient_address`, `amount_atomic_units`, `nonce`, and `timestamp`.
2. **Deterministic Serialization:** `DeterministicJSONSerializer.serialize(req.to_dict())` encodes sorted keys into compact UTF-8 JSON bytes ($M$).
3. **Cryptographic Signing:** `RSASigner.sign(M)` generates a 256-byte RSA-PSS signature ($S$).
4. **Cryptographic Verification:** `RSAVerifier.verify(M, S)` verifies signature integrity against public key via OpenSSL RSASSA-PSS (`rsa_pss_experiment.py:204`).
5. **Business & Freshness Validation:** `RequestValidator.validate_request(req, current_time)` evaluates:
   - *Step 1 (Sanity):* Positive integer amount and recipient length (`>= 10`).
   - *Step 2 (Freshness):* Evaluates $|current\_time - timestamp| \le 300\text{s}$.
   - *Step 3 (Replay Check & Nonce Commit):* Checks if `nonce in seen_nonces`; if not, adds `nonce` and returns `True`.
6. **Authorization Decision:** Final acceptance requires strictly `sig_valid and app_valid` (`rsa_pss_experiment.py:206`).

### 11.2 Detailed Audit Matrix Across Categories A–D

| Category | Audit Item | Implementation Details & Behavior | Method | Status |
|---|---|---|---|---|
| **A. Request Schema & Types** | Mandatory Fields | 6 required fields: `request_id`, `network`, `recipient_address`, `amount_atomic_units`, `nonce`, `timestamp`. | Code Inspection | **Verified** |
| | Integer Atomic Amount | Amount represented as exact integer (wei/satoshis). Eliminates floating-point rounding hazards. | Code Inspection | **Verified** |
| | Boolean Subclass Hazard | `bool` subclasses `int` in Python. `amount=True` passes `<= 0` check as amount 1. | Test Execution | **Finding M04-SEC-04 (Low)** |
| | Amount Boundaries | Negative amounts (`-50`) and zero (`0`) correctly rejected. No maximum amount threshold. | Test Execution | **Verified** |
| | Nonce UUIDv4 Format | Nonce accepted as arbitrary string; no UUIDv4 regex or entropy check. | Test Execution | **Finding M04-SEC-05 (Low)** |
| | Network & Address Validation | `network` uninspected; `recipient_address` checked for `len >= 10` without chain checksums. | Test Execution | **Finding M04-SEC-06 (Low)** |
| **B. Timestamp Freshness** | Drift Window | Symmetric $|current\_time - timestamp| \le 300\text{s}$ (configurable `max_clock_skew_seconds=300`). | Code Inspection | **Verified** |
| | Exact Boundaries | $-300\text{s}$ (Pass), $-301\text{s}$ (Rejected: drift 301s > 300s); $+300\text{s}$ (Pass), $+301\text{s}$ (Rejected: drift 301s > 300s). | Test Execution | **Verified** |
| | Timestamp Unit & Drift | Integer UNIX epoch seconds. System clock skew subject to OS/NTP drift. | Code Inspection | **Verified** |
| | Signed Binding | Timestamp is bound inside serialized payload; any tampering invalidates the RSA-PSS signature. | Test Execution | **Verified** |
| **C. Replay Protection** | Replay Detection | Duplicate nonce is intercepted and rejected with `Replay detected: nonce '...' has already been processed`. | Test Execution | **Verified** |
| | Nonce Consumption Timing | Nonce recorded at Step 3 of `validate_request`. If validation precedes signature verification, invalid sig burns nonce. | Code Inspection | **Finding M04-SEC-03 (Medium)** |
| | Failed Request Nonce Retries | If timestamp check fails, nonce is not consumed; retrying with corrected timestamp succeeds. | Test Execution | **Verified** |
| | Unbounded Memory Growth | `seen_nonces` has no eviction or TTL; nonces older than 300s accumulate indefinitely in memory. | Code Inspection | **Finding M04-SEC-02 (Medium)** |
| | Multi-Process & Concurrency | In-memory `set` is process-local; cannot protect multi-worker deployments (Redis / SQL required). | Code Inspection | **Finding M04-SEC-01 (Medium)** |
| **D. Overall Workflow** | Separation of Powers | Cryptographic signature validity proves payload integrity, NOT transaction authorization or KYC/AML status. | Code Inspection | **Verified** |
| | Crash Resilience | Invalid signatures, altered payloads, and out-of-bounds timestamps return boolean flags without unhandled crashes. | Test Execution | **Verified** |

### 11.3 Security Findings & Severity Classification
- **Critical (0):** None.
- **High (0):** None.
- **Medium (3):**
  - *Finding M04-SEC-01 (Process-Local In-Memory Replay Store):* Nonces stored in Python `set()` are local to the running process and lost on restart.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:154, 171-174` (`RequestValidator`).
    - *Impact:* Horizontal scaling (multi-pod / multi-worker) allows replay across nodes.
    - *Classification:* Confirmed by code inspection & architecture analysis.
    - *Minimal Fix Proposal:* Maintain explicit documentation in Section 4.3 that production requires distributed atomic check-and-insert (e.g., Redis `SETNX` with 300s TTL).
  - *Finding M04-SEC-02 (Unbounded Nonce Cache Accumulation):* `seen_nonces` never evicts expired nonces.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:154, 174` (`RequestValidator.seen_nonces`).
    - *Impact:* Memory consumption grows linearly with transaction volume ($O(N)$ leak).
    - *Classification:* Confirmed by code inspection.
    - *Minimal Fix Proposal:* Introduce a periodic cleanup purging nonces whose associated timestamp is older than `now - max_clock_skew_seconds`, or store `(nonce, timestamp)` tuples.
  - *Finding M04-SEC-03 (Decoupled Nonce Squatting / Denial-of-Service Risk):* If `RequestValidator.validate_request` is invoked before cryptographic signature verification, an attacker submitting an invalid signature with a victim's nonce will burn the victim's nonce.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:174` (`RequestValidator.validate_request`).
    - *Impact:* Denial of service against pending transactions if an application pipeline verifies order incorrectly.
    - *Classification:* Confirmed by code inspection.
    - *Minimal Fix Proposal:* Document pipeline invariant: `RSAVerifier.verify` MUST strictly execute and return `True` prior to invoking `RequestValidator.validate_request`.
- **Low (3):**
  - *Finding M04-SEC-04 (Boolean Subclass Integer Type Bypass):* `req.amount_atomic_units <= 0` accepts `True` (evaluates to integer 1).
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:158` (`RequestValidator.validate_request`).
    - *Impact:* Minor edge-case type confusion.
    - *Classification:* Confirmed by test.
    - *Minimal Fix Proposal:* Check `if type(req.amount_atomic_units) is not int or req.amount_atomic_units <= 0:`.
  - *Finding M04-SEC-05 (Lack of UUIDv4 Nonce Entropy & Format Enforcement):* Arbitrary strings accepted as nonces.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:171` (`RequestValidator.validate_request`).
    - *Impact:* Substandard nonce entropy if client generates weak nonces.
    - *Classification:* Confirmed by test.
    - *Minimal Fix Proposal:* Validate nonce format via `uuid.UUID(req.nonce, version=4)`.
  - *Finding M04-SEC-06 (Minimal Network and Recipient Address Sanitization):* `network` field uninspected; `recipient_address` only checked for length `>= 10`.
    - *File/Location:* `02_Source_Code/rsa_pss_experiment.py:160` (`RequestValidator.validate_request`).
    - *Impact:* Unhandled malformed addresses accepted at gateway.
    - *Classification:* Confirmed by test.
    - *Minimal Fix Proposal:* Validate network whitelist (`['Ethereum', 'Bitcoin']`) and apply EIP-55 regex validation.

### 11.4 Milestone M04 Acceptance
- All audit requirements A–D verified through code inspection and dynamic testing.
- No Critical or High vulnerabilities detected. All identified limitations are consistent with the documented educational prototype scope.
- Milestone M04 status: **PASS**.

---

## 12. Milestone M05 — Adversarial Testing & Wycheproof Validation

### 12.1 Execution Summary & Test Harness Details
- **Test Script Executed:** `02_Source_Code/test_m05_adversarial.py` (Non-destructive comprehensive test harness).
- **Execution Command:** `.\.venv\Scripts\python.exe 02_Source_Code/test_m05_adversarial.py`
- **Exit Code:** `0` (Clean run; 100% assertions satisfied).
- **Scope Covered:** Cryptographic signature corruption, Wycheproof 108 test vector classification, parameter tampering, and replay/squatting/concurrency evaluation.

### 12.2 Detailed Adversarial Findings Across Categories A–D

#### A. RSA-PSS / Signature Corruption & Malleability
- **Valid Signature Verification:** 256-byte valid RSA-PSS signature verified cleanly (`True`). *(Confirmed by test)*
- **Bit-Flip Corruption:** 1-bit mutations evaluated at byte indices 0, 128, and 255; all correctly rejected (`False`) by OpenSSL verification engine. *(Confirmed by test)*
- **Structural Malformations:**
  - Empty signature (0 bytes): Rejected (`False`). *(Confirmed by test)*
  - Truncated signature (255 bytes and 128 bytes): Rejected (`False`). *(Confirmed by test)*
  - Oversized signature (257 bytes): Rejected (`False`). *(Confirmed by test)*
- **Payload & Key Mismatches:**
  - Tampered message content: Rejected (`False`). *(Confirmed by test)*
  - Rogue / Unauthorized public key: Rejected (`False`). *(Confirmed by test)*
  - Cryptographic parameter mismatch (evaluating SHA-256 signature with SHA-384 verifier): Rejected (`False`). *(Confirmed by test)*
- **Crash Resilience:** Verifier safely returns boolean `False` across all corrupted signature inputs without unexpected process crash or memory faults. *(Confirmed by test)*

#### B. Wycheproof Test Vectors Comprehensive Classification
- **Dataset Snapshot:** Version 0.9 snapshot of Google Project Wycheproof (`rsa_pss_2048_sha256_mgf1_32_test.json`).
- **Test Group Configuration:** 1 group (2048-bit modulus, SHA-256 hash, MGF1-SHA256, 32-byte salt).
- **Quantitative Vector Breakdown:**
  1. **Valid Vectors Accepted:** **63 / 63** (100.0% agreement with expected valid).
  2. **Invalid Vectors Rejected:** **45 / 45** (100.0% agreement with expected invalid).
  3. **Skipped / Unsupported Vectors:** **0 / 108** (0% skipped).
  4. **Harness / Execution Errors:** **0**.
  5. **False Positives (Invalid Signature Accepted):** **0** (Zero tolerance met).
  6. **False Negatives (Valid Signature Rejected):** **0** (Zero tolerance met).
- **Interpretation Note:** 108/108 pass indicates exact compliance with expected ground truth across 63 valid and 45 invalid vectors; it does not denote 108 valid signatures. *(Confirmed by test)*

#### C. Withdrawal Request Adversarial Cases
- **Amount Boundary & Type Validation:**
  - Negative amount (`-100`): Rejected (`False`). *(Confirmed by test)*
  - Zero amount (`0`): Rejected (`False`). *(Confirmed by test)*
  - Excessive amount ($10^{30}$ wei): Accepted by Python arbitrary-precision integer; no maximum withdrawal ceiling enforced. *(Confirmed by test)*
  - Boolean subclass bypass: `amount=True` passes validation as integer 1 (Finding M04-SEC-04 re-confirmed). `amount=False` rejected as 0. *(Confirmed by test)*
- **Recipient & Network Validation:**
  - Empty recipient address: Rejected (`False`). *(Confirmed by test)*
  - Short recipient address (`< 10` chars): Rejected (`False`). *(Confirmed by test)*
  - Unchecksummed 10-char recipient address: Accepted (`True`) due to absence of EIP-55/Bech32 validation. *(Confirmed by test)*
  - Empty or arbitrary network string: Accepted (`True`) due to absence of network whitelist. *(Confirmed by test)*
- **Timestamp Boundary Verification:**
  - Exact past boundary ($-300\text{s}$): Accepted (`True`). *(Confirmed by test)*
  - Past boundary breach ($-301\text{s}$): Rejected (`False`). *(Confirmed by test)*
  - Exact future boundary ($+300\text{s}$): Accepted (`True`). *(Confirmed by test)*
  - Future boundary breach ($+301\text{s}$): Rejected (`False`). *(Confirmed by test)*
  - Epoch zero timestamp (`1970`): Rejected (`False`). *(Confirmed by test)*
  - Milliseconds timestamp ($1.7 \times 10^{12}$): Rejected (`False`). *(Confirmed by test)*
- **Post-Signing Payload Tampering:**
  - Modifying amount, recipient, nonce, or timestamp after signing causes RSASSA-PSS signature verification to fail immediately. *(Confirmed by test)*

#### D. Replay, Nonce Squatting & Concurrency
- **Replay Mitigation:** Resubmitting an identical valid request succeeds cryptographically (`sig_valid = True`) but is intercepted by application state (`app_valid = False`, `Replay detected: nonce '...' has already been processed`). *(Confirmed by test)*
- **Nonce Squatting Hazard (Order of Operations):** If an attacker submits a victim's nonce with a malformed signature to a pipeline that invokes `validate_request` before `verify`, the nonce is committed into `seen_nonces`. Subsequent submission of the genuine signature is blocked as a replay. *(Confirmed by test & code inspection)*
- **In-Process Concurrency:** 100 concurrent threads attempting to submit the same nonce against a single `RequestValidator` instance in Python resulted in exactly 1 acceptance and 99 rejections under CPython GIL. *(Confirmed by test)*
- **Multi-Process / Distributed Concurrency:** A multi-process deployment (e.g., Gunicorn workers, microservice containers) with unshared heaps will fail to detect cross-worker replays. *(Confirmed by code inspection; NOT TESTED in a live distributed cluster)*

### 12.3 Severity & Security Finding Assessment
- **Critical Vulnerabilities:** **0**. (No invalid signature was accepted; no bypass of cryptographic verification).
- **High Vulnerabilities:** **0**.
- **Medium Findings (3 - Retained from M04):**
  - M04-SEC-01: In-memory process-local nonce set boundary.
  - M04-SEC-02: Unbounded nonce memory accumulation ($O(N)$ growth).
  - M04-SEC-03: Nonce squatting hazard if validation precedes signature verification.
- **Low Findings (3 - Retained from M04):**
  - M04-SEC-04: Boolean `True` passes as integer 1.
  - M04-SEC-05: Nonce lacks UUIDv4 format check.
  - M04-SEC-06: Minimal address and network format validation.

### 12.4 Milestone M05 Acceptance
- All 108 Wycheproof vectors evaluated and classified (63 valid accepted, 45 invalid rejected, 0 skipped, 0 errors).
- All core adversarial scenarios (corruption, tampering, replay, squatting) executed and passed.
- Prototype limits accurately documented.
- Milestone M05 status: **PASS**.

---

## 13. Milestone M06 — Benchmark Reproduction & Performance Analysis Audit

### 13.1 Benchmark Execution & Runtime Environment

- **Execution Command:**
  ```powershell
  .\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, '02_Source_Code'); from rsa_pss_experiment import run_benchmarks_and_export; res = run_benchmarks_and_export(); print('\nBENCHMARK RUN COMPLETED SUCCESSFULLY')"
  ```
- **Exit Code:** `0` (Success, no errors or warnings).
- **Execution Duration:** $\approx 8.0\text{ seconds}$ total runtime.
- **Artifacts Generated/Updated:**
  - `03_Experimental_Data/benchmark_results.csv` (Aggregated statistical metrics across 4 algorithms).
  - `03_Experimental_Data/raw_benchmark_logs/raw_trials_all_algorithms.csv` (840 individual trial latency records).
- **Environment Hardware & Runtime Profile:**
  - **Reproduction Hardware:** Intel 12th Gen Core Processor (`Intel64 Family 6 Model 154 Stepping 3`, GenuineIntel, Alder Lake performance architecture).
  - **Reproduction OS:** Microsoft Windows 11 Build 26300 (`Windows-11-10.0.26300-SP0`).
  - **Reproduction Python:** Python 3.13.14 (tags/v3.13.14:fd17997, MSC v.1944 64-bit AMD64).
  - **Cryptographic Backend:** `cryptography v50.0.2` linked to `OpenSSL 4.0.3` (29 Sep 2026).
  - **Historical Baseline Hardware (for comparison):** AMD Ryzen 5 7520U (4 Cores / 8 Threads @ 2.80 GHz, Zen 2 Mendocino microarchitecture), Windows 11 Build 26200, Python 3.15.1, OpenSSL 4.0.3.

---

### 13.2 Methodological Audit (Pre-Execution & Operational Inspection)

A rigorous inspection of `02_Source_Code/rsa_pss_experiment.py` (lines 360–602) was conducted to verify measurement methodology:

1. **Operations Benchmarked:**
   - **RSA-2048, RSA-3072, RSA-4096:** Key Generation (`keygen`, $e=65537$), RSASSA-PSS Signing (`sign`, SHA-256, MGF1-SHA256, salt=32 bytes), and RSASSA-PSS Verification (`verify`).
   - **ECDSA-secp256k1:** Key Generation (`keygen`), ECDSA Signing (`sign`, SHA-256, DER-encoded signature), and ECDSA Verification (`verify`).
2. **Measurement Counts & Warm-Up:**
   - Key generation: 10 independent trials per algorithm configuration.
   - Signing: 100 independent trials per algorithm configuration.
   - Verification: 100 independent trials per algorithm configuration (evaluating signatures generated in the signing phase).
   - **Warm-Up Phase:** Zero explicit warm-up iterations are conducted prior to the timed loop. Consequently, trial 1 in each batch captures cold cache / JIT / page load effects, visible in the maximum latency figures.
3. **Timing Isolation & Timer Precision:**
   - **Monotonic High-Resolution Timer:** Employs `time.perf_counter_ns()` with sub-microsecond resolution (~1 ns timer tick on Windows QPC).
   - **No Contamination from Keygen:** Key generation is measured in an isolated preliminary loop; a single sample key is instantiated outside the signing/verification loops.
   - **Independent Signing & Verification:** Signing and verification are strictly separated into sequential loops.
4. **Data Condition Consistency:**
   - A single, identical 219-byte canonical deterministic JSON payload is used across all RSA and ECDSA benchmarks:
     `b'{"amount_atomic_units":12500000000000000000,"network":"Ethereum","nonce":"benchmark-trial-001","recipient_address":"0x71C8fb866367bf1fE6Ba539316653551e71Cc8E3","request_id":"REQ-ETH-001","timestamp":1700000000}'`.
5. **Verification Correctness Validation:**
   - In RSA verification, `valid = verifier.verify(...)` executes within the timed block, followed immediately by `t1 = time.perf_counter_ns()`, and `assert valid` is checked post-timing to guarantee validity without skewing latency.
   - In ECDSA verification, `ec_pub.verify(...)` executes inside the timed block, which raises an `InvalidSignature` exception on invalid signatures.
6. **Outlier & Exception Handling:**
   - Zero outliers or failed trials are discarded; all 840 measurements are recorded directly into raw CSV records.
   - Median is chosen as the primary reporting metric (`statistics.median`), effectively immunizing conclusions against OS scheduling spikes.

---

### 13.3 Quantitative Reproduction & Comparative Analysis

#### A. Comprehensive Empirical Benchmark Results (Reproduction vs. Baseline)

| Algorithm | Key Size / Strength | Operation | Historical Baseline (ms) | Reproduced Median (ms) | Absolute $\Delta$ (ms) | Latency Change (%) | Reproduced Mean $\pm$ Stdev (ms) | Min / Max Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **RSA-2048** | 2048 b / 112 b | Keygen | 50.0708 | **28.9800** | -21.0908 | **-42.12%** | $31.3814 \pm 9.0561$ | 21.3453 / 52.5908 |
| | | Sign | 0.9005 | **0.4736** | -0.4269 | **-47.41%** | $0.5472 \pm 0.4660$ | 0.4377 / 5.0537 |
| | | Verify | 0.0462 | **0.0214** | -0.0248 | **-53.68%** | $0.0248 \pm 0.0146$ | 0.0204 / 0.1466 |
| **RSA-3072** | 3072 b / 128 b | Keygen | 253.9132 | **172.3547** | -81.5585 | **-32.12%** | $176.5587 \pm 80.8453$ | 64.0480 / 314.6456 |
| | | Sign | 2.7834 | **1.4849** | -1.2985 | **-46.65%** | $1.5210 \pm 0.1726$ | 1.3395 / 2.3588 |
| | | Verify | 0.0756 | **0.0392** | -0.0364 | **-48.15%** | $0.0442 \pm 0.0220$ | 0.0358 / 0.1885 |
| **RSA-4096** | 4096 b / 152 b | Keygen | 633.0616 | **359.6380** | -273.4236 | **-43.19%** | $482.8411 \pm 319.3747$ | 134.8685 / 1088.1592 |
| | | Sign | 6.5425 | **3.2927** | -3.2498 | **-49.67%** | $3.3599 \pm 0.2822$ | 3.0784 / 4.6952 |
| | | Verify | 0.1150 | **0.0581** | -0.0569 | **-49.48%** | $0.0635 \pm 0.0148$ | 0.0573 / 0.1266 |
| **ECDSA-secp256k1** | 256 b / 128 b | Keygen | 0.7158 | **0.2672** | -0.4486 | **-62.67%** | $0.6275 \pm 1.1059$ | 0.2460 / 3.7725 |
| | | Sign | 0.7196 | **0.2553** | -0.4643 | **-64.52%** | $0.2879 \pm 0.1467$ | 0.2498 / 1.6786 |
| | | Verify | 0.6214 | **0.2423** | -0.3791 | **-61.01%** | $0.2647 \pm 0.0731$ | 0.2305 / 0.7879 |

*(Note: Negative latency change indicates improved execution throughput/speed on the reproduction machine).*

#### B. Asymmetry and Comparative Operational Ratios

1. **RSA Internal Asymmetry Ratio ($\text{Sign Median} / \text{Verify Median}$):**
   - **RSA-2048:** $0.4736\text{ ms} / 0.0214\text{ ms} = \mathbf{22.13\times}$ (Baseline: $19.49\times$).
   - **RSA-3072:** $1.4849\text{ ms} / 0.0392\text{ ms} = \mathbf{37.88\times}$ (Baseline: $36.82\times$).
   - **RSA-4096:** $3.2927\text{ ms} / 0.0581\text{ ms} = \mathbf{56.67\times}$ (Baseline: $56.89\times$).
   - **ECDSA-secp256k1:** $0.2553\text{ ms} / 0.2423\text{ ms} = \mathbf{1.05\times}$ (Baseline: $1.16\times$).
   - *Analysis:* Confirms the structural asymmetry inherent in RSA with small public exponent ($e=65537$), where verification involves only 17 modular squarings/multiplications ($2^{16}+1$), whereas signing requires full private exponentiation mod $n$ via Chinese Remainder Theorem (CRT). ECDSA operations, in contrast, remain essentially symmetric ($\approx 1:1$).

2. **Cross-Algorithm Performance Ratios (Equivalent 128-bit Security: RSA-3072 vs. ECDSA-secp256k1):**
   - **Verification Advantage (RSA-3072 over ECDSA):**
     - Historical Baseline: $0.6214\text{ ms} / 0.0756\text{ ms} = \mathbf{8.22\times}$ faster.
     - Reproduced Benchmark: $0.2423\text{ ms} / 0.0392\text{ ms} = \mathbf{6.18\times}$ faster.
   - **Signing Advantage (ECDSA over RSA-3072):**
     - Historical Baseline: $2.7834\text{ ms} / 0.7196\text{ ms} = \mathbf{3.87\times}$ faster.
     - Reproduced Benchmark: $1.4849\text{ ms} / 0.2553\text{ ms} = \mathbf{5.82\times}$ faster.

3. **Analysis of Hardware Variance & Microarchitecture Divergence:**
   - **Consistent Acceleration Factor:** All operations demonstrated systematic acceleration on the reproduction platform (latencies dropped by 32% to 65%).
   - **Underlying Cause:** The reproduction host utilizes an Intel 12th Gen Alder Lake architecture (Golden Cove microarchitecture with high single-thread Instructions Per Cycle [IPC] and higher turbo boost), compared to the baseline's AMD Ryzen 5 7520U (low-power Zen 2 Mendocino cores).
   - **Differential Optimization:** OpenSSL 4.0.3 elliptic curve point multiplication (secp256k1) gained greater relative speedup (~61–65% latency reduction) than RSA bignum modular exponentiation (~47–50% reduction). Consequently, the verification advantage of RSA-3072 narrowed from $8.22\times$ to $6.18\times$, while ECDSA's signing advantage widened from $3.87\times$ to $5.82\times$.
   - **Cold-Start Jitter:** In trials without warm-up, trial 1 exhibited outlier spikes (e.g., RSA-2048 signing maximum was $5.0537\text{ ms}$ vs. median $0.4736\text{ ms}$). The median statistic effectively isolated true execution performance from OS thread scheduling anomalies.

---

### 13.4 Data Integrity & Artifact Verification

- **Mathematical Consistency:** An automated consistency audit confirmed that for all 4 algorithms and all 3 operations (12 statistical series), the median calculated directly from the 840 raw records in `raw_trials_all_algorithms.csv` matched the values recorded in `benchmark_results.csv` with 100.0% precision (`assert calc_med == rep_med`).
- **CSV Data Validation:**
  - Header schema verified: `algorithm, key_size_bits, security_strength_bits, nist_reference, keygen_median_ms, keygen_mean_ms, keygen_std_ms, keygen_min_ms, keygen_max_ms, sign_median_ms, sign_mean_ms, sign_std_ms, sign_min_ms, sign_max_ms, verify_median_ms, verify_mean_ms, verify_std_ms, verify_min_ms, verify_max_ms, signature_length_bytes, modulus_length_bytes, internal_asymmetry_ratio, trials_keygen, trials_crypto`.
  - Zero missing values, zero NaN entries, and all units unambiguously defined in milliseconds (`ms`).

---

### 13.5 Actionable Report Guidance (M08 / M09 Alignment)

1. **Contextualize Benchmark Figures:** The Word report (`01_Final_Report/`) should cite both the historical baseline (AMD Ryzen 5 7520U) and the reproduced environment (Intel 12th Gen), clarifying that while absolute latencies vary across hardware, the core architectural takeaways remain invariant:
   - RSA-PSS verification is substantially faster ($\mathbf{6.18\times - 8.22\times}$) than ECDSA-secp256k1 at equivalent 128-bit security.
   - ECDSA-secp256k1 signing is substantially faster ($\mathbf{3.87\times - 5.82\times}$) than RSA-3072 signing.
   - RSA exhibits extreme operational asymmetry ($\mathbf{37.88\times}$ for RSA-3072), making it uniquely suited for read-heavy verification tiers (e.g., central banking settlement or API gateway edge verification) but computationally costly for signer devices.
2. **Prototype Boundaries:** Explicitly document that these figures reflect single-process, CPU-bound OpenSSL 4.0.3 execution and must not be conflated with end-to-end transaction throughput involving network I/O, database persistence, or Hardware Security Modules (HSMs).

---

### 13.6 Milestone M06 Acceptance

- Benchmark reproduction executed successfully with exit code 0.
- All raw (840 records) and aggregated CSV files verified and synchronized.
- Performance variance, speed ratios, and microarchitecture divergence fully analyzed and documented.
- Milestone M06 status: **PASS**.

---

## 14. Milestone M07 — Research References & Report Figures Audit

### 14.1 Verified Academic & Normative References (22 Verified / 0 Unverified)

Every cited reference supporting the academic report (`01_Final_Report/RSA_Real_World_Applications_Report.docx`) and technical specification was independently verified against official repositories, DOIs, and standard bodies. Zero fabricated, guessed, or unverified references exist in the catalog.

| Reference ID | Title & Standard Designation | Author / Organization | Year | Official Identifier (DOI / URL) | Report Section Supported | Verification Status |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: |
| **[1]** | A Method for Obtaining Digital Signatures and Public-Key Cryptosystems | R. Rivest, A. Shamir, L. Adleman | 1978 | `https://doi.org/10.1145/359340.359342` | Sec. 1, 2.1 (Mathematical Foundations, Factoring) | **VERIFIED** |
| **[2]** | PKCS #1 v2.2: RSA Cryptography Specifications (RFC 8017) | K. Moriarty, B. Kaliski, et al. / IETF | 2016 | `https://www.rfc-editor.org/rfc/rfc8017` | Sec. 2.1, 2.2, 5.1 (Primitives, PSS, OAEP bounds) | **VERIFIED** |
| **[3]** | The Transport Layer Security (TLS) Protocol Version 1.3 (RFC 9846) | E. Rescorla / IETF | 2026 | `https://www.rfc-editor.org/rfc/rfc9846` | Sec. 1, 2.3, 4.3, 6 (TLS 1.3, PSS auth, PFS) | **VERIFIED** |
| **[4]** | Digital Signature Standard (DSS) (FIPS 186-5) | NIST | 2023 | `https://doi.org/10.6028/NIST.FIPS.186-5` | Sec. 2.2, 5.1 (PSS approval, key separation) | **VERIFIED** |
| **[5]** | Recommendation for Pair-Wise Key-Establishment Schemes (SP 800-56B Rev. 2) | E. Barker, L. Chen, et al. / NIST | 2019 | `https://doi.org/10.6028/NIST.SP.800-56Br2` | Sec. 3.1, 5.1, Tab. 1 (GNFS bits: 112, 128, 152) | **VERIFIED** |
| **[6]** | Recommendation for Key Management: Part 1 – General (SP 800-57 Pt. 1 Rev. 5) | E. Barker / NIST | 2020 | `https://doi.org/10.6028/NIST.SP.800-57pt1r5` | Sec. 3.1, Tab. 1 (Algorithm equivalence: 256b EC) | **VERIFIED** |
| **[7]** | On the Importance of Eliminating Errors in Cryptographic Computations | D. Boneh, R. DeMillo, R. Lipton | 2001 | `https://doi.org/10.1007/s001450010016` | Sec. 3.2 (Bellcore CRT fault injection attack) | **VERIFIED** |
| **[8]** | Schnorr Signatures for secp256k1 (BIP 340) | P. Wuille, J. Nick, T. Ruffing | 2020 | `https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki` | Sec. 1, 3.1, Tab. 1 (Taproot 64B Schnorr) | **VERIFIED** |
| **[9]** | Segregated Witness (Consensus Layer) (BIP 141) | E. Lombrozo, J. Lau, P. Wuille | 2015 | `https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki` | Sec. 3.1 (Weight, vSize, P2WPKH 108B stack) | **VERIFIED** |
| **[10]** | MuSig2 for BIP340-compatible Multi-Signatures (BIP 327) | J. Nick, T. Ruffing, E. Jin | 2023 | `https://github.com/bitcoin/bips/blob/master/bip-0327.mediawiki` | Sec. 3.1 (2-round threshold signature aggregation) | **VERIFIED** |
| **[11]** | Edwards-Curve Digital Signature Algorithm (EdDSA) (RFC 8032) | S. Josefsson, I. Liusvaara / IETF | 2017 | `https://www.rfc-editor.org/rfc/rfc8032` | Tab. 1 (Ed25519 32B pubkey, 64B signature) | **VERIFIED** |
| **[12]** | Bitcoin Developer Guide: Transactions | Bitcoin Core Developers | 2026 | `https://developer.bitcoin.org/devguide/transactions.html` | Sec. 3.1 (P2WPKH witness serialization) | **VERIFIED** |
| **[13]** | Ethereum Developer Documentation: Transactions and Signatures | Ethereum Foundation | 2026 | `https://ethereum.org/en/developers/docs/transactions/` | Sec. 1, 3.1 (secp256k1, RLP, EIP-198 modexp) | **VERIFIED** |
| **[14]** | Project Wycheproof: Test Vectors for Asymmetric Algorithms (v0.9) | Google Security Research | 2026 | `https://github.com/google/wycheproof` | Sec. 5.2 (108 RSA-PSS test vector reproduction) | **VERIFIED** |
| **[15]** | OAEP Reconsidered | V. Shoup | 2002 | `https://doi.org/10.1007/s00145-002-0133-9` | Sec. 2.2 (IND-CCA2 gap analysis in arbitrary trapdoors) | **VERIFIED** |
| **[16]** | RSA-OAEP is Secure under the RSA Assumption | E. Fujisaki, T. Okamoto, et al. | 2004 | `https://doi.org/10.1007/s00145-002-0204-y` | Sec. 2.2 (Partial-domain one-wayness equivalence) | **VERIFIED** |
| **[17]** | Optimal Asymmetric Encryption — How to Encrypt with RSA | M. Bellare, P. Rogaway | 1995 | `https://doi.org/10.1007/BFb0053428` | Sec. 2.2 (Original OAEP construction, IND-CPA) | **VERIFIED** |
| **[18]** | The Exact Security of Digital Signatures: How to Sign with RSA & Rabin | M. Bellare, P. Rogaway | 1996 | `https://doi.org/10.1007/3-540-68339-9_34` | Sec. 2.2 (RSA-PSS tight EUF-CMA reduction in ROM) | **VERIFIED** |
| **[19]** | Secure Hash Standard (SHS) (FIPS 180-4) | NIST | 2015 | `https://doi.org/10.6028/NIST.FIPS.180-4` | Sec. 2.2, 4.2 (SHA-256 specification, MGF1 base) | **VERIFIED** |
| **[20]** | SEC 2: Recommended Elliptic Curve Domain Parameters (v2.0) | SECG / Certicom Corp. | 2010 | `https://www.secg.org/sec2-v2.pdf` | Sec. 3.1, 5.1 (secp256k1 curve equations & domain) | **VERIFIED** |
| **[21]** | EIP-712: Typed Structured Data Hashing and Signing | R. Bloemen, L. Logvinov, J. Evans | 2017 | `https://eips.ethereum.org/EIPS/eip-712` | Sec. 4.1 (Off-chain structured message signing) | **VERIFIED** |
| **[22]** | Digital Identity Guidelines: Authentication & Lifecycle (SP 800-63B) | P. Grassi, M. Garcia, et al. / NIST | 2020 | `https://doi.org/10.6028/NIST.SP.800-63B` | Sec. 4.2, 4.3 (Nonce freshness, replay tolerance) | **VERIFIED** |

*(Total: 22 references verified against primary standards/DOI registries; 0 unverified).*

---

### 14.2 Figure Quality Assessment & Placement Strategy

All three report figures in `04_Figures/` were inspected and verified for technical accuracy, 300 DPI print legibility, and exact alignment with report sections:

1. **Figure 1: RSA-PSS Operational Workflow (`04_Figures/rsa_pss_workflow.png`)**
   - **Visual Content:** Step-by-step schematic of `EMSA-PSS-ENCODE` ($M \to \text{SHA-256}(M) \to \text{salt} \to M' \to H \to \text{maskedDB} = DB \oplus \text{MGF1}(H) \to EM$) and `RSASP1` ($S = EM^d \bmod n$), followed by verification unmasking.
   - **Recommended Placement:** Report Section 2.2 ("Digital Signatures and Provable Security: RSA-PSS vs. Legacy Schemes").
   - **Formatting Status:** Crisp, clean text boxes; fits comfortably in a standard 6.5-inch A4 margins layout without text truncation.
2. **Figure 2: Off-Chain Withdrawal Authentication Architecture (`04_Figures/withdrawal_architecture.png`)**
   - **Visual Content:** Decoupled multi-tier pipeline: Withdrawal Client (atomic units, UUIDv4 nonce, epoch timestamp) $\to$ RSA Signing Component (deterministic JSON, SHA-256, RSA-PSS) $\to$ Edge Verification Gateway (signature recovery) $\to$ Request Validation Engine (anti-replay cache, $\pm 300\text{s}$ skew check) $\to$ Blockchain Node / Hot Wallet (broadcasts native secp256k1 transactions).
   - **Recommended Placement:** Report Section 4.1 ("Decoupled Architectural Model").
   - **Formatting Status:** Distinct color-coded functional components, explicit green/red rejection flow paths, fully legible at 300 DPI.
3. **Figure 3: Empirical Performance Benchmark Comparison (`04_Figures/benchmark_performance.png`)**
   - **Visual Content:** Dual-panel graph:
     - Panel 1 (left): Key Generation Latency (Log Scale, ms) showing RSA-2048 (29.0 ms), RSA-3072 (172.4 ms), RSA-4096 (359.6 ms) vs. ECDSA-secp256k1 (0.27 ms).
     - Panel 2 (right): Signing vs. Verification Latency (ms) highlighting RSA's extreme asymmetry ($1.48\text{ ms}$ sign vs. $0.039\text{ ms}$ verify for RSA-3072) vs. ECDSA's symmetric profile ($0.26\text{ ms}$ sign vs. $0.24\text{ ms}$ verify).
   - **Recommended Placement:** Report Section 5.1 ("Empirical Latency and Asymmetry Analysis").
   - **Regeneration Note:** Regenerated via `python 02_Source_Code/generate_figures.py` to directly plot the newly reproduced M06 data.

---

### 14.3 Critical Report Claims & Cautionary Guidance for M08/M09

1. **Mandatory Use of M06 Benchmark Data:**
   - The final report must treat the M06 reproduced dataset as the primary empirical benchmark (Intel 12th Gen, Python 3.13, OpenSSL 4.0.3), documenting:
     - RSA-3072 verification median: **0.0392 ms** ($\mathbf{6.18\times}$ faster than ECDSA-secp256k1 at 0.2423 ms).
     - ECDSA-secp256k1 signing median: **0.2553 ms** ($\mathbf{5.82\times}$ faster than RSA-3072 signing at 1.4849 ms).
   - The historical AMD Ryzen 5 7520U baseline ($8.22\times$ verify ratio, $3.87\times$ sign ratio) must be presented strictly as historical comparison illustrating cross-platform microarchitecture sensitivity.
2. **Methodological Disclaimers (Pre-Condition & Harness Constraints):**
   - Disclose that the microbenchmark harness utilizes **zero warm-up iterations**, causing trial 1 to reflect cold-cache / OS thread scheduling jitter (filtered via median).
   - Emphasize that measurements evaluate raw in-process cryptographic library operations (OpenSSL 4.0.3 C-bindings via `cryptography`), excluding RPC, network round-trips, database queries, and HSM bus latency.
3. **Architectural & Security Disclaimers:**
   - Delineate Python's application-level sorted-key JSON serialization from the full RFC 8785 JSON Canonicalization Scheme (JCS).
   - Explicitly highlight Finding M04-SEC-01: the educational prototype employs an in-memory process-local nonce set that lacks distributed state synchronization and exhibits $O(N)$ memory growth.
   - Emphasize Finding M04-SEC-03: edge pipelines must verify RSA-PSS signatures *before* invoking application state validation to prevent malicious nonce squatting.

---

### 14.4 Milestone M07 Acceptance

- 22 technical references verified against official DOI and standards registries; 0 unverified.
- All 3 report figures audited, regenerated with M06 data, and mapped to specific report sections.
- Critical architectural claims and benchmark limitations synthesized for document build.
- Milestone M07 status: **PASS**.


