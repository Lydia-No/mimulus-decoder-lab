from mimulus_decoder.decoders import explicit_mapping_decoder, token_structure_decoder
from mimulus_decoder.model import DecoderContext, MetaOutcome, Observation, compare_readings


def test_semantic_coherence_without_shared_structure_is_undetermined():
    source = Observation("s1", "a b a")
    left = explicit_mapping_decoder(source, DecoderContext("left"), {"a": "sun", "b": "water"})
    right = explicit_mapping_decoder(source, DecoderContext("right"), {"a": "king", "b": "war"})

    result = compare_readings([left, right])
    assert result.outcome is MetaOutcome.DIVERGENCE
    assert "a" in result.conflicting_mappings


def test_same_explicit_mapping_can_converge_without_claiming_truth():
    source = Observation("s1", "a b a")
    left = explicit_mapping_decoder(source, DecoderContext("left"), {"a": "X"})
    right = explicit_mapping_decoder(source, DecoderContext("right"), {"a": "X"})

    result = compare_readings([left, right])
    assert result.outcome is MetaOutcome.CONVERGENCE
    assert result.shared_mappings == {"a": "X"}
    assert "validation remains required" in result.note


def test_structure_can_be_observed_without_semantics():
    source = Observation("s1", "a b a c b a")
    one = token_structure_decoder(source, DecoderContext("structure-1"))
    two = token_structure_decoder(source, DecoderContext("structure-2"))

    result = compare_readings([one, two])
    assert result.outcome is MetaOutcome.CONVERGENCE
    assert "repeat:a:3" in result.shared_structure
    assert "repeat:b:2" in result.shared_structure


def test_single_reading_is_undetermined():
    source = Observation("s1", "a b")
    reading = token_structure_decoder(source, DecoderContext("one"))
    assert compare_readings([reading]).outcome is MetaOutcome.UNDETERMINED


def test_sources_cannot_be_silently_mixed():
    a = token_structure_decoder(Observation("a", "x x"), DecoderContext("d1"))
    b = token_structure_decoder(Observation("b", "x x"), DecoderContext("d2"))

    try:
        compare_readings([a, b])
    except ValueError:
        pass
    else:
        raise AssertionError("different frozen sources must not be compared as one source")
