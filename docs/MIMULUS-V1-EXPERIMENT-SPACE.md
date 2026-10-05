# Mimulus v1 experiment space and trajectory contract

Status: design-freeze candidate

This document restores an earlier Mimulus design constraint that is not fully captured by a flat list of Runs: interpretation ancestry, experimental adjacency, and trajectory are different structures and must remain separate.

It complements `MIMULUS-V1-ARCHITECTURE.md`, `MIMULUS-V1-SCHEMA.md`, and `MIMULUS-V1-ADAPTERS.md`.

## Three different relations

Mimulus must not collapse these into one graph.

### 1. LineageGraph — where did this output come from?

Examples:

`image -> transcription -> Sumerian-looking output -> English translation`

Lineage captures derivation, conditioning, translation, paraphrase, preprocessing ancestry, and semantic relay.

It answers provenance questions. It does not say what would have happened under another condition.

### 2. ExperimentSpace — what differs between comparable runs?

ExperimentSpace represents declared factors, their allowed levels, experimental cells, and explicit transitions between cells.

An edge normally means that one declared factor changed while the relevant remaining factors were held fixed.

It answers counterfactual/comparative questions such as:

- same source, different decoder
- same decoder, different context
- same context, different preprocessing branch
- same decoder/context, reset history
- same source support, targeted ablation

Experimental adjacency is not derivation and must not be represented as lineage.

### 3. Trajectory — what path was actually taken?

A trajectory records an ordered sequence of states/interventions/runs.

Two trajectories may end in the same apparent output while differing in path. This matters especially for history-bearing experiments, reconstructive effects, learning, memory, and path-dependent observer state.

A user navigation trace is not automatically a scientific trajectory. Navigation becomes experimental history only when the design explicitly makes it causally relevant.

## ExperimentSpace schema

```ts
export type FactorKind =
  | 'binary'
  | 'categorical'
  | 'ordinal'
  | 'continuous'
  | 'custom';

export type FactorTarget =
  | 'representation'
  | 'decoder'
  | 'context'
  | 'history'
  | 'execution'
  | 'intervention'
  | 'other';

export type FactorLevel = {
  id: string;
  label: string;
  valueRef?: string;
  value?: string | number | boolean | null;
};

export type ExperimentFactor = {
  id: string;
  label: string;
  kind: FactorKind;
  target: FactorTarget;
  levels: FactorLevel[];
  rationale?: string;
};

export type ExperimentCell = {
  id: string;
  assignments: Record<string, string>;
  plannedRunRef?: string;
  runRef?: string;
  status: 'planned' | 'executed' | 'excluded' | 'invalidated';
  exclusionReason?: string;
};

export type ExperimentTransition = {
  id: string;
  fromCellId: string;
  toCellId: string;
  factorId?: string;
  relation: 'one_factor_change' | 'multi_factor_jump' | 'ordered_step' | 'other';
  heldFixedFactorIds?: string[];
};

export type ExperimentSpace = {
  id: string;
  label?: string;
  sourceId: string;
  hypothesisId?: string;
  design:
    | 'full_factorial'
    | 'fractional_factorial'
    | 'matched_comparison'
    | 'ordered_path'
    | 'custom';
  factors: ExperimentFactor[];
  cells: ExperimentCell[];
  transitions: ExperimentTransition[];
  fixedConditionRefs?: string[];
  createdAt: string;
};
```

## Hypercube as a special case

A binary context hypercube is one valid ExperimentSpace, not the universal Mimulus ontology.

A Qn hypercube occurs when:

- there are `n` declared binary factors
- the design contains the full `2^n` factorial cell set
- two cells are adjacent when they differ on exactly one factor

The earlier Q4 Mimulus context experiment is therefore a concrete special case: 4 binary diagnostic axes, 16 cells, 32 one-factor edges, one fixed source.

Important boundaries from that work remain binding:

- axes are declared interventions, not discovered canonical dimensions
- vertices are experimental contexts, not automatically independent decoders
- two vertices may have identical effective behavior
- geometric proximity does not establish semantic similarity or truth
- agreement across vertices is not source evidence unless relevant dependencies are controlled

Mimulus may project a high-dimensional ExperimentSpace into a 2D or 3D visual interface, but projection geometry must never be treated as evidence.

## TestPlan relationship

`Test this hypothesis` should no longer be understood as merely emitting a flat list of planned runs.

Its durable output is an `ExperimentSpace` plus the minimum planned runs needed to populate the discriminating cells.

A TestPlan may still expose a flat `plannedRuns` view for convenience, but that view is derived from the ExperimentSpace.

The planner should prefer the smallest space that distinguishes the live alternatives. It must not generate a full factorial merely because all factors are available.

Examples:

- one decoder swap may require two cells and one edge
- decoder x context may require a 2x2 square
- four binary diagnostics may justify a Q4 hypercube
- history questions may require an ordered path rather than a factorial cube

## Trajectory schema

```ts
export type TrajectoryStep = {
  index: number;
  beforeStateRef?: string;
  interventionId?: string;
  experimentTransitionId?: string;
  runId?: string;
  afterStateRef?: string;
  occurredAt?: string;
};

export type Trajectory = {
  id: string;
  sourceId: string;
  experimentSpaceId?: string;
  initialStateRef?: string;
  steps: TrajectoryStep[];
  finalStateRef?: string;
  historyBearing: boolean;
  createdAt: string;
};
```

Rules:

- order is intrinsic to Trajectory
- Lineage does not substitute for trajectory order
- ExperimentSpace adjacency does not prove that a transition was actually traversed
- a visual inspection path is stored separately unless the experiment intentionally exposes that path as history
- editing a source, representation, decoder rule, or factor definition may invalidate affected cells/trajectories and must not silently preserve them as comparable

## beQube boundary

beQube is the structural engine that can instantiate, traverse, and record ExperimentSpaces and Trajectories.

It may manage:

- cell/state snapshots
- one-factor transitions
- jumps when explicitly requested
- before/intervention/after records
- reset and swap operations
- factorial and matched comparison designs
- ordered history-bearing paths

beQube does not decide:

- whether a factor is scientifically meaningful
- whether two decoders are evidentially independent
- whether a translation is true
- whether persistence counts as source-constrained residue

Those remain Mimulus-level research judgments.

## Meta Observer inputs

The Meta Observer should consume three separately queryable structures:

1. `LineageGraph` — ancestry and semantic relay
2. `ExperimentSpace` — declared contrasts and held-fixed conditions
3. `Trajectory` — ordered path where path matters

This separation allows Mimulus to distinguish, for example:

- inherited agreement through one translation lineage
- independent-looking outputs that differ only by prompt framing
- an effect that survives decoder changes but vanishes after history reset
- identical end states reached through different histories

## Green House interaction model

The user does not need to see the mathematical dimensionality unless useful.

A discovery can begin freely, for example:

`This looks botanical.`

`Test this hypothesis` may then construct a small ExperimentSpace and present human-scale moves such as:

- Same source, different decoder
- Same decoder, neutral framing
- Remove suspected motif
- Reset history
- Compare with a matched null

The interface can visualize a square, cube, hypercube projection, matrix, or path depending on the design. The underlying factor/transition record remains explicit.

The methodological burden belongs to Mimulus, not to the exploratory user.

## Required invariants

1. Lineage ancestry and experimental adjacency are different edge types in different structures.
2. A hypercube vertex is a condition/cell, not automatically an independent empirical replication.
3. A hypercube axis is declared, not discovered merely because the UI renders it.
4. One-factor adjacency must identify the factor changed and what was held fixed.
5. Multi-factor jumps must never be mislabeled as one-factor transitions.
6. A navigation trace is not causal history unless the experiment makes it causally operative.
7. Same end state does not imply same trajectory.
8. `NO_RESIDUE` remains valid across any ExperimentSpace geometry.
9. Full factorial expansion is optional; the planner should prefer discriminating minimality.
10. Tool/provider choice remains adapter-level and does not define the ExperimentSpace ontology.

## Implementation order amendment

The static-source v1 implementation order becomes:

1. Source + Representation
2. Decoder + Context + ExecutionAdapter / ReferenceAdapter
3. Run + LineageGraph
4. Hypothesis + TestPlan
5. ExperimentSpace generation with explicit factors/cells/transitions
6. Interpretation genealogy and experiment-space views
7. beQube execution of planned contrasts
8. known-answer synthetic validation
9. frozen opaque-source validation
10. Trajectory/history reset/swap only after static comparison works end to end

This restores the earlier Mimulus/Green House hypercube insight without making a binary hypercube the universal representation.