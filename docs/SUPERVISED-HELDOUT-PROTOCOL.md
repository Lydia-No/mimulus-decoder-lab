# Supervised held-out token protocol v1

Protocol identifier: `supervised-heldout-token-v1`.

This protocol is specified before its first recorded benchmark execution. The
learner, fixed controls, expected software outcomes, and tests are designed
together. This is a software validation protocol, not independent scientific
preregistration or a hypothesis test.

## Question and access regime

Can a learner extract unambiguous symbol-to-token mappings from aligned labeled
training pairs, then recover different sequences without receiving the encoder
key or held-out target tokens?

The evaluator/orchestrator owns the originals and encoding codebook. The learner
receives only `TrainingPair` records with aligned symbols and target labels.
Positions and token boundaries are supplied. Held-out decoding receives only an
`Observation` of encoded symbols. This is supervised substitution learning;
language discovery, key inference without labels, and semantic interpretation
are not tested.

The API does not enforce process isolation. Source-ID overlap is rejected, but
the API cannot prove a caller has not reused training content under another ID.
The fixed runner checks its split in tests. Future external runs require a
separate access audit.

## Fixed design

- Vocabulary: `sun`, `water`, `stone`, `wind`.
- Symbols: `q`, `x`, `z`, `v`; their assignment is shuffled with seeds 7, 19, 41.
- Complete training: `sun water stone wind sun stone`.
- Incomplete training: `sun water stone sun stone` (no `wind`).
- Held-out sequences: `stone wind sun water`; `water sun wind stone`.
- One symbol is emitted per token. Each held-out sequence is distinct from
  either training sequence. Vocabulary overlap is intentional.
- Every seed and condition is reported; no selection of the best run.

These sequences test new orderings of a tiny controlled vocabulary. They do
not establish generalization to new languages, encoding families, or corpora.

## Learner frozen for v1

Collect every target observed for each training symbol. Commit a mapping only
when the observed target set has one member. Conflicting targets are retained
as ambiguity and excluded from the mapping; majority voting is not used.
Unseen symbols remain unresolved. Freeze the learned mapping before held-out
decoding, then freeze all candidate readings before reference scoring.

## Conditions and expected checks

| Condition | Expected recovery | What it checks |
| --- | --- | --- |
| Reversible, complete training | 100% | Transfer of learned mappings to new orderings |
| Reversible, incomplete training | 75%; one unresolved token per sequence | No guessing for an unseen symbol |
| Lossy, complete training (`sun` and `water` share a symbol) | 50%; two unresolved tokens per sequence | Abstention under irreducible training conflict |
| Wrong-label control | 0% | Accuracy depends on correct training labels |

The wrong-label control rotates all training targets along the vocabulary list.
It is a fixed derangement, not a sampled statistical null distribution. Seed
variation only relabels symbols; these runs are not independent empirical
replications. Lossy and reversible substitutions are distinct conditions within
one token-encoding family, not broad coverage of encoding mechanisms.

## Scoring and audit record

Use the v1 positional recovery evaluator. Report accuracy, unresolved counts,
exact sequence counts, and ambiguous symbols for every run. SHA-256 hashes record
training pairs, frozen learned mappings, encoded observations, and candidate
readings. Hashes support reproducibility; they do not prove access isolation,
timestamp precedence, or independence.

No hyperparameter fitting, statistical significance claim, or correction of the
learner after viewing held-out answers is permitted within this protocol version.
Changes require a new version and a fresh evaluation set.

The first recorded execution is saved in
[`reports/supervised-heldout-token-v1.json`](../reports/supervised-heldout-token-v1.json).
All 24 sequence evaluations matched the declared software checks: 100%, 75%,
50%, and 0% aggregate token accuracy in the four conditions respectively.
All 38 repository tests passed. These outcomes validate this controlled learner
and evaluator; they are not an independent empirical discovery.

Run from the repository root:

```sh
PYTHONPATH=src python -m mimulus_decoder.heldout
python -m pytest -q
```

## Next gate

Before testing genuinely unknown encodings, specify the information available
without aligned labels, multiple materially different encoding families, larger
fresh evaluation sets, and chance/baseline comparisons appropriate to the task.
Keep Voynich source provenance and the memory experiment separate.
