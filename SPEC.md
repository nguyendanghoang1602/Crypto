# SPEC.md
# Project Specification

## 1. Project Identity

**Project title:** Real-World Applications of RSA: Cryptographic Foundations, Practical Implementation, and Off-Chain Blockchain Authentication.

**Primary deliverable:** A technically accurate, reproducible academic report of approximately 4–5 A4 pages.

**Working model:** Report-First Development. Source code, test results, benchmark data, figures, and references are supporting evidence for the report, not independent product-development goals.

**Repository baseline:** Existing GitHub repository and its current directory structure. Preserve the original implementation and evidence before modifying them.

## 2. Project Objectives

The report must address three central questions:

### WHAT — Cryptographic foundations

- Explain the RSA mathematical foundation at the level required by the report.
- Distinguish RSA-OAEP encryption/key transport from RSA-PSS digital signatures.
- Explain the practical role of RSA in PKI, TLS, code signing, and enterprise infrastructure.

### WHY — Algorithm and architecture comparison

- Compare RSA with ECDSA, Schnorr, and Ed25519 where supported by the existing research.
- Explain the trade-offs between signature size, signing performance, verification performance, and deployment context.
- Explain why off-chain RSA verification may be useful in a blockchain-related authentication workflow.
- Do not present benchmark results as universal performance guarantees.

### HOW — Educational implementation

Analyze and validate the existing educational cryptocurrency withdrawal authentication prototype.

Expected conceptual flow:

1. Withdrawal service creates a request.
2. Request includes network, recipient, integer atomic amount, UUIDv4 nonce, and UNIX timestamp.
3. Deterministic JSON serialization produces the signed message.
4. RSA-PSS with SHA-256 signs the message.
5. Verification gateway verifies the signature.
6. Validation engine checks timestamp freshness and nonce uniqueness.
7. The request is accepted or rejected.

The implementation is educational and must not be described as a production-ready withdrawal authorization system.

## 3. Existing Repository Components

Preserve and inspect the existing paths:

- `01_Final_Report/`: primary report.
- `02_Source_Code/`: Python implementation, tests, and benchmark scripts.
- `03_Experimental_Data/`: benchmark CSV and test logs.
- `04_Figures/`: architecture, process, and performance figures.
- `05_Research_References/`: references and test vectors.
- `06_Environment/`: dependencies and environment information.
- `README.md`: repository overview.
- `FINAL_REVIEW_NOTES.md`: previous technical review notes.
- `SHA256SUMS.txt`: integrity manifest.

Known implementation components include:

- `WithdrawalRequest`
- `DeterministicJSONSerializer`
- `RSASigner`
- `RSAVerifier`
- `RequestValidator`

Known test scenarios include valid requests, amount tampering, recipient tampering, fake public keys, replay attempts, and RSA-PSS Wycheproof vectors.

Do not assume that the current code or stored results have been independently verified until the relevant milestone has completed.

## 4. Security and Correctness Constraints

The prototype has important limitations that must remain explicit:

- In-memory RSA keys are not a production key-management solution.
- An in-memory nonce set does not provide atomic replay protection across concurrent workers or multiple service instances.
- Basic recipient-address checks do not establish ownership or authorization.
- A valid RSA signature proves possession of the corresponding private key and integrity of the signed payload. It does not independently prove customer identity, account ownership, AML compliance, or authorization to withdraw funds.
- No production PKI, key rotation, revocation, HSM, customer authentication, or distributed replay store should be claimed unless actually implemented and verified.
- Application-level deterministic JSON serialization must not be described as full RFC 8785 compliance unless demonstrated.

Any security limitation discovered during review must be reflected in the report.

## 5. Benchmark Evidence

Existing repository benchmark data reports:

| Algorithm | Median verification | Median signing |
|---|---:|---:|
| RSA-2048 | 0.0462 ms | 0.9005 ms |
| RSA-3072 | 0.0756 ms | 2.7834 ms |
| RSA-4096 | 0.1150 ms | 6.5425 ms |
| ECDSA-secp256k1 | 0.6214 ms | 0.7196 ms |

The existing report describes RSA-3072 verification as approximately 8.22× faster than ECDSA-secp256k1, while ECDSA signing is approximately 3.87× faster.

These are existing repository claims, not independently reproduced facts. Re-run the benchmark before presenting them as reproduced results. Record environment, repetitions, aggregation method, and any discrepancy.

## 6. Test Evidence

The repository describes a bundled RSA-PSS Wycheproof 2048/SHA-256/MGF1-SHA256 snapshot:

- 108 test cases.
- 63 valid cases accepted.
- 45 invalid cases rejected.

Verify the actual test bundle, test runner, and output before treating these numbers as confirmed.

## 7. Report Requirements

- Target length: approximately 4–5 A4 pages.
- Preserve the WHAT / WHY / HOW framing.
- Keep the report technically precise and evidence-based.
- Prefer concise tables and existing figures where they improve clarity.
- Every quantitative claim must be traceable to a reproducible result or a cited source.
- Clearly distinguish measured results, existing repository claims, standards-based facts, and limitations.
- Do not add material merely to increase page count.

## 8. Engineering Workflow

Use exactly 10 milestones defined in `TASKS.md`.

For each milestone:

1. Read only the explicitly scoped files.
2. Make the smallest necessary change.
3. Run only relevant tests or commands.
4. Inspect the resulting diff.
5. Update the relevant checkbox in `TASKS.md` only when its acceptance criteria pass.
6. Record material findings in the appropriate project document.

Maximum bug-fix fallback budget: 5 rounds for the whole project. Do not conceal repeated failures by endlessly retrying.

## 9. Definition of Done

The project is complete when:

- The report is 4–5 pages and consistent with the verified implementation and evidence.
- The relevant tests have been executed and their outcomes recorded.
- Benchmark claims are reproducible or explicitly qualified.
- Security limitations are clearly documented.
- References support the claims attributed to them.
- Figures and data agree with the report.
- `SHA256SUMS.txt` is regenerated if tracked files change.
- All 10 milestones have a documented final status.
- The repository can be reviewed without relying on undocumented assumptions.

## 10. Change Control

Do not:

- Replace the project topic.
- Rewrite the repository architecture without a demonstrated need.
- Invent benchmark or test results.
- Claim production-grade security for the educational prototype.
- Delete existing evidence or original files without preserving a baseline.
- Expand the implementation beyond what is necessary to support the report.

When evidence contradicts the report, prioritize verified evidence and document the correction.