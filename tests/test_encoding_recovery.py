import pytest

from mimulus_decoder.benchmark import run_benchmark
from mimulus_decoder.decoders import explicit_mapping_decoder, token_structure_decoder
from mimulus_decoder.encoding import encode_tokens
from mimulus_decoder.model import CandidateReading, DecoderContext, MetaOutcome, compare_readings
from mimulus_decoder.recovery import evaluate_recovery


def fixture():
    return encode_tokens("s1", "e1", ("sun", "water", "sun", "stone"),
                         {"sun": "q", "water": "x", "stone": "z"})


def decode(source, mapping, name="d1"):
    return explicit_mapping_decoder(source.observation(), DecoderContext(name), mapping)


def test_matching_key_recovers_order_and_repeats():
    source = fixture()
    score = evaluate_recovery(source, decode(source, {"q": "sun", "x": "water", "z": "stone"}))
    assert score.exact_recovery
    assert score.token_accuracy == 1
    assert score.recovered_tokens == source.original_tokens
    assert score.collision_groups == ()


def test_agreement_under_shared_wrong_key_does_not_pass_recovery():
    source = fixture()
    wrong = {"q": "king", "x": "war", "z": "crown"}
    readings = [decode(source, wrong, name) for name in ("a", "b")]
    assert compare_readings(readings).outcome is MetaOutcome.CONVERGENCE
    assert all(evaluate_recovery(source, r).token_accuracy == 0 for r in readings)


def test_missing_key_is_unresolved_not_invented():
    source = fixture()
    score = evaluate_recovery(source, decode(source, {"q": "sun"}))
    assert score.recovered_tokens == ("sun", None, "sun", None)
    assert score.unresolved_tokens == 2
    assert score.token_accuracy == 0.5
    assert not score.exact_recovery


def test_swapped_key_preserves_repetition_but_fails_positional_recovery():
    source = fixture()
    score = evaluate_recovery(source, decode(source, {"q": "water", "x": "sun", "z": "stone"}))
    assert score.matched_tokens == 1
    assert score.token_accuracy == 0.25


def test_lossy_collision_requires_explicit_declaration_and_remains_visible():
    mapping = {"sun": "q", "water": "q"}
    with pytest.raises(ValueError, match="allow_lossy"):
        encode_tokens("s", "e", ("sun", "water"), mapping)
    source = encode_tokens("s", "e", ("sun", "water"), mapping, allow_lossy=True)
    score = evaluate_recovery(source, decode(source, {"q": "sun"}))
    assert score.token_accuracy == 0.5
    assert not score.exact_recovery
    assert score.collision_groups == (("q", ("sun", "water")),)


def test_lucky_exact_lossy_reading_does_not_remove_codebook_ambiguity():
    source = encode_tokens("s", "e", ("sun",), {"sun": "q", "water": "q"}, allow_lossy=True)
    score = evaluate_recovery(source, decode(source, {"q": "sun"}))
    assert score.exact_recovery
    assert score.collision_groups  # Exact on this sample does not prove reversibility.


def test_decoder_observation_excludes_reference_and_copies_caller_state():
    mapping = {"sun": "q"}
    source = encode_tokens("s", "e", ("sun",), mapping)
    mapping["sun"] = "changed"
    assert source.codebook == (("sun", "q"),)
    assert source.observation().transcription == "q"
    assert source.observation().features == {}


def test_prose_and_structural_agreement_are_not_token_recovery():
    source = fixture()
    prose = CandidateReading(source.source_id, "fluent", (), semantic_reading="sun water sun stone")
    structure = token_structure_decoder(source.observation(), DecoderContext("structure"))
    for reading in (prose, structure):
        score = evaluate_recovery(source, reading)
        assert score.unresolved_tokens == 4
        assert score.token_accuracy == 0


def test_reference_cannot_be_scored_against_another_source():
    with pytest.raises(ValueError, match="source identifier"):
        evaluate_recovery(fixture(), CandidateReading("other", "d", ()))


@pytest.mark.parametrize("tokens,mapping", [
    ((), {"sun": "q"}), (("sun",), {}), (("sun",), {"water": "x"}),
    (("sun water",), {"sun water": "q"}), (("sun",), {"sun": "q x"}),
    (("sun",), {"sun": ""}), (("",), {"": "q"}),
])
def test_invalid_or_incomplete_encoding_is_rejected(tokens, mapping):
    with pytest.raises(ValueError):
        encode_tokens("s", "e", tokens, mapping)


def test_multiword_mapping_cannot_count_as_single_token_recovery():
    source = fixture()
    score = evaluate_recovery(source, decode(source, {"q": "sun water"}))
    assert score.matched_tokens == 0


def test_same_key_recovers_an_unseen_sequence_without_claiming_key_inference():
    source = encode_tokens("held-sequence", "e", ("stone", "water", "stone", "sun"),
                           {"sun": "q", "water": "x", "stone": "z"})
    assert evaluate_recovery(source, decode(source, {"q": "sun", "x": "water", "z": "stone"})).exact_recovery


def test_executable_benchmark_exposes_failure_controls():
    report = run_benchmark()
    scores = {r["decoder_id"]: r for r in report["results"]}
    assert scores["matching-key"]["exact_recovery"]
    assert scores["wrong-key-a"]["token_accuracy"] == 0
    assert scores["incomplete-key"]["unresolved_tokens"] == 2
    assert scores["lossy-choice"]["token_accuracy"] == 0.75
    assert report["shared_wrong_key_agreement"] == "convergence"
