import pytest

from mimulus_decoder.context_cube import AXES, context_hypercube
from mimulus_decoder.encoding import encode_tokens
from mimulus_decoder.model import Observation


def graph():
    fixture = encode_tokens("s", "e", ("sun", "water", "sun", "stone"),
                            {"sun": "q", "water": "x", "stone": "z"})
    return context_hypercube(fixture.observation(), {"q": "sun", "x": "water", "z": "stone"},
                            {"q": "king", "x": "war", "z": "crown"}, fixture)


def test_q4_has_sixteen_vertices_and_thirty_two_unique_one_axis_edges():
    cube = graph()
    assert len(cube["nodes"]) == 16
    assert len(cube["edges"]) == 32
    assert len({n["id"] for n in cube["nodes"]}) == 16
    assert len({(e["from"], e["to"]) for e in cube["edges"]}) == 32
    degree = {n["id"]: 0 for n in cube["nodes"]}
    for edge in cube["edges"]:
        changed = [i for i, (a, b) in enumerate(zip(edge["from"], edge["to"])) if a != b]
        assert len(changed) == 1
        assert edge["axis"] == AXES[changed[0]]["id"]
        degree[edge["from"]] += 1
        degree[edge["to"]] += 1
    assert set(degree.values()) == {4}


def test_all_contexts_preserve_one_source_and_default_recovery():
    cube = graph()
    nodes = {n["id"]: n for n in cube["nodes"]}
    assert {n["reading"]["source_id"] for n in cube["nodes"]} == {"s"}
    assert nodes["0000"]["recovery"]["token_accuracy"] == 1
    assert nodes["1000"]["recovery"]["token_accuracy"] == 0
    assert nodes["0100"]["mapping"] == {"x": "water", "z": "stone"}
    assert nodes["0001"]["mapping"] == {"q": "sun"}
    assert nodes["0001"]["recovery"]["unresolved_tokens"] == 2


def test_rotation_precedes_filters_and_does_not_modify_supplied_rules():
    source = Observation("s", "q x q z")
    a = {"q": "sun", "x": "water", "z": "stone"}
    b = {"q": "king"}
    nodes = {n["id"]: n for n in context_hypercube(source, a, b)["nodes"]}
    assert nodes["0010"]["mapping"] == {"q": "water", "x": "stone", "z": "sun"}
    assert nodes["0110"]["mapping"] == {"x": "stone", "z": "sun"}
    assert a == {"q": "sun", "x": "water", "z": "stone"}
    assert b == {"q": "king"}


def test_opaque_cube_never_assigns_recovery_scores():
    cube = context_hypercube(Observation("s", "q q x"), {"q": "sun"}, {})
    assert all(n["recovery"] is None for n in cube["nodes"])


def test_identical_context_outputs_do_not_establish_independence():
    cube = context_hypercube(Observation("s", "q q"), {"q": "sun"}, {"q": "sun"})
    nodes = {n["id"]: n for n in cube["nodes"]}
    assert nodes["0000"]["mapping"] == nodes["0010"]["mapping"]
    assert "not independent" in cube["boundary"]


@pytest.mark.parametrize("source", ["x q", "q", "q x x"])
def test_reference_with_same_id_but_different_tokens_is_rejected(source):
    fixture = encode_tokens("s", "e", ("sun", "water"), {"sun": "q", "water": "x"})
    with pytest.raises(ValueError, match="same encoded token sequence"):
        context_hypercube(Observation("s", source), {"q": "sun", "x": "water"}, {}, fixture)


def test_reference_with_different_source_id_is_rejected():
    fixture = encode_tokens("s", "e", ("sun",), {"sun": "q"})
    with pytest.raises(ValueError, match="same source identifier"):
        context_hypercube(Observation("other", "q"), {"q": "sun"}, {}, fixture)


def test_reference_alignment_compares_tokens_not_whitespace():
    fixture = encode_tokens("s", "e", ("sun", "water"), {"sun": "q", "water": "x"})
    cube = context_hypercube(Observation("s", " q\n\tx "), {"q": "sun", "x": "water"}, {}, fixture)
    assert cube["nodes"][0]["recovery"]["exact_recovery"]
