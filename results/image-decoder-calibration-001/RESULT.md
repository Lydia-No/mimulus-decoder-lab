# Image decoder calibration 001 — frozen result

Status: **FAIL** for `image-only-001.0` historical reuse.

Research direction, conceptual framing and methodology: Linda Thorstensen.

## Gate

Predeclared criterion: each decoder must classify all 8 known-answer claim-condition cells correctly.

Result:

- A2: **7/8** — fail;
- B5: **5/8** — fail;
- C8: **5/8** — fail;
- overall gate: **failed**.

The decoder version `image-only-001.0` is therefore blocked from another substantive f113r run.

## What passed

All three decoders correctly handled the straightforward positive construction and the margin-marker ablation:

- `positive_structured`: horizontal repetition present; margin repetition present;
- `margin_ablated`: horizontal repetition present; margin repetition not detected.

A2 also correctly rejected horizontal organization in the central-disruption control while retaining the margin signal.

## Failure pattern

### Texture null

The strongest result is the texture control.

All three decoders falsely reported horizontal repetition in deterministic fine periodic microtexture that had no macro line-group structure.

B5 and C8 also falsely reported discrete left-margin repetition on that texture control.

This means the v1.0 decoders can confuse lower-level periodicity or occupancy with the higher-level visual organization named by their claims.

### Central disruption

B5 and C8 also reported horizontal repetition after the central line-group organization had been deliberately destroyed while approximate glyph mass was retained.

B5's best central autocorrelation occurred at lag 8 px in that control. C8 marked 62 of 72 vertical bins active. These are consistent with the failure modes already visible in the first historical f113r run: sensitivity to fine-scale texture for B5 and an overly permissive occupancy rule for C8.

## Relation to f113r run 001

This calibration does not reinterpret or erase `f113r-image-only-001`. That run remains the frozen first historical transport attempt.

Instead, the calibration explains why its disagreement cannot currently be resolved by choosing one of A2/B5/C8 as the preferred observer. The relevant decoder family has not yet passed a basic known-answer discrimination gate.

## Next version boundary

Do not tune `image-only-001.0` directly on f113r.

A replacement decoder version should be developed against synthetic calibration material and then evaluated on a **separate held-out synthetic set** before any historical rerun. The held-out set should vary line spacing, glyph density, marker count, marker spacing, texture frequency, noise, blur and contrast so that passing cannot be achieved by matching the four existing fixtures.

Only a decoder version that passes the prospective holdout should be eligible for another f113r comparison.

No transcription, language identification, translation, decipherment or historical meaning is supported by this calibration result.
