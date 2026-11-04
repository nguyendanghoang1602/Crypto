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
