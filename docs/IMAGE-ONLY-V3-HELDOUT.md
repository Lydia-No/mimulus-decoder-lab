# Image-only v3 — fresh held-out gate

Status: prospective. No v3 held-out output existed when this protocol was introduced.

Frozen candidate decoder blob:

`historical/image_decoders_v3.py` → Git blob `24cd6a61c1744657ef6bbd62b14ee47a0afb8c8d`

The v3 development matrix scored 96/96 cells. That matrix includes the already-inspected v2 holdout and is not validation evidence for v3.

## Fresh holdout

Twelve new conditions are fixed prospectively, with seeds and geometry not used in prior development/holdout sets:

- two structured positives;
- two central disruptions with margin repetition retained;
- two margin ablations;
- two new periodic texture nulls;
- one marker-only positive;
- one irregular but horizontally concentrated margin null;
- one vertical-margin-rule null;
- one mixed sparse null.

Each condition has two known-answer claims, yielding 24 held-out cells per decoder and 72 total.

The two new adversarial margin nulls specifically test whether B7 confuses horizontal concentration with discrete vertical repetition.

## Pass criterion

A3, B7, and C9 must each score 24/24. No majority vote or post-hoc correction is permitted.

CI verifies the frozen v3 decoder Git blob before execution. Any mismatch aborts the run.

Failure blocks historical use of this candidate. Success authorizes only a separately preregistered f113r run using the unchanged decoder blob; it does not establish any Voynich interpretation or decipherment.
