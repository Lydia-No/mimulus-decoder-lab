from pathlib import Path

from mimulus_decoder.voynich import (
    character_permutation_null,
    parse_ivtff_folio,
    permutation_null,
    structural_report,
)

SOURCE = Path("data/voynich/source-001-f1r.ivtff.txt")


def load():
    return parse_ivtff_folio(SOURCE.read_text(encoding="utf-8"))


def test_source_parses_without_semantic_mapping():
    lines = load()
    report = structural_report(lines)
    assert len(lines) == 31
    assert report.token_count > 100
    assert report.unique_tokens > 50


def test_token_order_null_preserves_bag_statistics():
    lines = load()
    original = structural_report(lines)
    shuffled = structural_report(permutation_null(lines, seed=7))
    assert original.token_count == shuffled.token_count
    assert original.unique_tokens == shuffled.unique_tokens
    assert original.repeated_tokens == shuffled.repeated_tokens
    assert original.initial_counts == shuffled.initial_counts
    assert original.final_counts == shuffled.final_counts


def test_token_order_null_can_destroy_adjacency():
    lines = load()
    original = structural_report(lines)
    shuffled = structural_report(permutation_null(lines, seed=7))
    assert original.adjacency != shuffled.adjacency


def test_character_null_preserves_lengths_but_not_boundary_character_structure():
    lines = load()
    original = structural_report(lines)
    shuffled = structural_report(character_permutation_null(lines, seed=7))
    assert original.token_count == shuffled.token_count
    assert original.token_length_mean == shuffled.token_length_mean
    assert original.token_length_entropy == shuffled.token_length_entropy
    assert (original.initial_counts, original.final_counts) != (shuffled.initial_counts, shuffled.final_counts)
