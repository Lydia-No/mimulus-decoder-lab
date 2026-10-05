# Mimulus

Experimental framework for studying observer-conditioned representation: which structures are constrained by a source, which are introduced by a decoder or observer, and which persist when interpretive conditions are varied independently.

Mimulus is not primarily a Voynich decoder and does not treat fluent interpretation as evidence of decipherment. The decoder lab is one implementation domain inside a broader meta-observer research program.

## Core research question

Given a fixed source, what changes when the observer changes — and what remains attributable to the source after decoder assumptions, preprocessing choices, context, retained history, and downstream semantic relay are separated and tested?

A useful abstract model is:

`R = f(S, D, C, H)`

where:

- `S` = source or frozen source representation;
- `D` = decoder / observer mechanism;
- `C` = current context, assumptions, preprocessing and prompt conditions;
- `H` = retained history or prior interaction state;
- `R` = resulting representation or interpretation.

Mimulus does not assume that every experiment needs all four variables. Static-source experiments may hold `H` fixed or absent; history-bearing experiments intervene on it explicitly.

## What the project separates

A candidate interpretation remains decomposable into:

1. **source observation** — what is directly represented in the declared input;
2. **preprocessing / representation transform** — crop, segmentation, transcription, normalization, tokenization or other derived representation;
3. **decoder assumptions** — mappings, grammars, priors, operators or inference procedures supplied by the observer;
4. **derived structure** — consequences of applying those assumptions;
5. **semantic interpretation** — meaning assigned downstream;
6. **cross-decoder residue** — structure that survives materially different decoder contexts;
7. **lineage dependence** — structure inherited from an upstream decoder output rather than recovered independently from the original source.

Cross-decoder residue is interesting only when it cannot be explained by shared preprocessing, shared priors, copied semantic conclusions, or a downstream translation relay. It is not automatically historical or linguistic truth.

## Independence requirement

Survival through transformation is not sufficient evidence.

A translation or transformation of a previous decoder output is not an independent decoder of the original source. For two outputs to contribute independent evidence about a source, each must receive the original frozen source (or an independently frozen source representation), its own declared decoder context, and no semantic conclusions from the other run before freeze.

The project therefore distinguishes:

`source → decoder A → output A`

from

`source → decoder A → output A → translator B → output B`

The second chain may preserve semantics faithfully while contributing no additional independent source evidence.

## Experimental regimes

### 1. Static-source regime

`source → decoder context → representation → comparison`

Question: what changes when the observer changes while the source remains fixed?

Typical interventions include decoder substitution, preprocessing branches, permutation, ablation, null inputs and adversarial alternative decoders.

### 2. History-bearing regime

`source → interaction → changed observer state → later interaction → changed representation`

Question: does prior interaction alter later interpretation in a reproducible, intervention-sensitive way?

History must be tested with controls such as reset, swap, identical-history conditions and known-answer fixtures so apparent improvement or semantic fluency is not mistaken for retained source information.

The two regimes are related but should not be collapsed. Observer history is a candidate causal variable, not a default explanation for decoder disagreement.

## Current implementation domains

### Decoder Lab

Executable and protocol work for comparing explicit decoder contexts, testing provenance, separating agreement from correctness, and measuring cross-decoder persistence.

### Voynich stress test

The Voynich Manuscript is an adversarial opaque-source test case because it supports many superficially plausible interpretations. It is a pilot / stress test, not the identity of Mimulus and not a claimed decipherment.

### PolyTranslator

Controlled multi-decoder experiments using known-answer synthetic fixtures, seeded perturbations, targeted ablation, blind comparison and explicit falsification conditions before moving to opaque material.

### Observer-history / memory experiments

Experiments testing whether retained experience changes later segmentation, interpretation or transition behavior, with reset/swap controls and frozen baselines.

## Falsification orientation

Mimulus is designed so attractive interpretations can fail.

Initial questions include:

- Does an apparent pattern survive materially different decoder assumptions?
- Does it disappear when the source feature claimed to support it is ablated?
- Does it survive only because multiple decoders inherited the same preprocessing?
- Can a competing decoder produce an equally coherent but incompatible account?
- Can similar structure be recovered from a matched null or perturbed source?
- Does semantic convergence remain after semantic relay is removed?
- Does retained history change later output, and does the effect collapse under reset or follow the history under swap?

A result that survives destruction of its alleged source support is not strengthened by that survival. It is evidence that the decoder may be insensitive to the feature it claims to use.

## Current evidence boundary

Mimulus currently has a developing experimental architecture and executable control instruments. It does not yet claim an empirical decipherment result.

The next decisive gate is:

1. a clean known-answer experiment that distinguishes correct recovery from shared wrong agreement; then
2. a blind opaque-source run with frozen representations, independent decoder contexts, preregistered controls and the possibility of `NO_RESIDUE`.

A successful result would not be `we decoded Voynich`. It would be evidence that Mimulus can distinguish apparent interpretive agreement from structure that remains attributable to the observed source after observer assumptions, preprocessing, history and semantic relay are varied or removed.

## Status

Early experimental research framework. Interfaces, fixtures, controls and tests are being added incrementally. No decipherment claim is made.

## Authorship

Research direction, conceptual framing, methodology, and original project work: Linda Thorstensen.
