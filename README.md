# Mimulus Decoder Lab

Experimental framework for testing interpretations of opaque symbolic material across multiple independent decoder contexts.

The project preserves provenance and distinguishes **semantic plausibility** from **source-constrained evidence**. It is a decoder/meta-observer experiment, not a claim that any target text has been deciphered.

## Research question

When an opaque symbolic sequence is interpreted under multiple independently specified decoder contexts, what structure is stable across interpretations, what depends on the decoder, and what can actually be traced back to constraints in the source?

The immediate experimental target is the Voynich Manuscript. The framework itself is intended to remain target-agnostic.

## Boundary

This repository contains a deliberately bounded public experiment. It does **not** treat fluent output as evidence of a correct translation, and it does not infer a hidden language merely because an interpretation is coherent.

A candidate reading remains separable into:

1. source observations — features directly represented in the input;
2. decoder assumptions — mappings, grammars, priors, or operators introduced by the decoder;
3. derived structure — consequences of applying those assumptions;
4. semantic interpretation — meaning assigned to the derived structure;
5. cross-decoder residue — features that survive meaningful changes of decoder context.

The last category is interesting, but still does not by itself establish historical or linguistic truth.

## Method

The lab develops a reproducible pipeline around:

`source → observation → decoder context → candidate reading → comparison/meta-observation`

Multiple decoder contexts should be evaluated independently where possible. Comparison occurs after candidate readings are produced rather than forcing all decoders into a single shared semantic scheme.

## Current runnable pilot

`pilot/` contains **Pilot 001 — decoder persistence**, a deterministic known-answer gate for the measurement scaffold.

Three materially different decoder families inspect the same frozen synthetic source. The meta-observer then distinguishes source-supported invariants, decoder-dependent supported features, unsupported candidate structure and missed source features. A separate controlled history arm uses different, reset, swapped and identical retained states.

The pilot is deliberately synthetic. Passing it does not validate transport to Voynich; it only establishes that the implementation can preserve the distinctions the historical experiment requires.

See `docs/PILOT-001-DECODER-PERSISTENCE.md`, `pilot/README.md`, and the frozen result bundle in `results/pilot-001/`.

The frozen result is treated as a prospective gate: historical outputs do not retroactively change the Pilot 001 answer key, decoder behavior or result classification.

## Historical adapter

`historical/adapter.js` implements the bounded transition from the known-answer synthetic gate to historical material.

The historical adapter deliberately does **not** reuse known-answer result labels. Voynich has no independent answer key, so unanimous decoder agreement is recorded only as `CROSS_DECODER_RESIDUE`; partial agreement, decoder-specific claims and incompatible readings remain distinct.

The f113r source-image gate is open. The full-folio JPEG was fetched directly from Yale's IIIF Image API, frozen at SHA-256 `ad748f9012b174be520b7ac837fdadf913e49a696323920ca655ecf5474afb5c`, and independently fetched again with the same hash. The image is 2582 × 3787 pixels and 2,092,549 bytes. Any transcription supplied to a decoder still requires its own declared convention, version and frozen hash.

See `docs/HISTORICAL-INPUT-ADAPTER.md` and `fixtures/voynich/f113r/authority-freeze.json`.

## First historical image-only run

`f113r-image-only-001` is the first result-bearing historical transport test. Its three decoder families were preregistered before output inspection and received only the frozen f113r image.

The run produced `INCOMPATIBLE_READINGS` on both preregistered structural questions. No unanimous cross-decoder residue was produced. The raw outputs also exposed decoder-specific calibration problems, so the v1.0 result is frozen rather than retuned against f113r.

See `docs/F113R-IMAGE-ONLY-PILOT.md` and `results/f113r-image-only-001/RESULT.md`.

## Image decoder calibration 001

The frozen `image-only-001.0` decoder set was subsequently tested against preregistered known-answer image controls rather than tuned on f113r.

The strict gate failed:

- A2: 7/8;
- B5: 5/8;
- C8: 5/8.

All three produced a false horizontal-repetition signal on the texture/null control; B5 and C8 also produced false margin-repetition signals there. B5 and C8 additionally failed the central-disruption horizontal control.

`image-only-001.0` is therefore **blocked from further substantive historical reuse**.

See `docs/IMAGE-DECODER-CALIBRATION-001.md` and `results/image-decoder-calibration-001/RESULT.md`.

## Image-only v2 development and held-out gate

A versioned replacement, `image-only-002.0-dev`, was developed entirely on synthetic material. It specifically addressed the v1 texture false-positive failure by requiring macro structure rather than generic periodicity.

Its three new families were A3 (macro horizontal-run bands), B6 (smoothed gradient periodicity plus spatial concentration), and C9 (macro connected-component row clustering). On the declared development set all three scored 16/16, for 48/48 cells total.

The candidate decoder file was then frozen at Git blob `75207864d07573edf53fe29b321381e732347b91` before a separately generated held-out set was introduced. The held-out workflow verified that exact blob before execution.

The held-out result was:

- A3: 20/20 — PASS;
- B6: 17/20 — FAIL;
- C9: 20/20 — PASS.

All three B6 misses were true margin-repetition cases whose strongest valid lags were 130 or 138 px, above B6's frozen absolute upper lag bound of 120 px. The v1 periodic-texture false-positive failure did not recur. This isolates a different transport problem: the fixed absolute margin-lag range did not generalize across held-out scale.

Because the prospective gate required every decoder to score 20/20, `image-only-002.0-dev` is **blocked from historical use**. It will not be rerun on f113r. Any successor must receive a new version and a new future holdout; the failed held-out set cannot be used as the validation set for a decoder tuned from its failures.

See `docs/IMAGE-ONLY-V2-DEVELOPMENT.md`, `docs/IMAGE-ONLY-V2-HELDOUT.md`, `results/image-only-v2-development-001/`, and `results/image-only-v2-heldout-001/`.

## Initial falsification questions

- Does an apparent pattern survive changes in decoder assumptions?
- Can the result be reproduced from the same source observations?
- Does removing a source feature remove the claimed inference?
- Can a competing decoder generate an equally coherent but incompatible reading?
- Which parts of a reading are source-constrained, and which are supplied by the interpretive system?
- Does a claimed invariant survive deliberately adversarial decoder contexts?

## Voynich experiment

Voynich material is used here as a difficult test case because the manuscript supports many superficially plausible interpretations. That makes it useful for studying decoder behavior and false semantic convergence.

Any output in this repository should therefore be read as an **experimental candidate interpretation**, unless independently validated by evidence outside the decoder.

Historical source handling is governed by `docs/SOURCE-PROVENANCE.md`. The first historical fixture, `f113r`, has a frozen authority image; historical decoder runs must preserve declared representations, decoder provenance and frozen outputs before comparison.

## Status

Active experimental scaffold. Pilot 001 is frozen and passed. The historical comparison adapter is implemented and tested. The f113r authority image is frozen and independently re-verified. The first preregistered image-only historical run remains frozen with incompatible decoder readings. Both subsequent image-decoder generations have been prevented from further historical use by prospective synthetic gates: v1 failed known-answer calibration, while v2 passed development but failed its separately frozen held-out gate. No decipherment claim is made.

## Authorship

Research direction, conceptual framing, methodology, and original project work: Linda Thorstensen.
