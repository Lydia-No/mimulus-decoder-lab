# Mimulus v1 core schema

Status: design freeze candidate

This document defines the minimum stable research objects for Mimulus v1. These schemas are intentionally smaller than the full product model.

## Design rule

Mimulus should preserve provenance and experimental separability before adding convenience fields.

A field belongs in a core object only if it helps answer one of these questions:

- what was observed?
- what representation was used?
- which observer/decoder acted?
- under what context and history?
- what intervention changed?
- what output was produced?
- what lineage does that output belong to?

## Common identifiers

All persistent objects use opaque stable IDs.

Recommended prefixes:

- `src_` source
- `rep_` representation
- `dec_` decoder
- `ctx_` context
- `hst_` history state
- `int_` intervention
- `run_` run
- `lin_` lineage edge

IDs are identity only. They must not encode semantics.

## Source

A Source is the observed object at the top of a representation tree.

```ts
export type Source = {
  id: string;
  label?: string;
  mediaType: 'image' | 'text' | 'sequence' | 'synthetic' | 'other';
  artifactRef: string;
  sha256?: string;
  createdAt: string;
  notes?: string;
};
```

Rules:

- `artifactRef` points to the preserved source artifact or fixture record.
- source identity must not silently change when a crop or transcription changes.
- transformations of a source create Representations, not new Sources, unless the research object itself is genuinely different.

## Representation

A Representation is a derived view of a Source or another Representation.

```ts
export type Representation = {
  id: string;
  sourceId: string;
  parentRepresentationId?: string;
  kind:
    | 'original'
    | 'crop'
    | 'region'
    | 'mark_level'
    | 'glyph_segmentation'
    | 'transcription'
    | 'layout'
    | 'synthetic_variant'
    | 'other';
  artifactRef: string;
  sha256?: string;
  method?: string;
  assumptions?: string[];
  createdAt: string;
};
```

Rules:

- every Representation retains ancestry to the Source.
- ambiguous preprocessing should fork the tree rather than overwrite a prior representation.
- a transcription is a representation, not ground truth.

## Decoder

A Decoder describes an observer mechanism sufficiently to reproduce its role in a run.

```ts
export type Decoder = {
  id: string;
  label: string;
  family:
    | 'null'
    | 'recurrence'
    | 'layout'
    | 'linguistic'
    | 'symbolic_relation'
    | 'state_transformation'
    | 'historical_language'
    | 'adversarial'
    | 'user_defined'
    | 'other';
  implementation?: string;
  model?: string;
  version?: string;
  instructionsRef?: string;
  declaredAssumptions?: string[];
};
```

Rules:

- decoder identity is not equivalent to model identity.
- two prompts to one model may be distinct decoder contexts without being independent decoder families.
- independence is a claim tested at comparison time, not a boolean property permanently stored on the decoder.

## Context

Context captures run-local assumptions that are not part of Decoder identity or Source representation.

```ts
export type Context = {
  id: string;
  languageTarget?: string;
  framing?: string;
  promptRef?: string;
  suppliedHypotheses?: string[];
  suppliedIntermediateOutputs?: string[];
  priorExposureRefs?: string[];
};
```

Rules:

- if a Sumerian-looking intermediate output is supplied to a later run, that dependency must be recorded here and in Lineage.
- prior conversation or decoder outputs that can influence a run belong in context/history rather than disappearing into prose.

## HistoryState

HistoryState is a snapshot of retained observer experience relevant to later runs.

```ts
export type HistoryState = {
  id: string;
  decoderId: string;
  parentHistoryStateId?: string;
  eventRefs: string[];
  stateRef?: string;
  resetFrom?: string;
  createdAt: string;
};
```

Rules:

- `HistoryState` does not claim that a model has a human-like memory.
- it records whatever retained state the experiment deliberately exposes or simulates.
- reset and swap operations must produce explicit new states or explicit `none` conditions.

## Intervention

An Intervention records what was deliberately changed for a run.

```ts
export type Intervention = {
  id: string;
  type:
    | 'none'
    | 'decoder_swap'
    | 'context_swap'
    | 'history_reset'
    | 'history_swap'
    | 'representation_swap'
    | 'crop_change'
    | 'segmentation_change'
    | 'ablation'
    | 'permutation'
    | 'recurrence_preserving_substitution'
    | 'recurrence_disruption'
    | 'matched_null'
    | 'other';
  targetRef?: string;
  parameters?: Record<string, string | number | boolean | null>;
  rationale?: string;
  claimTested?: string;
};
```

Rules:

- interventions describe experimental manipulations, not results.
- each nontrivial intervention should state what claim it is intended to distinguish where possible.

## Run

A Run is the central experimental record.

```ts
export type EvidenceClass =
  | 'DIRECT_OBSERVATION'
  | 'EXPLORATORY_DECODER_OUTPUT'
  | 'SOURCE_CONSTRAINED_RESIDUE'
  | 'DECODER_DEPENDENT'
  | 'PREPROCESSING_DEPENDENT'
  | 'HISTORY_DEPENDENT'
  | 'SEMANTIC_RELAY'
  | 'UNDERDETERMINED'
  | 'CONTAMINATED'
  | 'NO_RESIDUE';

export type Run = {
  id: string;
  sourceId: string;
  representationId: string;
  decoderId: string;
  contextId?: string;
  historyStateId?: string;
  interventionId?: string;
  parentRunIds?: string[];
  inputRef: string;
  outputRef: string;
  evidenceClass: EvidenceClass;
  startedAt: string;
  completedAt?: string;
  deterministic?: boolean;
  seed?: string | number;
  notes?: string;
};
```

Rules:

- exploratory model output defaults to `EXPLORATORY_DECODER_OUTPUT`.
- `SOURCE_CONSTRAINED_RESIDUE` should not be assigned by a single run in isolation; it is normally a comparison-level result.
- a downstream translation remains a Run, but its parent run must be explicit.
- `NO_RESIDUE` is valid and preserved.

## LineageEdge

Lineage is represented as directed edges between Sources, Representations, and Runs.

```ts
export type LineageEdge = {
  id: string;
  fromRef: string;
  toRef: string;
  relation:
    | 'derived_from'
    | 'cropped_from'
    | 'segmented_from'
    | 'transcribed_from'
    | 'translated_from'
    | 'paraphrased_from'
    | 'conditioned_on'
    | 'history_from'
    | 'control_of'
    | 'compared_with'
    | 'other';
  createdAt: string;
};
```

Rules:

- lineage must be acyclic for derivation relations.
- comparison edges may connect independent branches but do not imply derivation.
- semantic relay is detectable from lineage patterns such as `translated_from` / `paraphrased_from` chains.

## ComparisonResult

ComparisonResult is intentionally separate from Run.

```ts
export type ComparisonResult = {
  id: string;
  runIds: string[];
  claim?: string;
  varyingFactors: Array<'representation' | 'decoder' | 'context' | 'history' | 'intervention'>;
  heldFixed: string[];
  outcome:
    | 'SOURCE_CONSTRAINED_RESIDUE'
    | 'DECODER_DEPENDENT'
    | 'PREPROCESSING_DEPENDENT'
    | 'HISTORY_DEPENDENT'
    | 'SEMANTIC_RELAY'
    | 'UNDERDETERMINED'
    | 'CONTAMINATED'
    | 'NO_RESIDUE';
  basisRefs: string[];
  notes?: string;
};
```

This prevents a single fluent decoder output from promoting itself to a cross-run evidential conclusion.

## Hypothesis

A Hypothesis is a first-class exploratory object because v1 should allow users to speculate freely and then promote speculation into a test.

```ts
export type Hypothesis = {
  id: string;
  label: string;
  claim: string;
  createdFromRunId?: string;
  sourceSupportRefs?: string[];
  assumptions?: string[];
  status: 'exploratory' | 'planned_test' | 'tested' | 'retired';
};
```

## TestPlan

`Test this hypothesis` produces a TestPlan before any execution.

```ts
export type PlannedRun = {
  label: string;
  representationId: string;
  decoderId: string;
  contextId?: string;
  historyStateId?: string;
  interventionId?: string;
  purpose: string;
};

export type TestPlan = {
  id: string;
  hypothesisId: string;
  baselineRunId?: string;
  plannedRuns: PlannedRun[];
  discriminatingQuestions: string[];
  stopConditions?: string[];
  createdAt: string;
};
```

Minimum generated plan should consider, where relevant:

1. unchanged rerun
2. alternative decoder
3. alternative context
4. history reset
5. source-support ablation
6. matched null or permutation
7. alternative preprocessing branch

Not every hypothesis needs all seven. The planner should choose the smallest set that can distinguish the live alternatives.

## beQube boundary

beQube should consume and emit structural records only.

Conceptually:

```ts
export type BeQubeTransition = {
  beforeStateRef: string;
  interventionId: string;
  afterStateRef: string;
};
```

beQube must not be responsible for:

- deciding historical truth
- deciding semantic correctness
- deciding that two decoders are independent
- upgrading an exploratory output into residue

Those belong to Mimulus comparison logic and explicit adjudication.

## Required invariants

1. No Run without a Source and Representation.
2. No derived output without lineage to its parent input/run.
3. No hidden overwriting of preprocessing variants.
4. No translation chain counted as independent decoder agreement.
5. No history effect without explicit history condition.
6. No `SOURCE_CONSTRAINED_RESIDUE` from fluency/coherence alone.
7. `NO_RESIDUE` must remain representable at every comparison layer.
8. A source-support-destroying intervention that preserves a claim cannot strengthen source attribution.

## First implementation slice

The first v1 implementation should support only:

- Source
- Representation
- Decoder
- Context
- Run
- LineageEdge
- Hypothesis
- TestPlan

HistoryState, Intervention execution, and ComparisonResult can be added after the static-source workflow is working end to end.

This ordering is deliberate: history must not complicate the basic provenance problem before source/decoder/lineage separation works reliably.
