from mimulus_decoder.memory import (
    ChangeKind,
    InterpretationCondition,
    MemoryRecord,
    compare_reconstruction,
)
from mimulus_decoder.nulls import run_synthetic_null


def test_m0_is_compared_to_new_record_without_mutation():
    m0 = MemoryRecord("p1", "M0", {"storm_distance": "far", "horse_moving": False})
    r1 = MemoryRecord("p1", "R1", {"storm_distance": "near", "horse_moving": False})
    condition = InterpretationCondition("C1", "storm framed as close", {"storm_distance": "near"})

    result = compare_reconstruction(m0, r1, condition)
    assert m0.features["storm_distance"] == "far"
    assert result.baseline_id == "M0"
    assert result.reconstruction_id == "R1"


def test_interpretation_aligned_change_is_explicit_not_inferred_from_prose():
    m0 = MemoryRecord("p1", "M0", {"storm_distance": "far"})
    r1 = MemoryRecord("p1", "R1", {"storm_distance": "near"})
    condition = InterpretationCondition("C1", "arbitrary prose is not parsed", {"storm_distance": "near"})

    [change] = compare_reconstruction(m0, r1, condition).changes
    assert change.kind is ChangeKind.INTERPRETATION_ALIGNED


def test_unpredicted_change_remains_plain_change():
    m0 = MemoryRecord("p1", "M0", {"horse_moving": False})
    r1 = MemoryRecord("p1", "R1", {"horse_moving": True})
    condition = InterpretationCondition("C1", "frame", {"storm_distance": "near"})

    [change] = compare_reconstruction(m0, r1, condition).changes
    assert change.kind is ChangeKind.CHANGED


def test_addition_and_omission_are_preserved():
    m0 = MemoryRecord("p1", "M0", {"cube_color": "white", "ladder_material": "wood"})
    r1 = MemoryRecord("p1", "R1", {"cube_color": "white", "flowers_color": "red"})
    condition = InterpretationCondition("C0", "neutral", {})
    kinds = {c.feature: c.kind for c in compare_reconstruction(m0, r1, condition).changes}

    assert kinds["ladder_material"] is ChangeKind.OMISSION
    assert kinds["flowers_color"] is ChangeKind.ADDITION


def test_baseline_cannot_be_reused_as_reconstruction():
    m0 = MemoryRecord("p1", "M0", {"x": 1})
    try:
        compare_reconstruction(m0, m0, InterpretationCondition("C0", "neutral", {}))
    except ValueError:
        pass
    else:
        raise AssertionError("M0 must not be overwritten/reused as R1")


def test_synthetic_null_does_not_encode_condition_into_reconstruction():
    first = run_synthetic_null(n=400, seed=7)
    second = run_synthetic_null(n=400, seed=7)
    assert first == second
    # Broad guardrail only: the null generator should not deterministically favor a condition.
    assert abs(first.difference) < 50
