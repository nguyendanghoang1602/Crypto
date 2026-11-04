"""
rsa_pss_experiment.py
=====================
Academic Research Implementation & Empirical Evaluation:
Real-World Applications of RSA - Digital Signature Scheme (RSA-PSS)
for Off-Chain Cryptocurrency Withdrawal Authentication.

This script executes:
1. Validation against bundled Wycheproof test set (version 0.9 snapshot, 108 cases; RSA-PSS 2048-bit, SHA-256).
2. Off-chain withdrawal request pipeline using atomic integer monetary units and deterministic serialization.
3. Five security and tampering verification test scenarios.
4. Independent empirical benchmarks for RSA (2048, 3072, 4096) and ECDSA (secp256k1).
5. Synchronous export of both raw per-trial measurements and aggregated benchmark metrics.
"""

import sys
import os
import json
import time
import platform
import csv
import statistics
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Tuple, Set, List

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.exceptions import InvalidSignature
import cryptography.hazmat.backends.openssl.backend as ossl_backend


# =====================================================================
# PATH RESOLUTION (STABLE PROJECT-RELATIVE PATHS)
# =====================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "03_Experimental_Data"
LOG_DIR = DATA_DIR / "test_execution_logs"
RAW_DIR = DATA_DIR / "raw_benchmark_logs"
FIG_DIR = PROJECT_ROOT / "04_Figures"
REF_DIR = PROJECT_ROOT / "05_Research_References"

for d in (DATA_DIR, LOG_DIR, RAW_DIR, FIG_DIR):
    d.mkdir(parents=True, exist_ok=True)


# =====================================================================
# 1. MODELS AND DETERMINISTIC SERIALIZATION
# =====================================================================

@dataclass
class WithdrawalRequest:
    """
    Data model for an off-chain cryptocurrency withdrawal request.
    Monetary amount is represented as an integer in atomic units (e.g., wei for
    Ethereum or satoshis for Bitcoin) to avoid floating-point representation hazards.
    """
    request_id: str
    network: str
    recipient_address: str
    amount_atomic_units: int  # Exact integer atomic units (e.g., 12.5 ETH = 12500000000000000000 wei)
    nonce: str
    timestamp: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "amount_atomic_units": self.amount_atomic_units,
            "network": self.network,
            "nonce": self.nonce,
            "recipient_address": self.recipient_address,
            "request_id": self.request_id,
            "timestamp": self.timestamp
        }


class DeterministicJSONSerializer:
    """
    Enforces deterministic JSON serialization for consistent cryptographic hashing.
    Sorts dictionary keys lexicographically, removes non-essential whitespace,
    and encodes to UTF-8.
    
    Technical Note: While inspired by canonical JSON principles, this serializer
    does not claim full IETF RFC 8785 compliance (which mandates strict ECMAScript
    number formatting rules, UTF-16 code unit ordering, and I-JSON constraints).
    It provides application-level deterministic serialization for the defined schema.
    """
    @staticmethod
    def serialize(payload: Dict[str, Any]) -> bytes:
        return json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')


# =====================================================================
# 2. CRYPTOGRAPHIC SIGNING & VERIFICATION ENGINE (RSA-PSS)
# =====================================================================

class RSASigner:
    """Signs payloads using RSA-PSS with SHA-256 and MGF1."""
    def __init__(self, private_key: rsa.RSAPrivateKey):
        self.private_key = private_key

    def sign(self, data: bytes) -> bytes:
        return self.private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=hashes.SHA256().digest_size  # 32-byte salt
            ),
            hashes.SHA256()
        )


class RSAVerifier:
    """Verifies RSA-PSS signatures against an authentic public key."""
    def __init__(self, public_key: rsa.RSAPublicKey):
        self.public_key = public_key

    def verify(self, data: bytes, signature: bytes) -> bool:
        try:
            self.public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=hashes.SHA256().digest_size
                ),
                hashes.SHA256()
            )
            return True
        except (InvalidSignature, ValueError):
            return False


# =====================================================================
# 3. REQUEST VALIDATION COMPONENT (EDUCATIONAL PROTOTYPE)
# =====================================================================

class RequestValidator:
    """
    Evaluates business rules, timestamp freshness, and nonce uniqueness.
    
    Architectural Clarification:
    - This prototype utilizes an in-memory Python set for nonce tracking.
      A production cryptocurrency exchange requires a persistent, atomic,
      and distributed cache (e.g., Redis or an ACID-compliant SQL store).
    - Address validation here performs prototype-level structure and length checks;
      production gateways require full chain-specific validation (e.g., EIP-55, Bech32).
    - Account balance verification is omitted as it belongs to an external ledger service.
    - RSA digital signatures guarantee authenticity and data integrity, but CANNOT
      prevent replay attacks on their own. Stateful tracking is strictly required.
    """
    def __init__(self, max_clock_skew_seconds: int = 300):
        self.max_clock_skew_seconds = max_clock_skew_seconds
        self.seen_nonces: Set[str] = set()

    def validate_request(self, req: WithdrawalRequest, current_time: int) -> Tuple[bool, str]:
        # 1. Parameter sanity checks
        if req.amount_atomic_units <= 0:
            return False, f"Invalid withdrawal amount: {req.amount_atomic_units}"
        if not req.recipient_address or len(req.recipient_address) < 10:
            return False, "Invalid recipient address format (prototype check)"

        # 2. Timestamp freshness (defense against delayed injection)
        time_diff = abs(current_time - req.timestamp)
        if time_diff > self.max_clock_skew_seconds:
            return False, f"Timestamp out of bounds (drift: {time_diff}s > {self.max_clock_skew_seconds}s)"

        # 3. Nonce uniqueness (in-memory anti-replay check)
        # Note: Educational in-memory store; production deployments require strictly atomic check-and-insert
        # (e.g., Redis SETNX or SQL unique constraint transaction) across distributed nodes.
        if req.nonce in self.seen_nonces:
            return False, f"Replay detected: nonce '{req.nonce}' has already been processed"

        self.seen_nonces.add(req.nonce)
        return True, "Request parameters and nonce valid"


# =====================================================================
# 4. FIVE SYSTEM OPERATIONAL SCENARIOS
# =====================================================================

def run_scenarios(private_key: rsa.RSAPrivateKey, public_key: rsa.RSAPublicKey) -> bool:
    print("\n" + "="*75)
    print("RUNNING PRACTICAL SYSTEM SCENARIOS (OFF-CHAIN WITHDRAWAL AUTH)")
    print("="*75)

    signer = RSASigner(private_key)
    verifier = RSAVerifier(public_key)
    validator = RequestValidator(max_clock_skew_seconds=300)

    now = int(time.time())

    # Scenario 1: Valid withdrawal request (12.5 ETH = 12,500,000,000,000,000,000 wei)
    req1 = WithdrawalRequest(
        request_id="REQ-ETH-20261104-001",
        network="Ethereum",
        recipient_address="0x71C8fb866367bf1fE6Ba539316653551e71Cc8E3",
        amount_atomic_units=12_500_000_000_000_000_000,
        nonce="a8f9c10e-8215-4c07-b649-1d2e3f4a5b6c",
        timestamp=now
    )
    payload1 = DeterministicJSONSerializer.serialize(req1.to_dict())
    sig1 = signer.sign(payload1)
    sig_valid1 = verifier.verify(payload1, sig1)
    app_valid1, msg1 = validator.validate_request(req1, current_time=now)
    passed1 = sig_valid1 and app_valid1

    print(f"\n[Scenario 1] Valid Request Acceptance:")
    print(f"  - Payload: {payload1.decode()}")
    print(f"  - Signature Preview: {sig1.hex()[:32]}... ({len(sig1)} bytes)")
    print(f"  - Cryptographic Verification: {sig_valid1}")
    print(f"  - Application Validation: {app_valid1} ({msg1})")
    print(f"  - Final Decision: {'ACCEPTED' if passed1 else 'REJECTED'}")
    assert passed1, "Scenario 1 failed"

    # Scenario 2: Tampered withdrawal amount (50.0 ETH instead of 12.5 ETH)
    req2_dict = req1.to_dict()
    req2_dict["amount_atomic_units"] = 50_000_000_000_000_000_000
    payload2_tampered = DeterministicJSONSerializer.serialize(req2_dict)
    sig_valid2 = verifier.verify(payload2_tampered, sig1)
    passed2 = (sig_valid2 is False)

    print(f"\n[Scenario 2] Tampered Amount Detection (12.5 ETH -> 50.0 ETH):")
    print(f"  - Signature on Tampered Payload Verified: {sig_valid2}")
    print(f"  - Final Decision: {'REJECTED (Integrity Violation Detected)' if not sig_valid2 else 'FAILED'}")
    assert passed2, "Scenario 2 failed"

    # Scenario 3: Tampered recipient address
    req3_dict = req1.to_dict()
    req3_dict["recipient_address"] = "0xAttackerControlledAddress00000000000000"
    payload3_tampered = DeterministicJSONSerializer.serialize(req3_dict)
    sig_valid3 = verifier.verify(payload3_tampered, sig1)
    passed3 = (sig_valid3 is False)

    print(f"\n[Scenario 3] Tampered Recipient Address Detection:")
    print(f"  - Signature on Tampered Recipient Verified: {sig_valid3}")
    print(f"  - Final Decision: {'REJECTED (Recipient Spoof Detected)' if not sig_valid3 else 'FAILED'}")
    assert passed3, "Scenario 3 failed"

    # Scenario 4: Incorrect / rogue public key
    rogue_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rogue_verifier = RSAVerifier(rogue_priv.public_key())
    sig_valid4 = rogue_verifier.verify(payload1, sig1)
    passed4 = (sig_valid4 is False)

    print(f"\n[Scenario 4] Rogue / Incorrect Public Key Verification:")
    print(f"  - Signature Verified against Rogue Public Key: {sig_valid4}")
    print(f"  - Final Decision: {'REJECTED (Untrusted Public Key)' if not sig_valid4 else 'FAILED'}")
    assert passed4, "Scenario 4 failed"

    # Scenario 5: Replay attack (valid signature submitted a second time)
    sig_valid5 = verifier.verify(payload1, sig1)  # Cryptographically still valid
    app_valid5, msg5 = validator.validate_request(req1, current_time=now + 5)
    passed5 = sig_valid5 and (not app_valid5)

    print(f"\n[Scenario 5] Replay Attack Mitigation:")
    print(f"  - Replayed Signature Verification: {sig_valid5} (RSA-PSS signature remains mathematically valid)")
    print(f"  - Application Validation: {app_valid5} ({msg5})")
    print(f"  - Final Decision: {'REJECTED BY APPLICATION STATE ENGINE' if not app_valid5 else 'FAILED'}")
    assert passed5, "Scenario 5 failed"

    print("\n>>> All 5 operational scenarios executed and passed successfully.")
    return True


# =====================================================================
# 5. BUNDLED WYCHEPROOF VALIDATION (VERSION 0.9 SNAPSHOT, 108 CASES)
# =====================================================================

def run_wycheproof_suite(json_path: Path) -> Dict[str, Any]:
    print("\n" + "="*75)
    print("RUNNING BUNDLED WYCHEPROOF TEST SET (VERSION 0.9 SNAPSHOT, 108 CASES)")
    print(f"Suite: {json_path.name}")
    print("="*75)

    if not json_path.exists():
        raise FileNotFoundError(f"Wycheproof test file not found at: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    g = data["testGroups"][0]
    pub_key = serialization.load_pem_public_key(g["publicKeyPem"].encode("utf-8"))

    total = len(g["tests"])
    passed = 0
    failed = 0
    valid_cases = 0
    invalid_cases = 0

    log_entries = []
    log_entries.append("BUNDLED WYCHEPROOF RSA-PSS VALIDATION EXECUTION LOG (VERSION 0.9 SNAPSHOT)")
    log_entries.append(f"Suite File: {json_path.name}")
    log_entries.append(f"Algorithm: RSASSA-PSS | Modulus: 2048 bits | Hash: SHA-256 | Salt Length: 32 bytes")
    log_entries.append(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n")

    for t in g["tests"]:
        tcid = t["tcId"]
        comment = t["comment"]
        msg = bytes.fromhex(t["msg"])
        sig = bytes.fromhex(t["sig"])
        expected = t["result"]

        if expected == "valid":
            valid_cases += 1
        elif expected == "invalid":
            invalid_cases += 1

        try:
            pub_key.verify(
                sig,
                msg,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=32
                ),
                hashes.SHA256()
            )
            actual = "valid"
        except (InvalidSignature, ValueError):
            actual = "invalid"

        if actual == expected:
            passed += 1
            log_entries.append(f"[PASS] tcId {tcid:3d}: expected '{expected}', got '{actual}' ({comment})")
        else:
            failed += 1
            log_entries.append(f"[FAIL] tcId {tcid:3d}: expected '{expected}', got '{actual}' ({comment})")

    summary_str = (
        f"Wycheproof Test Suite Results: {passed}/{total} passed "
        f"({valid_cases} expected-valid cases accepted, {invalid_cases} expected-invalid cases rejected, {failed} failed)."
    )
    print("  " + summary_str)
    print("  Note: Validating against this suite confirms compliance with these specific 108 test vectors,")
    print("  without claiming exhaustive mathematical proof of all possible RFC 8017 edge cases.")

    log_entries.append(f"\nSUMMARY: {summary_str}")

    # Write log file
    log_file = LOG_DIR / "wycheproof_reproduction.log"
    with open(log_file, "w", encoding="utf-8") as lf:
        lf.write("\n".join(log_entries) + "\n")
    print(f"  [+] Wycheproof execution log written to: {log_file}")

    assert failed == 0, f"Wycheproof suite encountered {failed} failures!"
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "valid_cases": valid_cases,
        "invalid_cases": invalid_cases
    }


# =====================================================================
# 6. UNIFIED EMPIRICAL BENCHMARKS & RAW MEASUREMENTS EXPORT
# =====================================================================

def run_benchmarks_and_export(
    rsa_key_sizes=(2048, 3072, 4096),
    keygen_trials=10,
    crypto_trials=100
) -> Dict[str, Any]:
    print("\n" + "="*75)
    print("RUNNING EMPIRICAL PERFORMANCE BENCHMARKS (RSA vs. ECDSA secp256k1)")
    print(f"RSA Moduli: {rsa_key_sizes} bits | Keygen trials: {keygen_trials} | Sign/Verify trials: {crypto_trials}")
    print("="*75)

    test_payload = b'{"amount_atomic_units":12500000000000000000,"network":"Ethereum","nonce":"benchmark-trial-001","recipient_address":"0x71C8fb866367bf1fE6Ba539316653551e71Cc8E3","request_id":"REQ-ETH-001","timestamp":1700000000}'

    raw_measurements: List[Dict[str, Any]] = []
    aggregated_results: List[Dict[str, Any]] = []
    sample_rsa_key = None

    # --- A. BENCHMARK RSA CONFIGURATIONS ---
    for size in rsa_key_sizes:
        print(f"\nEvaluating RSA-{size} ...")

        # 1. Key Generation
        keygen_times: List[float] = []
        sample_key = None
        for t in range(keygen_trials):
            t0 = time.perf_counter_ns()
            key = rsa.generate_private_key(public_exponent=65537, key_size=size)
            t1 = time.perf_counter_ns()
            dt_ms = (t1 - t0) / 1_000_000.0
            keygen_times.append(dt_ms)
            raw_measurements.append({
                "algorithm": f"RSA-{size}",
                "operation": "keygen",
                "trial_index": t + 1,
                "latency_ms": round(dt_ms, 6)
            })
            if sample_key is None:
                sample_key = key

        if size == 2048:
            sample_rsa_key = sample_key

        pub_key = sample_key.public_key()
        signer = RSASigner(sample_key)
        verifier = RSAVerifier(pub_key)

        # 2. Signing
        sign_times: List[float] = []
        signatures: List[bytes] = []
        for t in range(crypto_trials):
            t0 = time.perf_counter_ns()
            sig = signer.sign(test_payload)
            t1 = time.perf_counter_ns()
            dt_ms = (t1 - t0) / 1_000_000.0
            sign_times.append(dt_ms)
            signatures.append(sig)
            raw_measurements.append({
                "algorithm": f"RSA-{size}",
                "operation": "sign",
                "trial_index": t + 1,
                "latency_ms": round(dt_ms, 6)
            })

        # 3. Verification
        verify_times: List[float] = []
        for t, sig in enumerate(signatures):
            t0 = time.perf_counter_ns()
            valid = verifier.verify(test_payload, sig)
            t1 = time.perf_counter_ns()
            assert valid
            dt_ms = (t1 - t0) / 1_000_000.0
            verify_times.append(dt_ms)
            raw_measurements.append({
                "algorithm": f"RSA-{size}",
                "operation": "verify",
                "trial_index": t + 1,
                "latency_ms": round(dt_ms, 6)
            })

        sec_bits = 112 if size == 2048 else (128 if size == 3072 else 152)

        # Calculate exact medians and statistics directly from trial lists
        kg_med = round(statistics.median(keygen_times), 4)
        sg_med = round(statistics.median(sign_times), 4)
        vf_med = round(statistics.median(verify_times), 4)

        row = {
            "algorithm": f"RSA-{size}",
            "key_size_bits": size,
            "security_strength_bits": sec_bits,
            "nist_reference": "NIST SP 800-56B Rev. 2, Table 2 & App. D",
            "keygen_median_ms": kg_med,
            "keygen_mean_ms": round(statistics.mean(keygen_times), 4),
            "keygen_std_ms": round(statistics.stdev(keygen_times) if len(keygen_times) > 1 else 0.0, 4),
            "keygen_min_ms": round(min(keygen_times), 4),
            "keygen_max_ms": round(max(keygen_times), 4),

            "sign_median_ms": sg_med,
            "sign_mean_ms": round(statistics.mean(sign_times), 4),
            "sign_std_ms": round(statistics.stdev(sign_times), 4),
            "sign_min_ms": round(min(sign_times), 4),
            "sign_max_ms": round(max(sign_times), 4),

            "verify_median_ms": vf_med,
            "verify_mean_ms": round(statistics.mean(verify_times), 4),
            "verify_std_ms": round(statistics.stdev(verify_times), 4),
            "verify_min_ms": round(min(verify_times), 4),
            "verify_max_ms": round(max(verify_times), 4),

            "signature_length_bytes": len(signatures[0]),
            "modulus_length_bytes": size // 8,
            "internal_asymmetry_ratio": round(sg_med / vf_med, 2),
            "trials_keygen": keygen_trials,
            "trials_crypto": crypto_trials
        }
        aggregated_results.append(row)

        print(f"  Keygen : Median={row['keygen_median_ms']} ms, Mean={row['keygen_mean_ms']} ms")
        print(f"  Sign   : Median={row['sign_median_ms']} ms, Mean={row['sign_mean_ms']} ms")
        print(f"  Verify : Median={row['verify_median_ms']} ms, Mean={row['verify_mean_ms']} ms")
        print(f"  Sig Size: {row['signature_length_bytes']} B | Modulus: {row['modulus_length_bytes']} B | Asymmetry (Sign/Verify): {row['internal_asymmetry_ratio']}x")

    # --- B. BENCHMARK ECDSA (secp256k1) ---
    print("\nEvaluating ECDSA (secp256k1) ...")
    ec_keygen_times: List[float] = []
    sample_ec_key = None
    for t in range(keygen_trials):
        t0 = time.perf_counter_ns()
        k = ec.generate_private_key(ec.SECP256K1())
        t1 = time.perf_counter_ns()
        dt_ms = (t1 - t0) / 1_000_000.0
        ec_keygen_times.append(dt_ms)
        raw_measurements.append({
            "algorithm": "ECDSA-secp256k1",
            "operation": "keygen",
            "trial_index": t + 1,
            "latency_ms": round(dt_ms, 6)
        })
        if sample_ec_key is None:
            sample_ec_key = k

    ec_pub = sample_ec_key.public_key()
    ec_sign_times: List[float] = []
    ec_signatures: List[bytes] = []
    for t in range(crypto_trials):
        t0 = time.perf_counter_ns()
        sig = sample_ec_key.sign(test_payload, ec.ECDSA(hashes.SHA256()))
        t1 = time.perf_counter_ns()
        dt_ms = (t1 - t0) / 1_000_000.0
        ec_sign_times.append(dt_ms)
        ec_signatures.append(sig)
        raw_measurements.append({
            "algorithm": "ECDSA-secp256k1",
            "operation": "sign",
            "trial_index": t + 1,
            "latency_ms": round(dt_ms, 6)
        })

    ec_verify_times: List[float] = []
    for t, sig in enumerate(ec_signatures):
        t0 = time.perf_counter_ns()
        ec_pub.verify(sig, test_payload, ec.ECDSA(hashes.SHA256()))
        t1 = time.perf_counter_ns()
        dt_ms = (t1 - t0) / 1_000_000.0
        ec_verify_times.append(dt_ms)
        raw_measurements.append({
            "algorithm": "ECDSA-secp256k1",
            "operation": "verify",
            "trial_index": t + 1,
            "latency_ms": round(dt_ms, 6)
        })

    ec_kg_med = round(statistics.median(ec_keygen_times), 4)
    ec_sg_med = round(statistics.median(ec_sign_times), 4)
    ec_vf_med = round(statistics.median(ec_verify_times), 4)

    ec_row = {
        "algorithm": "ECDSA-secp256k1",
        "key_size_bits": 256,
        "security_strength_bits": 128,
        "nist_reference": "NIST SP 800-57 Part 1 Rev. 5, Table 2",
        "keygen_median_ms": ec_kg_med,
        "keygen_mean_ms": round(statistics.mean(ec_keygen_times), 4),
        "keygen_std_ms": round(statistics.stdev(ec_keygen_times) if len(ec_keygen_times) > 1 else 0.0, 4),
        "keygen_min_ms": round(min(ec_keygen_times), 4),
        "keygen_max_ms": round(max(ec_keygen_times), 4),

        "sign_median_ms": ec_sg_med,
        "sign_mean_ms": round(statistics.mean(ec_sign_times), 4),
        "sign_std_ms": round(statistics.stdev(ec_sign_times), 4),
        "sign_min_ms": round(min(ec_sign_times), 4),
        "sign_max_ms": round(max(ec_sign_times), 4),

        "verify_median_ms": ec_vf_med,
        "verify_mean_ms": round(statistics.mean(ec_verify_times), 4),
        "verify_std_ms": round(statistics.stdev(ec_verify_times), 4),
        "verify_min_ms": round(min(ec_verify_times), 4),
        "verify_max_ms": round(max(ec_verify_times), 4),

        "signature_length_bytes": len(ec_signatures[0]),  # DER encoded (~70-72 B)
        "modulus_length_bytes": 33,  # Compressed secp256k1 public key
        "internal_asymmetry_ratio": round(ec_sg_med / ec_vf_med, 2),
        "trials_keygen": keygen_trials,
        "trials_crypto": crypto_trials
    }
    aggregated_results.append(ec_row)

    print(f"  Keygen : Median={ec_row['keygen_median_ms']} ms, Mean={ec_row['keygen_mean_ms']} ms")
    print(f"  Sign   : Median={ec_row['sign_median_ms']} ms, Mean={ec_row['sign_mean_ms']} ms")
    print(f"  Verify : Median={ec_row['verify_median_ms']} ms, Mean={ec_row['verify_mean_ms']} ms")
    print(f"  Sig Size: {ec_row['signature_length_bytes']} B (DER) | Compressed PubKey: 33 B | Asymmetry: {ec_row['internal_asymmetry_ratio']}x")

    # --- EXPORT 1: RAW TRIAL MEASUREMENTS CSV ---
    raw_csv_path = RAW_DIR / "raw_trials_all_algorithms.csv"
    with open(raw_csv_path, "w", newline="", encoding="utf-8") as rf:
        writer = csv.DictWriter(rf, fieldnames=["algorithm", "operation", "trial_index", "latency_ms"])
        writer.writeheader()
        writer.writerows(raw_measurements)
    print(f"\n[+] Raw trial measurements ({len(raw_measurements)} records) saved to: {raw_csv_path}")

    # --- EXPORT 2: AGGREGATED BENCHMARK SUMMARY CSV ---
    agg_csv_path = DATA_DIR / "benchmark_results.csv"
    with open(agg_csv_path, "w", newline="", encoding="utf-8") as af:
        writer = csv.DictWriter(af, fieldnames=list(aggregated_results[0].keys()))
        writer.writeheader()
        writer.writerows(aggregated_results)
    print(f"[+] Aggregated benchmark summary saved to: {agg_csv_path}")

    # --- VERIFY MATHEMATICAL CONSISTENCY BETWEEN RAW AND AGGREGATED ---
    print("\nVerifying consistency between raw trial data and aggregated statistics...")
    for agg in aggregated_results:
        alg = agg["algorithm"]
        for op in ("keygen", "sign", "verify"):
            raw_vals = [r["latency_ms"] for r in raw_measurements if r["algorithm"] == alg and r["operation"] == op]
            calc_med = round(statistics.median(raw_vals), 4)
            rep_med = agg[f"{op}_median_ms"]
            assert calc_med == rep_med, f"Inconsistency detected for {alg} {op}: calculated {calc_med} vs reported {rep_med}"
    print("[Pass] Perfect 100% mathematical consistency confirmed: All raw medians exactly match aggregated table.")

    return {
        "aggregated": aggregated_results,
        "raw_count": len(raw_measurements),
        "sample_rsa_key": sample_rsa_key
    }


# =====================================================================
# 7. PERFORMANCE CHART GENERATION
# =====================================================================

def generate_benchmark_chart(results: list, output_path: Path):
    import matplotlib.pyplot as plt
    import numpy as np

    labels = [r["algorithm"] for r in results]
    keygen = [r["keygen_median_ms"] for r in results]
    sign = [r["sign_median_ms"] for r in results]
    verify = [r["verify_median_ms"] for r in results]

    x = np.arange(len(labels))
    width = 0.28

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 2.8), dpi=300)

    # Subplot 1: Key Generation (Logarithmic scale)
    bars1 = ax1.bar(x, keygen, width=0.45, color=['#1f77b4', '#1f77b4', '#1f77b4', '#ff7f0e'], edgecolor='black', alpha=0.85)
    ax1.set_title('Key Generation Latency (Median)', fontsize=8.5, fontweight='bold', pad=6)
    ax1.set_xlabel('Cryptographic Algorithm', fontsize=7.5)
    ax1.set_ylabel('Latency (ms, Log Scale)', fontsize=7.5)
    ax1.set_yscale('log')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=7, rotation=10)
    ax1.tick_params(axis='both', labelsize=7)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f'{yval:.1f}ms', ha='center', va='bottom', fontsize=6.8, fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.6)

    # Subplot 2: Signing vs Verification Latency
    rects1 = ax2.bar(x - width/2, sign, width, label='Sign (ms)', color='#d62728', edgecolor='black', alpha=0.85)
    rects2 = ax2.bar(x + width/2, verify, width, label='Verify (ms)', color='#2ca02c', edgecolor='black', alpha=0.85)
    ax2.set_title('Signing vs. Verification Latency (Median)', fontsize=8.5, fontweight='bold', pad=6)
    ax2.set_xlabel('Cryptographic Algorithm', fontsize=7.5)
    ax2.set_ylabel('Latency (ms)', fontsize=7.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=7, rotation=10)
    ax2.tick_params(axis='both', labelsize=7)
    ax2.legend(fontsize=7, loc='upper left')
    for bar in rects1:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f'{yval:.2f}', ha='center', va='bottom', fontsize=6.5)
    for bar in rects2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.15, f'{yval:.3f}', ha='center', va='bottom', fontsize=6.5)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[+] Benchmark chart saved to: {output_path}")


# =====================================================================
# 8. MAIN EXECUTION ROUTINE
# =====================================================================

def main():
    print("="*75)
    print("ACADEMIC EXPERIMENTAL EXECUTION SUITE: REAL-WORLD APPLICATIONS OF RSA")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Platform    : {platform.platform()}")
    print(f"Python      : {sys.version.split()[0]}")
    print(f"OpenSSL     : {ossl_backend.openssl_version_text()}")
    print("="*75)

    # 1. Execute full Wycheproof test suite (108 cases)
    wyche_json = REF_DIR / "Wycheproof_Test_Vector" / "rsa_pss_2048_sha256_mgf1_32_test.json"
    wyche_res = run_wycheproof_suite(wyche_json)

    # 2. Benchmark data handling: Preserve existing verified benchmark files unless --rerun-benchmarks is requested
    bench_csv = DATA_DIR / "benchmark_results.csv"
    raw_csv = DATA_DIR / "raw_benchmark_logs" / "raw_trials_all_algorithms.csv"
    rerun_requested = "--rerun-benchmarks" in sys.argv

    if rerun_requested or not (bench_csv.exists() and raw_csv.exists()):
        print("\n[*] Executing unified benchmark suite (10 keygen, 100 crypto trials per algorithm)...")
        bench_data = run_benchmarks_and_export(rsa_key_sizes=(2048, 3072, 4096), keygen_trials=10, crypto_trials=100)
        chart_path = FIG_DIR / "benchmark_performance.png"
        generate_benchmark_chart(bench_data["aggregated"], chart_path)
        priv_2048 = bench_data["sample_rsa_key"]
    else:
        print("\n[*] Preserving existing verified benchmark datasets:")
        print(f"    - Aggregated CSV: {bench_csv}")
        print(f"    - Raw Trials CSV: {raw_csv}")
        print("    (Pass '--rerun-benchmarks' to force re-execution of benchmark measurements)")
        priv_2048 = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # 3. Execute five practical operational scenarios
    run_scenarios(priv_2048, priv_2048.public_key())

    print("\n" + "="*75)
    print("ALL EXPERIMENTS, BENCHMARKS, AND TEST SCENARIOS COMPLETED SUCCESSFULLY.")
    print("="*75)


if __name__ == "__main__":
    main()
