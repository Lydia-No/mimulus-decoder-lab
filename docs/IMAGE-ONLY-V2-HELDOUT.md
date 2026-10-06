# Image-only v2 — held-out gate

Status: prospective held-out protocol; no held-out run has occurred at the time this file is introduced.

Frozen candidate decoder blob:

`historical/image_decoders_v2.py` → Git blob `75207864d07573edf53fe29b321381e732347b91`

Development result: A3 16/16, B6 16/16, C9 16/16. Development performance is not counted as held-out evidence.

## Held-out construction

The held-out generator was created only after the candidate decoder blob above had been merged and frozen. It uses new seeds and parameters not present in the development set.

Ten conditions are fixed prospectively:

- two structured positives with new line/marker spacings and small line-position jitter;
- two central disruptions with preserved margin markers, including a new ellipse-based disruption family;
- two margin ablations;
- two periodic texture nulls with new mark geometry and spacings;
- one marker-only case;
- one sparse non-periodic null.

Each condition has two known-answer claims:

1. macro horizontal repetition;
2. discrete left-margin repetition.

That yields 20 held-out cells per decoder and 60 total.

## Pass criterion

A3, B6, and C9 must each classify all 20 held-out cells correctly. There is no majority-vote rescue and no post-hoc threshold adjustment.

If any decoder misses any held-out cell, `image-only-002.0-dev` is blocked from historical use. A later redesign must receive a new version and a new future holdout; this held-out set cannot become a tuning set for the same candidate.

If all three pass, the result authorizes only the next procedural step: a separately preregistered historical f113r run using the unchanged decoder blob. It does not validate a Voynich interpretation.

## Execution guard

The CI workflow verifies the Git blob hash of `historical/image_decoders_v2.py` before running the holdout. A mismatch aborts the test.
