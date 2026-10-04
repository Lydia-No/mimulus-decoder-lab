# Experiment 001 — Voynich multi-decoder test

Status: protocol draft

## Purpose

Test whether apparently meaningful structure in a selected Voynich passage is constrained by the source or generated primarily by decoder assumptions.

This experiment does not begin with a decipherment hypothesis.

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

## Interpretation boundary

A successful run may establish that a decoder is reproducible, source-sensitive, predictive, or unusually invariant. None of those alone establishes that its semantic reading is the historical meaning of the Voynich Manuscript.
