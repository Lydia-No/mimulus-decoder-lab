# Possibility Machine v0

Status: synthetic known-answer sandbox. Non-canonical.

This experiment is the first concrete test of the possibility-machine idea from draft PR #24. It is intentionally tiny and fully inspectable before any external engine is introduced.

## Research question

Can multiple formal views preserve the difference between:

1. present state,
2. trajectory/history,
3. future reachability,
4. counterfactual intervention,

without collapsing them into one object?

The key known-answer condition is that two trajectories converge to the same present state while retaining different future possibilities.

## World

Four monotone binary factors define 16 raw cells:

`A B C D`

Initial state:

`0000`

Rules:

- `set_a`: A may become 1.
- `set_b`: B may become 1.
- `set_c`: C may become 1 only when A=1 and B=1.
- `set_d`: D may become 1 only when C=1 **and** `set_a` occurred before `set_b`.

The final rule is deliberately history-sensitive.

## Known answer

Only six present states are reachable:

```text
0000
0100
1000
1100
1110
1111
```

But there are eight reachable `(state, history)` nodes because two current states have convergent trajectories:

```text
0000
 ├─ set_a → 1000 ─ set_b → 1100 ─ set_c → 1110 ─ set_d → 1111
 └─ set_b → 0100 ─ set_a → 1100 ─ set_c → 1110
```

At `1110`, the present state is identical in both branches.

However:

- history `set_a → set_b → set_c` can still reach `1111`;
- history `set_b → set_a → set_c` cannot.

Therefore this fixture contains a direct known-answer witness for:

> identical present state does not imply identical future reachability.

## Four views

### 1. Forward / generative

Question:

> Given the initial state and rules, what states and trajectories are reachable?

Expected answer includes six unique current states and eight state-history nodes.

Candidate engines later: Wolfram Multiway, Maude.

### 2. Inverse / constraint

Question:

> Given observation `1110`, which histories are compatible with it?

Expected answer:

```text
set_a → set_b → set_c
set_b → set_a → set_c
```

The observation alone is insufficient to determine whether D remains reachable.

Candidate engines later: Alloy, SMT.

### 3. Intervention / counterfactual

Intervention:

> Remove the history-order condition from `set_d` while leaving the present-state requirement C=1 unchanged.

Expected result:

The `set_b → set_a → set_c` branch regains reachability to `1111`.

This tests whether the system records a changed transition condition rather than silently rewriting the prior history.

Candidate engine: beQube / ExperimentSpace.

### 4. Verification

Required invariants:

1. C=1 implies A=1 and B=1.
2. D=1 implies C=1.
3. `1111` is reachable only through a history where `set_a` precedes `set_b` under the baseline rules.
4. There exists at least one same-state pair with different future reachability.

Candidate engines later: TLA+/TLC, Lean, Maude or structural Wolfram checks.

## Mimulus role

Mimulus must not decide which engine is "right" by fluency or tool identity.

For this synthetic experiment it should compare records such as:

- current state recovered,
- compatible histories recovered,
- reachable-future set recovered,
- intervention effect recovered,
- invariant/counterexample results,
- provenance and execution lineage.

The experiment passes only if the different formal views preserve the known-answer distinctions rather than flattening them.

## Files

- `fixture.json` — frozen known-answer specification.
- `reference.py` — dependency-free forward enumerator and intervention reference implementation.
- `test_reference.py` — executable known-answer assertions.

Run locally from this directory with:

```bash
python reference.py
python -m unittest test_reference.py
```

## Boundary

This is not a model of Voynich, ArcTopia, FCP, or a real institution. It is not evidence that history-sensitive reachability is the correct ontology for any external domain. It is a deliberately constructed calibration object for testing whether the proposed machinery can distinguish state, path and possibility before transport to harder material.
