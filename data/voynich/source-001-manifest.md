# Source 001 manifest

Experiment: 001 — Voynich multi-decoder test
Source ID: `voynich-f1r-rf1a`
Folio: `f1r`
Transliteration: Reference Transliteration `RF1a-n`, IVTFF 2.0 / EVA
Selection date: 2026-10-05

## Selection rule

Source 001 is the first manuscript folio represented in the published Reference Transliteration. This deterministic rule was chosen before examining the folio for semantic content and without reference to any proposed Hawaiian, Gaelic, Sumerian, or other translation.

This is preferable to selecting a visually or semantically suggestive page after inspection.

## Source channels

### Symbolic channel

The frozen IVTFF/EVA record is stored in `source-001-f1r.ivtff.txt`. IVTFF locus identifiers, punctuation, uncertain-space markers, uncertain glyph markers, and text-type metadata are retained rather than silently normalized.

### Visual channel

The manuscript image is treated as a separate source channel. Visual/layout observations must be recorded independently and must identify the folio. They must not be inferred from EVA transliteration alone.

The user supplied an Internet Archive scan of the Voynich Manuscript. The experiment may use that scan for visual inspection, while the symbolic channel uses the published Reference Transliteration.

## Contamination boundary

Before independent decoder runs are frozen, do not use:

- Mimulus/The Green House's candidate translations;
- semantic guesses derived from those translations;
- a preferred historical-language hypothesis;
- a mapping selected because it yields coherent prose.

After independent runs are frozen, external candidate translations may be registered as separate decoder outputs and compared by the meta-observer.

## First-pass allowed analyses

Source-only analyses may examine features such as:

- line/locus structure;
- token counts and repeated tokens;
- character and token frequency;
- token-position patterns;
- prefixes/suffixes under explicitly declared tokenization;
- local repetition and adjacency;
- uncertainty markers;
- differences between running text and labels/text types where metadata supports the comparison.

These analyses must not be described as translation.

## Evidence ladder

For Experiment 001, treat evidence roughly in increasing strength:

1. fluent/plausible semantic output;
2. reproducible pattern under one decoder;
3. structural residue across materially different decoders;
4. explicit stable source-to-function mapping;
5. successful prediction on held-out material not used to tune the mapping;
6. independent corroboration external to the decoder.

No level automatically proves historical meaning.
