# Experiment 001 — Voynich multi-decoder test

Status: protocol draft

## Purpose

Test whether apparently meaningful structure in a selected Voynich passage is constrained by the source or generated primarily by decoder assumptions.

This experiment does not begin with a decipherment hypothesis.

## Source precedence

This experiment follows `docs/SOURCE-PROVENANCE.md`.

For evidence about what is visibly present, the manuscript image outranks any transcription, normalization, segmentation or decoder representation. A transcription is a declared representation of the source, not the source itself.

A fixture is not enabled for evidence-bearing runs until its source pointer, folio/region identity, extraction procedure and relevant provenance fields are frozen. Do not invent or backfill hashes that were not computed from acquired bytes.

Access-copy pagination is not source identity. Where an authoritative folio-level catalog pointer exists, use it to anchor the folio independently of a particular PDF's page numbering.

## Inputs

For each selected passage preserve separately:

1. source reference (folio/region);
2. image or authoritative source pointer where licensing permits;
3. transcription and transcription convention;
4. visual/layout observations not captured by transcription;
5. preprocessing decisions.

Do not silently normalize uncertain glyphs.

## Decoder runs

Run multiple decoder contexts without passing semantic conclusions between them. Candidate families may include:

- structural/symbolic analysis;
- operator or state-transition interpretation;
- linguistic hypotheses when explicitly specified;
- deliberately adversarial or null decoders;
- independent external decoder contexts.

The list is intentionally provisional. A decoder earns inclusion by having an explicit mapping and producing inspectable provenance, not by producing attractive prose.

## Output record

Each run should return:

- decoder identifier/version;
- declared assumptions;
- source observations used;
- intermediate representation, if any;
- candidate claims;
- provenance for each claim;
- uncertainty/alternatives;
- information unavailable to the decoder.

## Historical comparison semantics

The synthetic gate has an independent answer key; the historical Voynich experiment does not.

Therefore the known-answer labels used in Pilot 001, including `SOURCE_SUPPORTED_INVARIANT` and `DECODER_DEPENDENT_SUPPORTED`, are not available to the historical meta-observer.

Historical agreement is described only as persistence or conflict across frozen outputs:

- `CROSS_DECODER_RESIDUE`;
- `PARTIAL_CROSS_DECODER_RESIDUE`;
- `DECODER_SPECIFIC`;
- `INCOMPATIBLE_READINGS`.

These labels are local experimental bookkeeping, not theoretical terms. Agreement does not become correctness merely because multiple decoders produce it.

The executable gate and comparison rules are in `historical/adapter.js`; see `docs/HISTORICAL-INPUT-ADAPTER.md`.

## Meta-observer pass

Only after independent runs are frozen, compare them for:

- exact structural agreement;
- partial agreement;
- incompatible readings;
- shared dependence on the same preprocessing choice;
- apparent semantic convergence unsupported by shared source constraints;
- residue that survives decoder variation.

## Falsification tests

1. **Ablation:** remove or perturb a claimed source-bearing feature. Does the interpretation change as predicted?
2. **Alternative decoder:** can materially different assumptions produce equally coherent but incompatible semantics?
3. **Permutation/null:** does the decoder continue to find similar meaning after structure that should matter has been disrupted?
4. **Blind rerun:** can the result be reproduced without seeing the previous semantic output?
5. **Provenance audit:** can each important conclusion be traced to source evidence rather than an undeclared prior?
6. **Cross-passage prediction:** does a decoder make a constraint or prediction that can be tested on material it was not tuned on?

## First historical fixture

`fixtures/voynich/f113r/source.json` is the initial historical fixture. Its folio identity is anchored to the Beinecke/Yale catalog object for f113r rather than inferred from access-copy page numbering.

`fixtures/voynich/f113r/reference-observations.json` records secondary descriptive observations separately from direct image evidence. Those observations may be used to design perturbations, but they must be checked against frozen source-image bytes before they are scored as source evidence.

Synthetic known-answer material remains the required first validation stage for the measurement machinery. The historical run remains gated on both synthetic validation and a frozen f113r image/extraction record.

The historical adapter is now implemented, but the live f113r gate remains closed until exact source-image bytes and extraction provenance are frozen.

## Interpretation boundary

A successful run may establish that a decoder is reproducible, source-sensitive, predictive, or unusually invariant. None of those alone establishes that its semantic reading is the historical meaning of the Voynich Manuscript.
