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

The f113r source-image gate now satisfies conditions 1–3. The exact full-folio JPEG returned by Yale IIIF image id `1006270` is frozen at SHA-256 `ad748f9012b174be520b7ac837fdadf913e49a696323920ca655ecf5474afb5c`. A second authority retrieval matched that hash. Image-only inputs may therefore pass the historical gate; transcription-bearing inputs remain gated on their own transcription provenance.

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

The f113r identity is anchored to the Yale/Beinecke folio object and its source image is frozen separately in `fixtures/voynich/f113r/authority-freeze.json`.

Secondary descriptions remain in `reference-observations.json`. They do not become direct source evidence merely because the image gate is open; each such observation must still be verified against the frozen image before scoring.

## Validation

`historical/test.js` tests both provenance acceptance and comparison semantics:

- the live authority-frozen f113r image opens the image-only gate;
- malformed transcription provenance closes the gate;
- a properly frozen declared transcription preserves an open gate;
- unanimous historical agreement is classified as residue rather than source truth;
- incompatible readings remain explicit;
- decoder-specific claims remain decoder-specific.

The authority-fetch workflow also re-downloads the Yale image and fails if its bytes drift from the recorded hash. The first independent re-fetch matched the frozen hash and the historical adapter assertions passed.

This adapter changes no ArcTopia theory or terminology. Its labels are local experimental bookkeeping.
