# f113v preregistered control plan

Status: **PRE-DECODER / FROZEN WITH FIXTURE**

These controls are defined before substantive decoder output is inspected. Their purpose is to distinguish source-sensitive structure from structure that a flexible decoder can recover regardless of the relevant source relation.

A control may be instantiated only from a frozen representation branch. The transform must be deterministic or fully recorded, and the controlled output must receive its own artifact id/hash where applicable.

## General rule

For every non-trivial claim, the decoder must identify in advance:

1. the source relation believed to support the claim;
2. the control below that should weaken or destroy that relation;
3. the predicted effect on the claim.

A claim that survives destruction of its alleged support is not strengthened by that survival. It becomes evidence that the decoder may be insensitive to the source feature it claimed to use.

## C0 — unchanged rerun

Purpose: baseline reproducibility.

Transform: none. Re-run the same decoder/version on the same frozen representation under the same declared settings where reproducibility is meaningful.

Expected use: distinguish unstable/stochastic output from source-sensitive output.

## C1 — manuscript-region mask control

Purpose: test claims attributed to a specific visible region or marker class.

Transform: mask the pre-identified source region supporting the claim while preserving the remaining geometry and dimensions as far as practical.

Prediction requirement: the decoder must state which claim should weaken or disappear.

Do not choose the masked region after inspecting the control result.

## C2 — within-line order permutation

Purpose: test claims requiring local sequential order.

Transform: preserve the candidate units present in each frozen line/sequence representation but permute their order using a recorded seed or deterministic permutation.

Preserves approximately:

- unit inventory;
- per-line counts;
- line membership.

Destroys:

- original within-line adjacency and order.

A claim about sequential structure should degrade if its evidence actually depends on sequence order.

## C3 — line / region order permutation

Purpose: test claims requiring higher-level order across lines or regions.

Transform: preserve each frozen line/region internally while permuting their order using a recorded seed or deterministic permutation.

Preserves local structure while disrupting higher-level progression.

## C4 — recurrence-preserving substitution

Purpose: test whether a decoder is responding to recurrence topology rather than identity-specific source distinctions.

Transform: relabel candidate units by a one-to-one neutral substitution that preserves the recurrence pattern exactly.

Preserves:

- equality/inequality relations;
- recurrence counts;
- relative positions.

Destroys:

- any information dependent on the visual identity of a candidate unit.

If a claim is intended to depend only on abstract recurrence, it may survive. If it is claimed to depend on specific glyph identities, it should not.

## C5 — recurrence-topology disruption

Purpose: test claims attributed to repeated configurations.

Transform: alter selected repeated candidate units or configurations so that the relevant recurrence relation is broken while preserving unrelated line length/layout as closely as possible.

Selection rule: the target recurrence must be identified in the claim's frozen prediction record before the intervention is instantiated.

## C6 — spatial-marker ablation

Purpose: test claims attributed to visible marginal/spatial markers independently of text-like marks.

Transform: remove/mask the selected class of spatial marks while leaving the central textual field unchanged as far as practical.

No functional name for the marks is assumed.

## C7 — segmentation-branch control

Purpose: detect dependence on preprocessing segmentation.

Transform: run the same decoder against at least one alternative segmentation branch that was defined and frozen before substantive decoder output, or against an earlier representation stage if the decoder permits it.

A result that exists only under one segmentation branch is `PREPROCESSING_DEPENDENT` unless additional evidence establishes otherwise.

## C8 — matched synthetic/null representation

Purpose: estimate how much apparently meaningful structure the decoder can manufacture from material with comparable superficial properties.

The synthetic/null input should be generated before inspecting the target decoder's substantive output and should preserve a declared subset of crude properties, such as:

- dimensions or line-count distribution;
- approximate mark density;
- candidate-unit frequency distribution or recurrence rate, when working at R3/R4;
- spatial density, when working at R1/R2.

It must not preserve the exact higher-order relations that the target claim is meant to detect.

The null generator and seed must be recorded.

## C9 — alternative explicit decoder

Purpose: test underdetermination rather than merely perturb the source.

Transform: none to the source. Instead apply a materially different, fully declared decoder capable of producing an incompatible account from the same frozen representation.

This control does not count as independent support merely because both decoders are coherent. Its purpose is to ask what source evidence discriminates between them.

## Control interpretation

The meta-observer should distinguish at least:

- **expected sensitivity** — claim changes as preregistered when alleged support is disrupted;
- **unexpected invariance** — claim survives a control that should have destroyed its support;
- **control fragility** — claim changes under a transform that should have been irrelevant;
- **preprocessing dependence** — result changes across frozen representation branches;
- **null recoverability** — comparable structure is recovered from a matched synthetic/null input;
- **untested** — no appropriate control was run.

Passing a control does not establish historical or semantic truth. It only provides evidence that a claim is sensitive to the source relation it says it uses.

## Freeze rule

The control families above are part of the fixture's pre-decoder specification. Specific instantiated controls may be added later only by recording the transform, parent representation, parameters/seed, and resulting artifact identity.

New control families proposed after seeing decoder output must be labelled `EXPLORATORY`.