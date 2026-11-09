# TASKS.md
# Project Roadmap — 10 Macro Milestones

**Primary deliverable:** 4–5 page academic report  
**Execution policy:** Report-First Development  
**Bug-fix fallback budget:** Maximum 5 rounds  
**Rule:** Do not mark a milestone complete unless its acceptance criteria pass.

---

## M01 — Repository Audit & Baseline

- [x] M01: Audit repository structure, current project state, and integrity baseline.

**Scope:**
- `README.md`
- `FINAL_REVIEW_NOTES.md`
- `SHA256SUMS.txt`
- `01_Final_Report/`
- `02_Source_Code/`
- `03_Experimental_Data/`
- `04_Figures/`
- `05_Research_References/`
- `06_Environment/`

**Tasks:**
- Confirm existing files and identify the actual report file.
- Record current repository state and existing limitations.
- Check whether the integrity manifest matches the current files.
- Do not recursively dump or summarize the entire repository.

**Acceptance criteria:**
- Existing structure is documented.
- Missing or inconsistent files are identified.
- No original evidence is overwritten.
- Findings are recorded in `FINAL_REVIEW_NOTES.md`.

---

## M02 — Environment & Reproducibility

- [x] M02: Verify dependencies, runtime environment, and reproducible execution.

**Scope:**
- `06_Environment/`
- `02_Source_Code/`
- Relevant dependency/configuration files only.

**Tasks:**
- Inspect Python and dependency versions.
- Identify the minimum commands required to execute the prototype and tests.
- Run the relevant commands in the documented environment.
- Record failures separately from warnings.

**Acceptance criteria:**
- Environment requirements are documented.
- Relevant scripts can run, or blockers are precisely identified.
- No unnecessary dependency upgrades are introduced.

---

## M03 — RSA Cryptographic Implementation Audit

- [x] M03: Audit RSA-PSS, hashing, key handling, and deterministic serialization.

**Scope:**
- `02_Source_Code/rsa_pss_experiment.py`
- Relevant cryptographic tests only.

**Tasks:**
- Verify RSA-PSS parameters and SHA-256 usage.
- Verify MGF1 and salt-length configuration.
- Inspect signing and verification behavior.
- Inspect canonical JSON serialization and its documented guarantees.
- Check that OAEP and PSS are not incorrectly conflated.

**Acceptance criteria:**
- Actual implementation behavior is documented.
- Security-relevant discrepancies are fixed or recorded.
- No unsupported standards-compliance claim remains.

---

## M04 — Request Validation & Replay Protection

- [x] M04: Audit timestamp, nonce, payload validation, and replay handling.

**Scope:**
- `02_Source_Code/rsa_pss_experiment.py`
- Directly related validation tests.

**Tasks:**
- Inspect timestamp freshness logic and configured time window.
- Inspect nonce uniqueness and replay behavior.
- Check behavior under repeated and concurrent requests where practical.
- Inspect recipient and amount validation.
- Separate signature validity from business authorization.

**Acceptance criteria:**
- Validation behavior is tested and documented.
- In-memory replay-protection limitations are explicit.
- No claim of customer identity or withdrawal authorization is inferred from RSA signature validity.

---

## M05 — Adversarial Tests & Wycheproof

- [x] M05: Execute tampering, replay, invalid-key, and Wycheproof test coverage.

**Scope:**
- `02_Source_Code/`
- `05_Research_References/`
- Relevant test logs in `03_Experimental_Data/`

**Tasks:**
- Run the five existing adversarial scenarios.
- Verify the actual Wycheproof test bundle and test runner.
- Check accepted/rejected case counts.
- Investigate any unexpected pass, failure, or skipped test.

**Acceptance criteria:**
- Test commands and outcomes are recorded.
- Test counts match actual output or are corrected.
- Failures are not silently ignored.

---

## M06 — Benchmark Reproduction

- [x] M06: Re-run RSA and ECDSA benchmarks and verify reported performance claims.

**Scope:**
- `02_Source_Code/`
- `03_Experimental_Data/benchmark_results.csv`
- Relevant environment metadata in `06_Environment/`

**Tasks:**
- Identify the original benchmark methodology.
- Re-run the benchmark using documented parameters.
- Record environment, repetitions, and aggregation method.
- Compare new results with stored CSV values.
- Explain discrepancies rather than silently replacing them.

**Acceptance criteria:**
- Reproduced data is distinguishable from historical data.
- Any reported speed ratio is calculated from the correct measurements.
- Benchmark limitations are documented.

---

## M07 — Figures, References & Standards Audit

- [x] M07: Verify figures, bibliography, and standards-related statements.

**Scope:**
- `04_Figures/`
- `05_Research_References/`
- `01_Final_Report/`
- Relevant sections of `README.md`

**Tasks:**
- Verify that figures accurately represent the implementation.
- Check reference metadata and relevance to the claims they support.
- Verify standards-related statements against the cited primary sources.
- Identify outdated, ambiguous, or unsupported claims.

**Acceptance criteria:**
- Each important technical claim has appropriate supporting evidence.
- Figure labels and architecture descriptions are consistent.
- Unsupported references or statements are corrected or qualified.

---

## M08 — Report & Evidence Consistency Review

- [ ] M08: Cross-check the report against code, tests, benchmarks, and references.

**Scope:**
- `01_Final_Report/`
- `02_Source_Code/`
- `03_Experimental_Data/`
- `04_Figures/`
- `05_Research_References/`
- `FINAL_REVIEW_NOTES.md`

**Tasks:**
- Cross-check algorithm parameters and architecture descriptions.
- Cross-check benchmark numbers and test counts.
- Check that limitations are accurately represented.
- Resolve contradictions using verified evidence.
- Preserve the WHAT / WHY / HOW structure.

**Acceptance criteria:**
- No material contradiction remains unexplained.
- Every reported result has a traceable source.
- The report does not overstate prototype capabilities.

---

## M09 — Final Report Editing & Layout

- [ ] M09: Polish the final report to approximately 4–5 A4 pages.

**Scope:**
- `01_Final_Report/`
- `04_Figures/`
- Relevant bibliography files in `05_Research_References/`

**Tasks:**
- Improve clarity, academic tone, and technical precision.
- Remove redundant explanations.
- Optimize tables, figures, captions, and references.
- Preserve the original research framing.
- Verify actual page count after saving/exporting.

**Acceptance criteria:**
- Final report is approximately 4–5 A4 pages.
- Formatting is readable and consistent.
- No unsupported result or claim is introduced during editing.

---

## M10 — Final Verification & Release

- [ ] M10: Run final checks, regenerate integrity manifest, and prepare the deliverable.

**Scope:**
- `SPEC.md`
- `TASKS.md`
- `README.md`
- `FINAL_REVIEW_NOTES.md`
- `SHA256SUMS.txt`
- All final deliverable paths, as needed.

**Tasks:**
- Run the relevant final tests.
- Verify report page count and file presence.
- Regenerate `SHA256SUMS.txt` if tracked files changed.
- Confirm that references, data, figures, and report are synchronized.
- Record unresolved limitations and final status.

**Acceptance criteria:**
- Final report and supporting evidence are present.
- Integrity manifest is current.
- All 10 milestones have an accurate status.
- Final review notes explain any remaining limitations.

---

## Bug-Fix Budget

Maximum: 5 fallback rounds for the entire project.

Record each round here:

| Round | Root cause | Files changed | Verification |
|---|---|---|---|
| 1 | Pending | Pending | Pending |
| 2 | Pending | Pending | Pending |
| 3 | Pending | Pending | Pending |
| 4 | Pending | Pending | Pending |
| 5 | Pending | Pending | Pending |

Do not consume a fallback round for cosmetic changes. Each round must address a concrete failure.

## Progress Summary

- Completed milestones: 7/10
- Current milestone: M08
- Remaining fallback rounds: 5/5
- Primary deliverable: 4–5 page report
