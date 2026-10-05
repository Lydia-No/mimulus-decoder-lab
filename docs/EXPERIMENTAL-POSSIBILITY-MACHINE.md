# Experimental Possibility Machine

Status: sandbox / non-canonical

This note explores a cross-project computational idea for Mimulus and Cube/Hypercube. It is not part of Mimulus v1, does not define ArcTopia theory, and must not be used to infer canonical terminology.

## Prompt

Can we build a practical "thinking machine" that does more than answer questions: one that explicitly expands possibility space, generates alternative trajectories, finds hidden structures consistent with observations, supports controlled interventions, and checks selected invariants?

The key design choice is not to force all of these tasks into one formalism.

## Four modes of formal thinking

### 1. Generative / forward possibility

Question:

> Given this state and these transformation rules, what can happen?

Candidate engines:

- Wolfram Multiway systems
- Maude rewriting logic

Output:

- reachable states
- alternative branches
- trajectories
- causal/event structure
- convergence/divergence
- terminal or unreachable regions

This is the closest computational analogue to a "mental machine" that can be run before a concrete implementation is built.

### 2. Constraint / inverse possibility

Question:

> What structures could be true if these observations and constraints are true?

Candidate engines:

- Alloy
- SMT solvers such as cvc5

Output:

- satisfying structures
- counterexamples
- alternative relational configurations
- impossible combinations

This direction is especially relevant to Mimulus because it reverses the usual decoder flow. Instead of asking only "what does this source mean?", it can ask "what distinct hidden structures could generate or remain consistent with what we observe?"

### 3. Intervention / counterfactual possibility

Question:

> What changes if exactly one condition changes?

Primary engine:

- beQube / neutral Mimulus experiment-space machinery

Output:

- before/intervention/after records
- one-factor transitions
- reset/swap/ablation comparisons
- explicit trajectories through an ExperimentSpace

A binary Qn hypercube is one special case: n binary declared factors, 2^n cells, and one-factor adjacency.

### 4. Verification / necessity

Question:

> What must remain true, or where does a claimed invariant fail?

Candidate engines:

- TLA+/TLC for state-machine behavior and counterexamples
- Lean for selected proofs
- Maude model checking for rewrite systems
- Wolfram for independent structural checks

Output:

- invariant checks
- counterexample traces
- reachability claims
- selected proofs

## Mimulus role

Mimulus should not become any one of these engines.

Its distinctive role is meta-observation across them:

```text
source / initial state
        |
        +--> forward generator ----> possible trajectories
        |
        +--> constraint finder ----> possible structures
        |
        +--> intervention engine --> controlled alternatives
        |
        +--> verifier -------------> invariants / counterexamples
                                     |
                                     v
                                  Mimulus
                                     |
                                     v
                       what survived, and why?
```

Mimulus can compare:

- source dependence
- path dependence
- observer/decoder dependence
- preprocessing dependence
- inherited semantic lineage
- whether agreement is genuinely independent

## Two graphs remain distinct

### LineageGraph

Answers:

> Where did this representation or interpretation come from?

Tracks derivation, translation, paraphrase, supplied intermediate outputs, and semantic relay.

### ExperimentSpace

Answers:

> Which declared conditions differ between these runs?

Tracks factors, cells, held-fixed variables, and experimental adjacency.

Neither replaces Trajectory, which records ordered path when order/history matters.

## Why Maude is especially interesting

Maude is not just another graph library. Rewriting logic is explicitly a logic of change. A rule can be executable, alternative rules can generate different futures, and the same formalism supports search and model checking. Maude is also reflective: rules and representations can themselves become objects of computation.

That makes it a particularly strong sandbox candidate for the bridge between:

```text
state
-> transformation rule
-> alternative reachable states
-> trajectory
-> meta-analysis
```

This does not mean Maude should replace beQube. A useful experiment would be to encode the same tiny transition system independently in both systems and compare their generated reachability/adjacency records.

## Why Alloy is the surprising complement

Alloy asks a different question from a simulator. Given relational constraints, it finds structures satisfying them and can generate counterexamples to assertions.

For Mimulus this suggests an inverse mode:

```text
observed residues + constraints
              |
              v
      candidate structures
       /       |       \
      A        B        C
```

Rather than forcing an interpretation, the machine can expose multiple structurally valid explanations. This is potentially useful for deliberately resisting premature semantic convergence.

## First bounded experiment

Do not begin with Voynich or an ArcTopia case.

Use a synthetic known-answer system with:

- 4 binary declared factors
- 16 possible cells
- one-factor transitions
- at least one forbidden state
- at least one convergent pair of paths
- at least one path-sensitive condition

Then run four independent questions:

1. Forward: enumerate reachable trajectories.
2. Inverse: find all structures consistent with a partial observation.
3. Intervention: change one declared factor at a time.
4. Verification: test a known invariant and recover a counterexample when intentionally broken.

Success is not agreement between tools. Success is a traceable account of why outputs agree or disagree.

## Candidate implementation order

1. Maude: tiny forward/rewrite model.
2. Alloy: inverse constraint model of the same synthetic system.
3. beQube: equivalent intervention graph.
4. Mimulus: ingest all three result families with provenance and compare them.
5. Add one intentionally false invariant and ensure the verification layer returns a useful counterexample.
6. Only then consider a real opaque-source or ArcTopia-adjacent use case.

## Boundary

The following claims are explicitly not made:

- that Wolfram's Ruliad is the ontology of ArcTopia, Cube, or Mimulus;
- that formal possibility equals real-world possibility;
- that a satisfying model is evidence that the modeled interpretation is true;
- that multiple engines are independent evidence merely because they are different tools;
- that mathematical elegance establishes semantic correctness.

The experimental value is narrower: different formal systems can expose different aspects of a possibility space, while Mimulus preserves provenance and compares what survives across those views.
