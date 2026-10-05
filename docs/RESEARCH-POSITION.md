# Research position — Mimulus as meta-observer

## Scope

Mimulus studies observer-conditioned representation.

Its primary object is not a particular manuscript, language, cipher, or decoder. It studies the relation among:

- a source;
- the representation supplied to an observer;
- the observer / decoder mechanism;
- the current interpretive context;
- retained prior state or history;
- the resulting structural and semantic output.

A compact abstraction is:

`R = f(S, D, C, H)`

The research task is to determine which properties of `R` remain attributable to `S` after `D`, `C`, and where relevant `H` are varied under controlled conditions.

## Central distinction

Mimulus distinguishes **persistence** from **independent persistence**.

An interpretation can survive many transformations because downstream systems preserve the semantics introduced upstream. This does not make the interpretation independently source-constrained.

Therefore:

`source → decoder A → output A → translator B → output B`

is one evidential lineage, not two independent source decoders.

Cross-decoder residue requires materially independent routes from the frozen source to the compared outputs, with shared preprocessing and shared priors accounted for explicitly.

## Two experimental regimes

### Static-source

Hold the source fixed and vary observer conditions.

Goal: identify structure that survives independent decoder variation and matched source interventions.

### History-bearing

Allow prior interactions to modify the observer state and test later output under reset, swap, identical-history and control conditions.

Goal: determine whether retained history causally alters later representation rather than merely increasing fluency or reusing prior semantics.

These regimes may inform one another but should remain separately testable.

## Voynich boundary

Voynich is an opaque-source stress test because it supports many plausible but incompatible interpretations.

It is not the identity of Mimulus and not a privileged theory target.

Voynich results should remain labelled as pilot/stress-test results unless a separate evidential chain justifies stronger claims.

## What counts as progress

Progress is not defined by producing increasingly convincing prose.

Useful progress includes:

- separating source observations from representation transforms;
- exposing decoder assumptions;
- distinguishing convergence from correctness;
- identifying shared-preprocessing dependence;
- detecting semantic relay and lineage dependence;
- showing preregistered sensitivity to matched ablation;
- recovering known-answer structure under blind conditions;
- obtaining `NO_RESIDUE` when no robust structure survives.

Negative results are valid outcomes.

## Near-term empirical gate

Before broad opaque-source claims, Mimulus should demonstrate both:

1. **known-answer discrimination** — correct recovery can be distinguished from shared wrong agreement on frozen synthetic material; and
2. **blind opaque-source analysis** — independently specified decoders can be compared on a frozen source with preregistered controls and without inherited semantic conclusions.

Only after those gates should semantic or historical interpretation be treated as a downstream research layer.

## Authorship boundary

Research direction, conceptual framing, methodology, and original project work are by Linda Thorstensen. Implementation assistance, synthesis, drafting, testing, and computational support do not imply co-authorship, co-invention, or shared ownership of the research concepts.
