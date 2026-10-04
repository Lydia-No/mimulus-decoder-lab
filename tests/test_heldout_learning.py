import pytest

from mimulus_decoder.heldout import HELDOUT, TRAIN, TRAIN_PARTIAL, run_heldout_benchmark
from mimulus_decoder.learning import TrainingPair, learn_mapping
from mimulus_decoder.model import Observation


def test_learner_recovers_unseen_order_without_encoder_key():
    learned = learn_mapping((TrainingPair("train", ("q", "x", "q"),
                                         ("sun", "water", "sun")),), "learner")
    assert learned.decode(Observation("held", "x q x")).semantic_reading == "water sun water"


def test_unseen_symbol_remains_unresolved():
    learned = learn_mapping((TrainingPair("train", ("q",), ("sun",)),), "learner")
    reading = learned.decode(Observation("held", "q z"))
    assert reading.mapping_claims == {"q": "sun"}
    assert reading.semantic_reading == "sun [z]"
    assert "No mapping for 'z'" in reading.uncertainties


def test_conflicting_training_labels_abstain_even_with_majority():
    learned = learn_mapping((TrainingPair("train", ("q", "q", "q", "z"),
                                         ("sun", "sun", "water", "stone")),), "learner")
    assert learned.mapping == (("z", "stone"),)
    assert learned.ambiguous_symbols == (("q", ("sun", "water")),)
    reading = learned.decode(Observation("held", "q z"))
    assert reading.semantic_reading == "[q] stone"
    assert any("competing targets" in note for note in reading.uncertainties)


def test_training_and_heldout_identifiers_cannot_overlap():
    learned = learn_mapping((TrainingPair("train", ("q",), ("sun",)),), "learner")
    with pytest.raises(ValueError, match="overlaps training"):
        learned.decode(Observation("train", "q"))


def test_duplicate_training_identifiers_are_rejected():
    pair = TrainingPair("train", ("q",), ("sun",))
    with pytest.raises(ValueError, match="unique"):
        learn_mapping((pair, pair), "learner")


@pytest.mark.parametrize("symbols,targets", [
    ((), ()), (("q",), ("sun", "water")), (("q x",), ("sun",)),
    (("q",), ("",)), (["q"], ("sun",)),
])
def test_malformed_training_pairs_are_rejected(symbols, targets):
    with pytest.raises(ValueError):
        TrainingPair("train", symbols, targets)


def test_empty_training_is_rejected():
    with pytest.raises(ValueError):
        learn_mapping((), "learner")


def test_heldout_sequences_are_distinct_from_training():
    assert all(sequence not in (TRAIN, TRAIN_PARTIAL) for sequence in HELDOUT)
    assert len(set(HELDOUT)) == len(HELDOUT)


def test_fixed_protocol_results_and_hashes_are_reproducible():
    report = run_heldout_benchmark()
    assert report == run_heldout_benchmark()
    assert len(report["runs"]) == 24
    scores = {row["condition"]: row for row in report["summary"]}
    assert scores["complete-training"]["token_accuracy"] == 1
    assert scores["complete-training"]["exact_sequences"] == 6
    assert scores["incomplete-training"]["token_accuracy"] == 0.75
    assert scores["incomplete-training"]["unresolved_tokens"] == 6
    assert scores["lossy-training"]["token_accuracy"] == 0.5
    assert scores["lossy-training"]["unresolved_tokens"] == 12
    assert scores["wrong-label-control"]["token_accuracy"] == 0
    for row in report["runs"]:
        assert all(len(row[key]) == 64 for key in (
            "training_sha256", "learned_mapping_sha256", "observation_sha256", "candidate_sha256"))


def test_heldout_reference_is_not_used_to_patch_learned_mapping():
    learned = learn_mapping((TrainingPair("train", ("q",), ("sun",)),), "learner")
    before = learned.mapping
    learned.decode(Observation("held-a", "q x"))
    learned.decode(Observation("held-b", "x q"))
    assert learned.mapping == before == (("q", "sun"),)
