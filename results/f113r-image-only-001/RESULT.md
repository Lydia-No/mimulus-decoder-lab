# f113r image-only run 001 — frozen result

Status: completed historical image-only run; result frozen without retuning.

Research direction, conceptual framing and methodology: Linda Thorstensen.

## Result

The first image-only historical run did **not** produce a stable cross-decoder residue on either preregistered question.

For `horizontal-repetition`:

- A2: `not_detected`;
- B5: `present`;
- C8: `present`;
- historical meta-observer: `INCOMPATIBLE_READINGS`.

For `left-margin-discrete-repetition`:

- A2: `not_detected`;
- B5: `present`;
- C8: `not_detected`;
- historical meta-observer: `INCOMPATIBLE_READINGS`.

No Voynich meaning, language, translation or decipherment follows from this result.

## Diagnostics

The disagreement is itself useful because the raw measurements expose representation-specific failure modes.

### A2

A2 produced only one central row-projection band and one margin band after its preregistered thresholding. That means the representation effectively collapsed most dark structure into continuous activity instead of resolving repeated visual units. Its `not_detected` outputs should therefore not be read as evidence that the page lacks horizontal or margin organization.

### B5

B5 found strong gradient-energy autocorrelation in both regions: 0.4423 at lag 21 px centrally and 0.4505 at lag 20 px in the margin. The margin optimum occurs at the lower edge of the preregistered lag range, so it may be responding to fine-scale texture/stroke rhythm rather than the intended class of discrete margin features. The result is retained exactly as produced, but requires a control before substantive interpretation.

### C8

C8 marked horizontal repetition `present` because 65 of 72 vertical bins met its component-occupancy criterion. That is highly permissive on this real page and may be detecting broad page-wide ink occupancy rather than repeated units. In the margin it generated 49 collapsed loci, exceeding the preregistered 8–35 range, so the margin proposition was `not_detected` despite a median locus gap of 8.10 px.

## Interpretation

The important result of run 001 is therefore not that one decoder is right. It is that the first transport from the synthetic gate to a real historical image exposes a calibration problem:

- binary decisions are too sensitive to representation choice;
- at least one decoder is degenerate under the real image distribution;
- another may be responding to fine-scale texture;
- another is too permissive for the horizontal claim.

This is exactly the kind of failure Mimulus is intended to preserve rather than average away.

## Next gate

Do **not** retune A2/B5/C8 directly against f113r.

The next step should be an image-specific known-answer calibration set constructed independently of Voynich output, including at minimum:

1. a positive synthetic page with repeated horizontal bands and repeated left-margin markers;
2. an ink-density-matched control with horizontal organization disrupted;
3. a margin-marker ablation;
4. a texture/null control capable of triggering short-lag autocorrelation without discrete markers.

Only after that calibration should a versioned image decoder set be rerun on f113r.

The v1.0 result remains frozen as the first historical transport attempt.
