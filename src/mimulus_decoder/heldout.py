"""Fixed supervised held-out token experiment, as specified in the v1 protocol."""
from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict

from .encoding import encode_tokens
from .learning import TrainingPair, learn_mapping
from .recovery import evaluate_recovery

PROTOCOL_ID = "supervised-heldout-token-v1"
SEEDS = (7, 19, 41)
VOCABULARY = ("sun", "water", "stone", "wind")
TRAIN = ("sun", "water", "stone", "wind", "sun", "stone")
TRAIN_PARTIAL = ("sun", "water", "stone", "sun", "stone")
HELDOUT = (("stone", "wind", "sun", "water"),
           ("water", "sun", "wind", "stone"))


def _digest(value: object) -> str:
    serialized = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def run_heldout_benchmark() -> dict[str, object]:
    """The orchestrator owns gold; only TrainingPair enters the learner.

    Separate API arguments provide an auditable access convention, not an
    enforced process sandbox. This is supervised inference of substitutions.
    """
    rows = []
    for seed in SEEDS:
        symbols = ["q", "x", "z", "v"]
        random.Random(seed).shuffle(symbols)
        reversible = dict(zip(VOCABULARY, symbols))
        lossy = {**reversible, "water": reversible["sun"]}
        for condition in ("complete-training", "incomplete-training",
                          "lossy-training", "wrong-label-control"):
            is_lossy = condition == "lossy-training"
            mapping = lossy if is_lossy else reversible
            tokens = TRAIN_PARTIAL if condition == "incomplete-training" else TRAIN
            training = encode_tokens(f"train-{seed}-{condition}", f"e-{seed}",
                                     tokens, mapping, allow_lossy=is_lossy)
            labels = tokens
            if condition == "wrong-label-control":
                # Predeclared derangement: all target labels are systematically wrong.
                rotated = dict(zip(VOCABULARY, VOCABULARY[1:] + VOCABULARY[:1]))
                labels = tuple(rotated[t] for t in tokens)
            pair = TrainingPair(training.source_id, training.encoded_tokens, labels)
            learned = learn_mapping((pair,), f"learner-{seed}-{condition}")
            references = [encode_tokens(f"held-{seed}-{condition}-{i}", f"e-{seed}",
                                        tokens, mapping, allow_lossy=is_lossy)
                          for i, tokens in enumerate(HELDOUT)]
            observations = [reference.observation() for reference in references]
            # Freeze all candidate outputs before giving references to the evaluator.
            readings = tuple(learned.decode(observation) for observation in observations)
            training_hash = _digest(asdict(pair))
            learned_hash = _digest(asdict(learned))
            for reference, observation, reading in zip(references, observations, readings):
                score = evaluate_recovery(reference, reading)
                rows.append({
                    "seed": seed, "condition": condition,
                    "source_id": score.source_id,
                    "training_sha256": training_hash,
                    "learned_mapping_sha256": learned_hash,
                    "observation_sha256": _digest(asdict(observation)),
                    "candidate_sha256": _digest(asdict(reading)),
                    "matched_tokens": score.matched_tokens,
                    "total_tokens": score.total_tokens,
                    "unresolved_tokens": score.unresolved_tokens,
                    "token_accuracy": score.token_accuracy,
                    "exact_recovery": score.exact_recovery,
                    "ambiguous_symbols": learned.ambiguous_symbols,
                })
    summaries = []
    for condition in ("complete-training", "incomplete-training",
                      "lossy-training", "wrong-label-control"):
        subset = [row for row in rows if row["condition"] == condition]
        total = sum(row["total_tokens"] for row in subset)
        summaries.append({"condition": condition, "sequences": len(subset),
                          "token_accuracy": sum(row["matched_tokens"] for row in subset) / total,
                          "unresolved_tokens": sum(row["unresolved_tokens"] for row in subset),
                          "exact_sequences": sum(row["exact_recovery"] for row in subset)})
    return {"protocol": PROTOCOL_ID, "seeds": SEEDS,
            "access": "Supervised aligned training pairs; no held-out targets or encoder key supplied to learner.",
            "scope": "Single-symbol substitutions; no unsupervised decipherment or statistical inference.",
            "summary": summaries, "runs": rows}


if __name__ == "__main__":
    print(json.dumps(run_heldout_benchmark(), indent=2))
