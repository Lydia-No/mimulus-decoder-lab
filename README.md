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

## Status

Early experimental scaffold. Interfaces, fixtures, and tests will be added incrementally. No decipherment claim is made.

## Authorship

Research direction, conceptual framing, methodology, and original project work: Linda Thorstensen.
