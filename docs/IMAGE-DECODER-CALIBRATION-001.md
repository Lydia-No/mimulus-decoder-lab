# Image decoder calibration 001

Status: preregistered known-answer calibration for `image-only-001.0`.

Research direction, conceptual framing and methodology: Linda Thorstensen.

## Why this gate exists

The first historical f113r image-only run produced incompatible decoder readings and exposed representation-specific failure modes. The decoder thresholds must therefore not be retuned directly against f113r.

This calibration uses synthetic images with known construction before any versioned historical rerun.

## Frozen decoder version

The calibration evaluates the existing A2, B5 and C8 implementations in `historical/image_only_f113r.py` at version `image-only-001.0`. The decoder logic is not changed for this calibration.

## Four controls

All images use the same 2582 × 3787 canvas as the frozen f113r authority image.

### `positive_structured`

Contains 42 repeated horizontal line-like groups in the central region and 16 repeated discrete margin markers.

Known answer:

- `horizontal-repetition`: `present`
- `left-margin-discrete-repetition`: `present`

### `central_disrupted`

Preserves approximately the same central glyph mass but randomizes the vertical locations of those glyph-like units. The 16 margin markers remain intact.

Known answer:

- `horizontal-repetition`: `not_detected`
- `left-margin-discrete-repetition`: `present`

### `margin_ablated`

Preserves the structured central horizontal groups but removes the margin markers.

Known answer:

- `horizontal-repetition`: `present`
- `left-margin-discrete-repetition`: `not_detected`

### `texture_null`

Contains deterministic fine periodic microtexture but no macro text-line groups and no discrete margin-marker objects. This control is specifically intended to expose short-lag autocorrelation or occupancy false positives.

Known answer:

- `horizontal-repetition`: `not_detected`
- `left-margin-discrete-repetition`: `not_detected`

## Seed and generation

Generator seed: `170113`.

The generator and exact known-answer table are implemented in `historical/image_calibration.py` and are frozen before the result-bearing calibration run.

## Gate criterion

Each decoder is scored on 8 claim-condition cells: two claims across four controls.

The calibration gate passes only if **each decoder classifies all 8 cells correctly**.

This is deliberately strict. These are simple known-answer constructions intended to test whether the decoder is measuring its declared target rather than incidental image statistics.

## Consequence

If the gate fails, `image-only-001.0` is not eligible for a substantive historical rerun. Any redesign becomes a new version and must be validated on calibration controls before another f113r run.

The calibration does not modify or reinterpret the already frozen `f113r-image-only-001` result.
