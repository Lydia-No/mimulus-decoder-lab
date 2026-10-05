# Mimulus v1 architecture

Status: design freeze candidate

## Position

Mimulus is an experimental meta-observer for studying what is source-constrained, what is introduced by a decoder/observer, and what persists under independently varied interpretive conditions.

Voynich is a pilot / stress test, not the identity of the project.

The current Explorer remains a prototype surface. Mimulus v1 is organized around three primary research objects:

- `Source`
- `Run`
- `Lineage`

beQube is used as the state/intervention/trajectory engine inside Mimulus. It does not decide meaning and it is not a decoder.

## Core model

A run can be represented abstractly as:

`R_t = f(S, P, D, C, H_t, I)`

where:

- `S` = source
- `P` = preprocessing / representation state
- `D` = decoder / observer mechanism
- `C` = current context / assumptions
- `H_t` = retained history at time t
- `I` = intervention applied for this run
- `R_t` = resulting representation / interpretation record

The experimental question is not only what `R_t` says, but which properties of `R_t` remain attributable to `S` when `P`, `D`, `C`, `H`, or `I` are changed independently.

## Primary objects

### Source

A source is the observed object plus its representation lineage.

Examples:

- original image
- frozen crop
- mark-level representation
- glyph segmentation
- EVA or other transcription

Each representation must preserve provenance to its parent representation.

The source model must support explicit alternative branches when preprocessing is ambiguous.

### Run

A run records one observer interaction with a source or derived representation.

Minimum fields:

- source id
- representation id
- decoder id
- context id
- history-state id
- intervention id
- model/tool identity where applicable
- prompt/instructions where applicable
- output
- timestamps
- parent run(s), if derived
- evidence classification

A run may produce observations, structures, hypotheses, or downstream transformations. None of these become independent evidence merely by being fluent or coherent.

### Lineage

Lineage records how one output descends from another.

Example:

`Voynich image -> Sumerian-looking decoder output -> English translation -> Aymara translation`

This is one lineage, not four independent confirmations.

Lineage must make semantic relay visually and computationally explicit.

## beQube role

beQube manages controlled state and intervention mechanics.

It is responsible for:

- state snapshots
- before / intervention / after records
- decoder swap
- context swap
- history reset
- history swap
- preprocessing swap
- crop / segmentation variants
- targeted ablation
- permutation controls
- recurrence-preserving substitutions
- matched null representations
- known-answer synthetic controls

beQube should remain structurally neutral. It should not infer canonical Mimulus semantics from its implementation structure.

## Five working surfaces

### 1. Explore

Purpose: unrestricted discovery without pretending discovery is evidence.

Capabilities:

- image upload
- pasted transcription or intermediate representation
- free-form questions
- bounded language hypotheses
- symbolic / operator hypotheses
- structural observations
- user-created hypotheses

A useful idea can be promoted into a controlled experiment with `Test this hypothesis`.

### 2. Source Lab

Purpose: freeze and inspect the source before decoder contamination.

Supports:

- original source
- region selection
- mark-level representation
- candidate glyph segmentation
- candidate transcription
- alternative preprocessing branches
- source hashes
- explicit representation ancestry

The existing f113v R0-R4 lineage is the first concrete pattern for this surface.

### 3. Decoder Lab

Purpose: define and compare observer families.

Possible decoder families:

- recurrence/statistical
- layout/spatial
- linguistic
- symbolic relation
- state/transformation
- historical-language hypothesis
- adversarial competitor
- null decoder
- user-defined decoder

Different prompts to the same model are not automatically independent decoders. Effective decoder dependence must be represented explicitly.

### 4. beQube

Purpose: turn hypotheses into interventions.

A user should be able to take a discovery-phase idea and request a controlled experiment without manually designing every control.

Example interventions:

- hold source fixed, vary decoder
- hold decoder fixed, reset history
- swap histories between decoders
- hold interpretation fixed, perturb source support
- destroy recurrence while preserving superficial layout
- preserve recurrence topology while substituting symbols
- compare original source against matched nulls

### 5. Meta Observer

Purpose: compare runs and classify what persists.

The Meta Observer does not decide that a translation is true. It asks what survives and what that survival is attributable to.

Candidate result classes include:

- `SOURCE_CONSTRAINED_RESIDUE`
- `DECODER_DEPENDENT`
- `PREPROCESSING_DEPENDENT`
- `HISTORY_DEPENDENT`
- `SEMANTIC_RELAY`
- `UNDERDETERMINED`
- `CONTAMINATED`
- `NO_RESIDUE`

`NO_RESIDUE` is a full-validity result, not a failure of the system.

## Interpretation genealogy

Mimulus should expose a graph of interpretive descent.

Example:

```text
Voynich region
  |
  +-- Decoder A
  |     +-- Sumerian-looking output
  |            +-- English translation
  |                   +-- Aymara translation
  |
  +-- Decoder B
  |     +-- astronomical structure
  |
  +-- Decoder C
        +-- recurrence structure
```

This view should make it immediately visible when apparent agreement is inherited through a single lineage rather than independently recovered.

## Static-source and history-bearing regimes

These must remain distinct.

### Static-source regime

`source -> decoder/context -> representation -> comparison`

Question: what changes when the observer changes while source and history are controlled?

### History-bearing regime

`source -> interaction -> changed observer/history state -> later interaction -> changed representation`

Question: does prior interaction alter later observation or interpretation in a reproducible and intervention-sensitive way?

History must not be invoked as an explanation for static decoder divergence unless reset/swap controls support that claim.

## History experiments

Required interventions:

### Reset

Compare:

`source X -> decoder A + H1 -> output`

against:

`source X -> decoder A + RESET -> output`

### Swap

Compare:

- decoder A + history from B
- decoder B + history from A

If output follows history rather than decoder identity, that becomes a candidate history-dependent effect.

### Known-answer controls

History effects must first be validated on systems where correctness is independently knowable.

A history-bearing model becoming more fluent does not by itself show that history contributed source information.

## `Test this hypothesis`

This is a central v1 interaction.

A discovery-phase idea should be promotable into a test plan.

Mimulus should automatically propose a minimal set of competing runs covering:

- same-source rerun
- decoder variation
- context variation
- reset where history may matter
- relevant source ablation
- matched null / permutation
- alternative preprocessing where ambiguity is material

The system should show which claim each intervention is intended to distinguish.

## Evidence rule

Cross-decoder persistence counts as candidate residue only when the relevant decoder conditions are sufficiently independent for the claim being tested.

A downstream translation, paraphrase, or elaboration of a previous decoder output is lineage-dependent and cannot count as independent corroboration of the source.

A claim surviving an intervention that destroys its alleged source support is evidence against source sensitivity, not evidence for robustness.

## Product boundary

Mimulus v1 should feel permissive during discovery and strict during evaluation.

The user should be allowed to be speculative.

The system should carry the methodological discipline around the speculation by preserving provenance, generating controls, and preventing derived agreement from masquerading as independent evidence.

## Immediate implementation order

1. Freeze v1 schemas for `Source`, `Run`, `Lineage`, `Decoder`, `HistoryState`, and `Intervention`.
2. Preserve current Explorer as `Explore` surface rather than evolving it into the whole system.
3. Implement lineage graph / interpretation genealogy.
4. Implement `Test this hypothesis` to emit a run plan without executing it.
5. Connect run planning to beQube state/intervention records.
6. Execute a known-answer synthetic experiment with independent scoring.
7. Execute one frozen opaque-source experiment using the f113v fixture.
8. Add history reset/swap experiments only after static-source controls are working.

## Non-goals for v1

- claiming Voynich decipherment
- ranking interpretations by fluency alone
- treating multiple translations in one lineage as independent agreement
- importing ArcTopia normative semantics into Mimulus
- training a bespoke model before the experimental object and data model are understood

## Success condition

Mimulus v1 succeeds when a user can begin with an unconstrained interpretation, promote it into a controlled comparison, and receive a traceable account of:

- what came from the source
- what depended on preprocessing
- what depended on decoder assumptions
- what depended on history
- what was inherited through lineage
- what survived relevant controls
- and when nothing survives at all
