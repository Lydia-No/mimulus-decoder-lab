# Mimulus v1: Wolfram verification/computation adapter

Status: bounded implementation note for the Mimulus v1 architecture freeze.

## Position

Wolfram is not a decoder and does not define Mimulus semantics.

Its role is an optional verification/computation adapter for ExperimentSpace and Trajectory structure.

It may be used to independently check mathematical properties of a declared experimental design or executed trajectory without promoting computational agreement into semantic truth.

## Appropriate responsibilities

A Wolfram-backed adapter may verify or compute:

- number of cells/states in a declared ExperimentSpace
- whether a claimed binary Qn design actually has 2^n cells
- adjacency under one-factor transitions
- vertex degree in full binary hypercubes
- connected components
- reachability
- shortest paths
- path length / diameter where meaningful
- state-space projections
- transition matrices
- admissibility masks supplied by the experiment definition
- irreversible or one-way regions when transitions are directed
- branching / multiway evolution
- trajectory comparison
- whether two trajectories reach the same terminal state through different paths
- graph invariants useful for detecting malformed experiment-space construction

## Explicit non-responsibilities

Wolfram must not decide:

- whether a decoder output is historically or linguistically true
- whether two decoders are evidentially independent
- whether a candidate interpretation is source-constrained
- whether a corpus attestation confirms a translation
- which axes are theoretically canonical
- whether a declared dimension corresponds to a real property of the world

Those remain Mimulus comparison/adjudication questions.

## ExperimentSpace boundary

A binary Qn hypercube is a special case only:

- n declared binary factors
- 2^n possible cells when fully instantiated
- edges connecting conditions differing on exactly one factor

Mimulus must not call an arbitrary finite state space a hypercube merely because it is visualized as one.

Higher-cardinality factors, sparse factorial designs, masked/admissible subsets, directed transitions, or incomplete experimental designs remain ExperimentSpaces but are not automatically Qn hypercubes.

## Verification pattern

Conceptually:

```text
TestPlan
  -> declared ExperimentSpace
  -> beQube instantiation/execution
  -> Trajectory / run records
  -> Wolfram verification adapter
  -> structural verification result
  -> Meta Observer
```

The Wolfram result is evidence about the mathematical structure of the experimental design or trajectory only.

Example:

```text
Claim: this design is a complete Q4 context hypercube.

Wolfram checks:
- 16 cells
- 32 unique undirected edges
- degree 4 at every vertex
- each edge changes exactly one declared binary factor

If true:
STRUCTURE_VERIFIED

This does not imply:
- the axes are the right axes
- the decoders are independent
- agreement has semantic meaning
```

## Relationship to earlier Mimulus Q4 work

The earlier decoder-context Q4 remains a useful test case because its expected graph properties are independently knowable.

It should be treated as a verification fixture for the ExperimentSpace machinery, not as a universal ontology for Mimulus.

## Adapter classification

Recommended classification:

```ts
kind: 'verification_computation'
executionMode: 'external_tool' | 'remote_compute' | 'manual_handoff'
```

A later implementation may expose Wolfram through a connected computational tool, exported notebook/script, or manual verification workflow. The core architecture must not depend on any one access method.

## Evidence label

Structural verification should be stored separately from semantic/evidential classes.

Suggested bounded result states:

- `STRUCTURE_VERIFIED`
- `STRUCTURE_MISMATCH`
- `PARTIALLY_VERIFIED`
- `NOT_CHECKED`

These labels describe computational checks only and must never be promoted automatically into `SOURCE_CONSTRAINED_RESIDUE` or any semantic result class.
