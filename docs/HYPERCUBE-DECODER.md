# Hypercube decoder mode v1

The interactive workspace uses a Q4 decoder-context graph: 16 vertices, 32
undirected edges, and degree four at every vertex. A vertex is an explicit
combination of four binary interventions; an edge changes exactly one choice.
This follows the binary-state, one-axis-transition convention used by Symbolic
Cube Explorer. It does not import or modify that engine or claim canonical
ArcTopia dimensional semantics.

## Declared axes

1. Base mapping: A / B.
2. Mapping coverage: keep all / withhold the first observed symbol's mapping.
3. Target assignment: declared / cyclically rotate target values over sorted keys.
4. Symbol filter: all observed / repeated symbols only.

These axes are diagnostic interventions, not discovered dimensions. Operations
execute in the listed dependency order: choose A/B, rotate, withhold, then filter.
Rotation occurs before filtering. Different vertices may produce identical
effective mappings, particularly with small or incomplete codebooks.

## Fixed-source rule

Every vertex reads the same encoded observation and source identifier. The
original reference, when available, remains with the recovery evaluator. Source
ordering, encoding rules, and the reference do not change as the user traverses
the cube. This is a context comparison, not 16 independent model replications.

Known-original mode reports recovery for each vertex; opaque mode reports no
accuracy. Agreement and disagreement across an edge describe explicit mapping
claims. Neither graph proximity nor agreement establishes semantic truth.

## Interface and trace

The diagram is a two-dimensional projection of two connected Q3 cubes. Vertex
buttons select a context; axis buttons move to its one-bit neighbor. Each selected
vertex reveals assumptions, effective mappings, candidate output, uncertainty,
and recovery where available. Selecting a non-neighbor starts a new inspection
segment; it is not recorded as a one-axis transition.

Export includes the complete 16-context graph and a user inspection trace. The
trace is a navigation record, not a scientific causal history. Editing the source
or decoder rules invalidates the entire graph and its trace until another run.

Before scoring, the source identifier and ordered encoded tokens must match the
reference. A reused identifier alone cannot authorize scoring a different source.
Whitespace differences are allowed within the whitespace-token model.

Validation: all 69 tests passed. Tests cover graph size, unique edges, vertex
degree, one-axis adjacency, fixed-source identity, intervention order, recovery,
opaque-mode scoring, coincident contexts, and reference alignment. Browser checks verified axis
navigation, direct vertex selection, jump labeling, complete graph export, and
opaque-mode recovery unavailability.

## Integration with current main

This Python workspace is a local comparison instrument alongside the existing
Explorer and deterministic Pilot 001. It is not wired into the deployed Explorer
or the beQube state/intervention adapters. It does not execute image decoders,
change frozen historical results, or authorize the prospective held-out run.

Integration validation against main commit `f60c876`: 69 Python tests passed,
Pilot 001 assertions passed for all 12 cells, and the historical adapter checks
passed for 3 meta-observations. Existing main files were preserved unchanged.
