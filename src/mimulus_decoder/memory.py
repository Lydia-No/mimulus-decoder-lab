from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

Scalar = str | int | float | bool | None


@dataclass(frozen=True)
class MemoryRecord:
    participant_id: str
    record_id: str
    features: Mapping[str, Scalar]
    free_text: str = ""


@dataclass(frozen=True)
class InterpretationCondition:
    condition_id: str
    intervention_text: str
    predicted_changes: Mapping[str, Scalar]


class ChangeKind(str, Enum):
    UNCHANGED = "unchanged"
    ADDITION = "addition"
    OMISSION = "omission"
    CHANGED = "changed"
    INTERPRETATION_ALIGNED = "interpretation_aligned"
    INTERPRETATION_OPPOSED = "interpretation_opposed"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class FeatureChange:
    feature: str
    before: Scalar
    after: Scalar
    kind: ChangeKind


@dataclass(frozen=True)
class ReconstructionComparison:
    participant_id: str
    baseline_id: str
    reconstruction_id: str
    condition_id: str
    changes: tuple[FeatureChange, ...]

    @property
    def aligned_count(self) -> int:
        return sum(c.kind is ChangeKind.INTERPRETATION_ALIGNED for c in self.changes)


def compare_reconstruction(
    baseline: MemoryRecord,
    reconstruction: MemoryRecord,
    condition: InterpretationCondition,
) -> ReconstructionComparison:
    if baseline.participant_id != reconstruction.participant_id:
        raise ValueError("M0 and reconstruction must belong to the same participant")
    if baseline.record_id == reconstruction.record_id:
        raise ValueError("Reconstruction must be stored as a new record; M0 is immutable")

    keys = set(baseline.features) | set(reconstruction.features)
    changes: list[FeatureChange] = []

    for key in sorted(keys):
        before = baseline.features.get(key)
        after = reconstruction.features.get(key)

        if key not in baseline.features:
            kind = ChangeKind.ADDITION
        elif key not in reconstruction.features:
            kind = ChangeKind.OMISSION
        elif before == after:
            kind = ChangeKind.UNCHANGED
        elif key in condition.predicted_changes:
            predicted = condition.predicted_changes[key]
            if after == predicted:
                kind = ChangeKind.INTERPRETATION_ALIGNED
            elif before == predicted:
                kind = ChangeKind.INTERPRETATION_OPPOSED
            else:
                kind = ChangeKind.AMBIGUOUS
        else:
            kind = ChangeKind.CHANGED

        changes.append(FeatureChange(key, before, after, kind))

    return ReconstructionComparison(
        participant_id=baseline.participant_id,
        baseline_id=baseline.record_id,
        reconstruction_id=reconstruction.record_id,
        condition_id=condition.condition_id,
        changes=tuple(changes),
    )
