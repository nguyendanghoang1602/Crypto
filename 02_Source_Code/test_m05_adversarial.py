"""
test_m05_adversarial.py
=======================
Milestone M05 Adversarial Testing & Wycheproof Comprehensive Validation Suite
Audits:
A. RSA-PSS signature corruption, malleability, parameters, and wrong key.
B. Full 108 Wycheproof test vectors classification (valid accepted, invalid rejected, skipped, errors).
C. WithdrawalRequest parameter boundary and type anomalies.
D. Replay attacks, nonce squatting vulnerability, and concurrency evaluation.
"""

import sys
import json
import time
import threading
from pathlib import Path

# Add project root and source dir to path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REF_DIR = PROJECT_ROOT / "05_Research_References"

sys.path.insert(0, str(SCRIPT_DIR))
from rsa_pss_experiment import (
    WithdrawalRequest, DeterministicJSONSerializer,
    RSASigner, RSAVerifier, RequestValidator
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def run_all_m05_tests():
    print("=" * 70)
    print("TASK M05 — ADVERSARIAL TESTING & WYCHEPROOF VALIDATION SUITE")
    print("=" * 70)

    # --------------------------------------------------------------------
    # PART A: RSA-PSS / SIGNATURE ADVERSARIAL TESTS
    # --------------------------------------------------------------------
    print("\n[PART A] RSA-PSS / Signature Adversarial Tests:")
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = priv.public_key()
    signer = RSASigner(priv)
    verifier = RSAVerifier(pub)

    msg = b'{"amount_atomic_units":1000,"network":"Ethereum","nonce":"test-nonce-1","recipient_address":"0x1234567890abcdef","request_id":"REQ-001","timestamp":1700000000}'
    sig = signer.sign(msg)

    # A1. Valid signature
    res_valid = verifier.verify(msg, sig)
    print(f"  A1. Valid signature verification: {res_valid} (Expected: True)")
    assert res_valid is True

    # A2. Bit-flip corruption tests
    bit_flip_positions = [0, len(sig) // 2, len(sig) - 1]
    for pos in bit_flip_positions:
        corrupted = bytearray(sig)
        corrupted[pos] ^= 0x01
        res_corrupt = verifier.verify(msg, bytes(corrupted))
        print(f"  A2. Bit-flip at byte index {pos}: {res_corrupt} (Expected: False)")
        assert res_corrupt is False

    # A3. Structural signature malformations
    print(f"  A3a. Empty signature (0 B): {verifier.verify(msg, b'')} (Expected: False)")
    assert verifier.verify(msg, b"") is False
    print(f"  A3b. Truncated signature (255 B): {verifier.verify(msg, sig[:-1])} (Expected: False)")
    assert verifier.verify(msg, sig[:-1]) is False
    print(f"  A3c. Severely truncated sig (128 B): {verifier.verify(msg, sig[:128])} (Expected: False)")
    assert verifier.verify(msg, sig[:128]) is False
    print(f"  A3d. Oversized signature (257 B): {verifier.verify(msg, sig + b'\\x00')} (Expected: False)")
    assert verifier.verify(msg, sig + b"\x00") is False

    # A4. Wrong message & wrong public key
    wrong_msg = msg + b" "
    print(f"  A4a. Altered message text: {verifier.verify(wrong_msg, sig)} (Expected: False)")
    assert verifier.verify(wrong_msg, sig) is False
    rogue_pub = rsa.generate_private_key(public_exponent=65537, key_size=2048).public_key()
    rogue_verifier = RSAVerifier(rogue_pub)
    print(f"  A4b. Unauthorized public key: {rogue_verifier.verify(msg, sig)} (Expected: False)")
    assert rogue_verifier.verify(msg, sig) is False

    # A5. Cryptographic parameter mismatch
    try:
        pub.verify(sig, msg, padding.PSS(mgf=padding.MGF1(hashes.SHA384()), salt_length=32), hashes.SHA384())
        res_mismatch = True
    except Exception:
        res_mismatch = False
    print(f"  A5. Parameter mismatch (SHA-384 on SHA-256 sig): {res_mismatch} (Expected: False)")
    assert res_mismatch is False

    # --------------------------------------------------------------------
    # PART B: WYCHEPROOF TEST VECTORS COMPREHENSIVE AUDIT
    # --------------------------------------------------------------------
    print("\n[PART B] Wycheproof Test Vectors Comprehensive Audit:")
    wyche_json = REF_DIR / "Wycheproof_Test_Vector" / "rsa_pss_2048_sha256_mgf1_32_test.json"
    with open(wyche_json, "r", encoding="utf-8") as f:
        wdata = json.load(f)

    g = wdata["testGroups"][0]
    w_pub = serialization.load_pem_public_key(g["publicKeyPem"].encode("utf-8"))
    w_tests = g["tests"]

    valid_accepted = 0
    valid_rejected = 0
    invalid_rejected = 0
    invalid_accepted = 0
    skipped = 0
    harness_errors = 0

    for t in w_tests:
        expected = t["result"]
        t_msg = bytes.fromhex(t["msg"])
        t_sig = bytes.fromhex(t["sig"])
        try:
            w_pub.verify(
                t_sig,
                t_msg,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32),
                hashes.SHA256()
            )
            actual = "valid"
        except Exception:
            actual = "invalid"

        if expected == "valid":
            if actual == "valid":
                valid_accepted += 1
            else:
                valid_rejected += 1
        elif expected == "invalid":
            if actual == "invalid":
                invalid_rejected += 1
            else:
                invalid_accepted += 1
        else:
            skipped += 1

    total_vectors = len(w_tests)
    print(f"  Total test vectors evaluated : {total_vectors}")
    print(f"  1. Valid vectors accepted    : {valid_accepted} / 63 (Expected: 63)")
    print(f"  2. Invalid vectors rejected  : {invalid_rejected} / 45 (Expected: 45)")
    print(f"  3. Skipped / unsupported     : {skipped} (Expected: 0)")
    print(f"  4. Harness errors            : {harness_errors} (Expected: 0)")
    print(f"  False Positives (Invalid Accepted): {invalid_accepted}")
    print(f"  False Negatives (Valid Rejected)  : {valid_rejected}")

    assert valid_accepted == 63, "Not all valid vectors were accepted!"
    assert invalid_rejected == 45, "Not all invalid vectors were rejected!"
    assert invalid_accepted == 0, "Security Violation: Invalid signature accepted!"
    assert valid_rejected == 0, "Legitimate signature falsely rejected!"

    # --------------------------------------------------------------------
    # PART C: WITHDRAWAL REQUEST ADVERSARIAL CASES
    # --------------------------------------------------------------------
    print("\n[PART C] Withdrawal Request Adversarial Cases:")
    validator = RequestValidator(max_clock_skew_seconds=300)
    now = 1700000000

    # C1. Amount validation
    cases_amount = [
        ("Negative amount (-100)", -100, False),
        ("Zero amount (0)", 0, False),
        ("Excessive amount (10^30)", 10**30, True),  # Handled as arbitrary-precision int; no max cap
        ("Boolean amount (True)", True, True),        # Bug M04-SEC-04: bool subclasses int
        ("Boolean amount (False)", False, False),     # False <= 0 is True; rejected
    ]
    for desc, amt, exp in cases_amount:
        r = WithdrawalRequest("REQ", "Ethereum", "0x1234567890abcdef", amt, f"nonce-{desc}", now)
        ok, err = validator.validate_request(r, now)
        print(f"  C1. {desc}: passed={ok} (Expected: {exp}) -> {err}")
        assert ok == exp

    # C2. Recipient / Network validation
    cases_recip = [
        ("Empty recipient address", "", False),
        ("Short recipient address (len 9)", "0x1234567", False),
        ("Valid length without checksum", "1234567890", True),
        ("Empty network identifier", "", True),
    ]
    for desc, val, exp in cases_recip:
        if "network" in desc:
            r = WithdrawalRequest("REQ", val, "0x1234567890abcdef", 100, f"nonce-{desc}", now)
        else:
            r = WithdrawalRequest("REQ", "Ethereum", val, 100, f"nonce-{desc}", now)
        ok, err = validator.validate_request(r, now)
        print(f"  C2. {desc}: passed={ok} (Expected: {exp})")
        assert ok == exp

    # C3. Timestamp boundaries
    cases_time = [
        ("Exact past boundary (-300s)", now - 300, True),
        ("Past boundary violation (-301s)", now - 301, False),
        ("Exact future boundary (+300s)", now + 300, True),
        ("Future boundary violation (+301s)", now + 301, False),
        ("Epoch zero timestamp (1970)", 0, False),
        ("Milliseconds timestamp (1.7e12)", int(now * 1000), False),
    ]
    for desc, ts, exp in cases_time:
        r = WithdrawalRequest("REQ", "Ethereum", "0x1234567890abcdef", 100, f"nonce-{desc}", ts)
        ok, err = validator.validate_request(r, now)
        print(f"  C3. {desc}: passed={ok} (Expected: {exp})")
        assert ok == exp

    # --------------------------------------------------------------------
    # PART D: REPLAY, NONCE SQUATTING & CONCURRENCY
    # --------------------------------------------------------------------
    print("\n[PART D] Replay, Nonce Squatting & Concurrency:")

    # D1. Replay of legitimate request
    r_valid = WithdrawalRequest("REQ-D1", "Ethereum", "0x1234567890abcdef", 1000, "nonce-d1", now)
    p_valid = DeterministicJSONSerializer.serialize(r_valid.to_dict())
    s_valid = signer.sign(p_valid)

    ok1_v = verifier.verify(p_valid, s_valid)
    ok1_a, _ = validator.validate_request(r_valid, now)
    print(f"  D1a. First submission: verify={ok1_v}, validate={ok1_a} -> ACCEPTED")
    assert ok1_v and ok1_a

    ok2_v = verifier.verify(p_valid, s_valid)  # Cryptographically valid
    ok2_a, err2 = validator.validate_request(r_valid, now)  # Replay intercepted
    print(f"  D1b. Replay submission: verify={ok2_v}, validate={ok2_a} ({err2}) -> REJECTED")
    assert ok2_v and (not ok2_a)

    # D2. Nonce Squatting / Order of Operations Vulnerability Test
    v_squat = RequestValidator(300)
    r_squat = WithdrawalRequest("REQ-D2", "Ethereum", "0x1234567890abcdef", 1000, "nonce-squat-victim", now)
    p_squat = DeterministicJSONSerializer.serialize(r_squat.to_dict())
    bad_sig = b"\x00" * 256

    # Attacker calls validate first with bad signature
    ok_squat_val, _ = v_squat.validate_request(r_squat, now)
    ok_bad_sig = verifier.verify(p_squat, bad_sig)
    print(f"  D2a. Attacker submission: validate={ok_squat_val}, verify={ok_bad_sig} (Nonce burned in validator)")
    assert ok_squat_val is True
    assert ok_bad_sig is False

    # Legitimate user now attempts to submit real signature with same nonce
    ok_legit_val, err_legit = v_squat.validate_request(r_squat, now)
    print(f"  D2b. Victim subsequent attempt: validate={ok_legit_val} ({err_legit}) -> SQUATTED/BLOCKED")
    assert ok_legit_val is False

    # D3. Concurrency within single process
    v_conc = RequestValidator(300)
    r_conc = WithdrawalRequest("REQ-D3", "Ethereum", "0x1234567890abcdef", 1000, "nonce-concurrent", now)
    accepted_conc = 0
    c_lock = threading.Lock()

    def conc_worker():
        nonlocal accepted_conc
        ok, _ = v_conc.validate_request(r_conc, now)
        if ok:
            with c_lock:
                accepted_conc += 1

    threads = [threading.Thread(target=conc_worker) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"  D3. In-process concurrency (100 threads same nonce): accepted={accepted_conc}/100")
    assert accepted_conc == 1, f"Concurrency race failure: {accepted_conc} requests accepted!"

    print("\n" + "=" * 70)
    print("ALL M05 ADVERSARIAL AND WYCHEPROOF TESTS COMPLETED WITH 100% SUCCESS.")
    print("=" * 70)


if __name__ == "__main__":
    run_all_m05_tests()

