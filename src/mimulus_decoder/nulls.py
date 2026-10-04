from __future__ import annotations

import random
from dataclasses import dataclass

from .memory import InterpretationCondition, MemoryRecord, compare_reconstruction


@dataclass(frozen=True)
class NullSummary:
    participants: int
    aligned_a: int
    aligned_b: int
    difference: int


def run_synthetic_null(n: int = 200, seed: int = 1) -> NullSummary:
    """Generate reconstruction noise independently of assigned condition.

    This is a software sanity check, not a statistical significance test.
    Conditions predict opposite values for one feature; reconstruction noise is
    generated without access to assignment, so neither condition should receive
    a systematic advantage except finite-sample fluctuation.
    """
    rng = random.Random(seed)
    conditions = (
        InterpretationCondition("A", "frame A", {"storm_distance": "near"}),
        InterpretationCondition("B", "frame B", {"storm_distance": "far"}),
    )

    totals = {"A": 0, "B": 0}
    for i in range(n):
        condition = conditions[i % 2]
        m0 = MemoryRecord(str(i), "M0", {"storm_distance": "middle", "horse_moving": False})

        # Crucially generated independently of condition.
        r1_value = rng.choice(("near", "middle", "far"))
        r1 = MemoryRecord(str(i), "R1", {"storm_distance": r1_value, "horse_moving": False})
        comparison = compare_reconstruction(m0, r1, condition)
        totals[condition.condition_id] += comparison.aligned_count

    return NullSummary(n, totals["A"], totals["B"], totals["A"] - totals["B"])
