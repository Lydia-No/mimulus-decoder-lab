# Historical input adapter

Status: bounded implementation support for Experiment 001.

Research direction, conceptual framing and methodology: Linda Thorstensen.

## Purpose

Pilot 001 uses a synthetic fixture with an independent answer key. Historical material does not have that privilege.

The historical adapter therefore reuses the same separation of source, representation, decoder output and meta-observation while preventing known-answer labels from leaking into the Voynich experiment.

## Gate

`historical/adapter.js` will not admit an evidence-bearing historical run unless:

1. the synthetic Pilot 001 gate remains frozen as passed;
2. the historical fixture has a frozen source-image record with a 64-character SHA-256;
3. the image extraction/region record is frozen;
4. any transcription supplied to a decoder has a declared convention, version and frozen hash.

The current f113r fixture intentionally fails this gate because exact source-image bytes have not yet been frozen.

## Historical run record

A decoder run must be frozen before comparison and must retain:

- unique run identifier;
- blinded decoder code and version;
- declared decoder assumptions;
- explicit claims;
- a stable claim key and target for each claim;
- proposition text;
- evidence locators with representation-layer provenance.

Evidence locators may point to `SOURCE_IMAGE`, `TRANSCRIPTION`, `PREPROCESSING` or `DERIVED_STRUCTURE`. A locator records where a decoder's support comes from; it does not make the claim true.

## Historical meta-observer labels

Because there is no independent Voynich answer key, the adapter uses only descriptive comparison labels:

- `CROSS_DECODER_RESIDUE`: all compared frozen decoders make the same proposition for the same claim key;
- `PARTIAL_CROSS_DECODER_RESIDUE`: more than one but not all decoders make the same proposition;
- `DECODER_SPECIFIC`: only one decoder makes the proposition;
- `INCOMPATIBLE_READINGS`: decoders attach incompatible propositions to the same claim key.

These labels describe persistence and conflict. They do not establish correctness.

## Forbidden inference

Historical comparison must not emit or imply the synthetic labels `SOURCE_SUPPORTED_INVARIANT` or `DECODER_DEPENDENT_SUPPORTED`, because those labels depend on an independent known answer.

Likewise, cross-decoder residue must not be promoted to `CORRECT_TRANSLATION`, `HISTORICAL_TRUTH`, decipherment, or linguistic identification solely from decoder agreement.

## f113r status

The f113r identity is anchored to the Yale/Beinecke folio object already registered in the fixture. Secondary descriptions remain in `reference-observations.json` and do not open the gate.

The next required source operation is to freeze exact f113r image bytes plus the extraction record. Only then may decoder inputs be generated from the historical adapter.

## Validation

`historical/test.js` tests both sides of the gate:

- the live f113r fixture remains blocked;
- a mock correctly frozen source opens the adapter;
- unanimous historical agreement is classified as residue rather than source truth;
- incompatible readings remain explicit;
- decoder-specific claims remain decoder-specific.

This adapter changes no ArcTopia theory or terminology. Its labels are local experimental bookkeeping.
