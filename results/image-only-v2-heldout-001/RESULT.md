# Image-only v2 held-out 001

Status: FAIL — historical use blocked.

Frozen decoder blob: `75207864d07573edf53fe29b321381e732347b91`

Workflow run: `37398721829`
Artifact: `11384058580`
Artifact ZIP SHA-256: `ced3c2c88342ee5db1f31b64ca1b518b03a1bde2c425c13881d939384a137f38`

## Prospective criterion

A3, B6, and C9 each had to classify all 20 held-out known-answer cells correctly. There was no majority-vote rescue or post-hoc threshold adjustment.

## Result

- A3: 20 / 20 — PASS
- B6: 17 / 20 — FAIL
- C9: 20 / 20 — PASS
- Overall gate: FAIL

## B6 failures

All three misses concern `left-margin-discrete-repetition` on cases where the answer key is `present`:

- `positive_d`: best margin lag 138 px, autocorrelation 0.84245, top-20% column-energy fraction 0.99702;
- `disrupted_d`: best margin lag 138 px, same margin measurements;
- `marker_only`: best margin lag 130 px, autocorrelation 0.83922, top-20% column-energy fraction 0.99672.

B6's frozen rule required a margin lag in the interval 30–120 px. The held-out structures therefore failed solely because their strongest valid periodicity lay above the hard upper bound.

## Interpretation

This is a narrower failure than v1. The periodic texture/null false-positive problem that blocked `image-only-001.0` did not recur here. A3 and C9 transported perfectly across all held-out geometry, and B6 correctly handled all central-structure and null cases.

However, the prospective rule was strict. The family set does not pass because B6 did not generalize its absolute scale range.

The appropriate lesson is methodological: the fixed absolute margin-lag ceiling is not transport-stable. This result may motivate a scale-normalized or otherwise less arbitrary replacement in a new decoder version, but the three held-out misses cannot be repaired inside `image-only-002.0-dev`.

## Boundary

No f113r rerun is authorized. `image-only-002.0-dev` is frozen as a failed held-out candidate.

Any successor must receive a new version, may use this failure only as development evidence, and must face a new future held-out set that has not been used for tuning. No Voynich interpretation, translation, or decipherment follows from this result.
