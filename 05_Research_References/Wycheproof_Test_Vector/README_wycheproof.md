# Google Project Wycheproof Test Vectors: RSA-PSS

## Source Information
- **Repository:** [Google Project Wycheproof](https://github.com/google/wycheproof)
- **Official Path:** `testvectors_v1/rsa_pss_2048_sha256_mgf1_32_test.json`
- **Direct Raw URL:** `https://raw.githubusercontent.com/google/wycheproof/master/testvectors_v1/rsa_pss_2048_sha256_mgf1_32_test.json`
- **Specification Conformance:** RFC 8017 Section 8.1 / 9.1 (RSASSA-PSS / EMSA-PSS) and NIST FIPS 186-5.

## Test Group Parameters
- **Algorithm Type:** RSASSA-PSS
- **Key Size:** 2048 bits
- **Hash Function:** SHA-256
- **Mask Generation Function:** MGF1 (SHA-256)
- **Salt Length (`sLen`):** 32 bytes

## Reproduced Test Cases
1. **`tcId: 1` (Valid Signature):**
   - Message: `""` (empty byte sequence, testing zero-length hash preimage).
   - Expected Result: `"valid"`
   - Evaluation: Successfully verified with OpenSSL 4.0.3 backend in `rsa_pss_experiment.py`.
2. **Bit Perturbation Test:**
   - Perturbed the first byte of `tcId: 1` signature via XOR (`sig[0] ^= 0x01`).
   - Expected Result: `"invalid"` (`InvalidSignature` exception).
   - Evaluation: Successfully confirmed exact cryptographic rejection.

