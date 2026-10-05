# Frozen fixture — f113v

Status: **SOURCE-LOCK / PRE-DECODER**

This fixture instantiates `docs/EXPERIMENT-001-VOYNICH.md` on one fixed source. It is not a decipherment record and does not import an external Voynich theory into the experiment.

## Fixture identity

- fixture id: `voynich-f113v-001`
- external identifier: `f113v` — metadata only; the identifier carries no semantic assumptions into decoder runs
- raw input: user-supplied screenshot
- raw filename: `4C485E75-FE73-453E-BFC6-D8CEDBA1656B.jpeg`
- raw dimensions: `1536 x 1151`
- SHA-256: `bccf2e0fdf11d6040ab87d55701eb23e2b6effc9e4ea5ad24c4aaf9e8a27f1c1`

The raw screenshot is the locked source for this experiment. It includes interface framing around the manuscript image. Any crop, rotation, contrast change, transcription, segmentation, or normalization is a **derived representation** and must be versioned with its transformation recorded.

## Contamination boundary

Before the independent decoder runs are frozen, do not encode the following as source facts:

- a proposed language;
- a proposed plaintext or translation;
- a proposed manuscript purpose or genre;
- historical interpretations of this folio;
- claims imported from Voynich scholarship about paragraph grammar, positional morphology, recipes, stars, gallows, or token meaning;
- conclusions from another Mimulus decoder run.

Such material may later be introduced as an explicitly labelled **external prior** in a separate decoder context. It must never be silently merged into the observation layer.

## Observation layer

The observation pass may record only features recoverable from the locked source or a declared derived representation. Examples include:

- visible spatial marks and their coordinates;
- line and region boundaries;
- repeated visual glyph sequences;
- exact or approximate recurrence relations;
- local adjacency and position;
- uncertainty where a glyph or boundary cannot be distinguished reliably.

Do not name a feature by presumed function. For example, record `left-margin marker` rather than `entry marker`; record `repeated glyph sequence G17` rather than a lexical gloss.

No transcription is authoritative merely because it is convenient. If a transcription is introduced, record its convention, source, uncertainty, and the mapping back to the source image.

## Initial decoder set

The first pass is deliberately narrow. It should test the Mimulus mechanism before attempting semantic translation.

### D0 — null / recurrence baseline

Uses counts, positions, adjacency, recurrence and simple permutation controls only. Produces no semantic reading.

### D1 — layout / segmentation decoder

May infer candidate grouping or boundary structure from spatial organization only. It may not use token meaning, historical claims, or another decoder's segmentation.

### D2 — symbolic relation decoder

May infer relations among recurring glyph sequences and positions. It may assign neutral identifiers or operators but no natural-language meanings.

### D3 — state / transformation decoder

May test whether the sequence is parsimoniously represented as transformations over a state. Any state variables and operators are decoder-supplied and must be exposed explicitly.

### D4 — adversarial/null competitor

Attempts to reproduce apparent regularity after permutations or using an alternative equally explicit rule set. Its purpose is to identify structure that a flexible decoder could manufacture.

A natural-language or historical decoder is **not** part of the first pass. It may be added only after the source/structure pass is frozen, so semantic fluency cannot steer what the experiment decides is structurally present.

## Independence rule for this fixture

Each decoder receives:

1. the same locked source or the same explicitly versioned derived representation;
2. its own declared decoder context;
3. no candidate conclusions from the other decoders.

Runs are frozen before the meta-observer compares them.

## Meta-observer labels

The meta-observer may emit only the following evidence-status labels initially:

- `SOURCE_CONSTRAINED_RESIDUE` — survives materially different decoder contexts and can be traced to source features;
- `DECODER_DEPENDENT` — changes or disappears when decoder assumptions change;
- `PREPROCESSING_DEPENDENT` — depends on crop, transcription, segmentation, normalization or another shared transform;
- `UNDERDETERMINED` — multiple incompatible readings remain equally supported;
- `CONTAMINATED` — a run used knowledge it was not supposed to receive;
- `NO_RESIDUE` — no non-trivial cross-decoder result survives.

`SOURCE_CONSTRAINED_RESIDUE` is not equivalent to historical meaning or decipherment.

## Required interventions

Any candidate residue should be challenged by at least one intervention matched to the claimed source support:

- remove or mask the feature claimed to carry the result;
- alter the relevant order while preserving unrelated visual properties;
- substitute a repeated sequence with a controlled alternative;
- reset a shared preprocessing decision;
- run an adversarial decoder that can generate a coherent incompatible account.

A claimed source relation should weaken or disappear when its supporting source relation is destroyed. If it does not, treat the claim as decoder-generated until shown otherwise.

## First question

Do materially different non-semantic decoders recover any of the same structural distinctions from this exact source, and do those distinctions survive matched ablation?

That question is intentionally narrower than `What does f113v say?`.

## Freeze condition

This file fixes the experimental boundary, not the result. Any later addition of observations, transcription, decoder output, semantic hypotheses, or external scholarship must be added as a new versioned artifact rather than rewritten into this source-lock record.
