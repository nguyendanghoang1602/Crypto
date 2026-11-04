# Google Project Wycheproof Test Vectors: RSA-PSS (Bundled Snapshot)

## Source Information
- **Repository Snapshot:** Version 0.9 snapshot of [Google Project Wycheproof](https://github.com/google/wycheproof)
- **Suite File:** `rsa_pss_2048_sha256_mgf1_32_test.json`
- **Specification Conformance:** RFC 8017 Section 8.1 / 9.1 (RSASSA-PSS / EMSA-PSS) and NIST FIPS 186-5.
- **Upstream Project Notice:** The active upstream repository maintained by C2SP contains an expanded number of test vectors; this bundled version 0.9 snapshot (108 test cases: 63 expected-valid, 45 expected-invalid) is preserved unchanged for experimental determinism and academic reproducibility.

## Test Group Parameters
- **Algorithm Type:** RSASSA-PSS
- **Key Size:** 2048 bits
- **Hash Function:** SHA-256
- **Mask Generation Function:** MGF1 (SHA-256)
- **Salt Length (`sLen`):** 32 bytes
- **Total Test Cases:** 108 (63 expected-valid accepted, 45 expected-invalid rejected)

## Validation Scope
- Evaluation against this bundled snapshot validates the cryptographic implementation against these specific 108 test vectors.
- It demonstrates practical compliance with selected edge-case test vectors, but does not claim exhaustive mathematical proof of all theoretical RFC 8017 edge cases.
