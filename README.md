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

The f113r source-image gate is now open. The full-folio JPEG was fetched directly from Yale's IIIF Image API, frozen at SHA-256 `ad748f9012b174be520b7ac837fdadf913e49a696323920ca655ecf5474afb5c`, and independently fetched again with the same hash. The image is 2582 × 3787 pixels and 2,092,549 bytes. Any transcription supplied to a decoder still requires its own declared convention, version and frozen hash.

See `docs/HISTORICAL-INPUT-ADAPTER.md` and `fixtures/voynich/f113r/authority-freeze.json`.

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

Historical source handling is governed by `docs/SOURCE-PROVENANCE.md`. The first historical fixture, `f113r`, now has a frozen authority image; historical decoder runs must still preserve declared representations, decoder provenance and frozen outputs before comparison.

## Status

Active experimental scaffold. Pilot 001 is frozen and passed. The historical comparison adapter is implemented and tested. The f113r authority image is frozen and independently re-verified, so image-only historical inputs can now pass the source gate. No decipherment claim is made.

## Authorship

Research direction, conceptual framing, methodology, and original project work: Linda Thorstensen.
