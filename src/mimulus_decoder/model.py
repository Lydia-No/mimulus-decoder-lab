from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class ClaimKind(str, Enum):
    OBSERVED = "observed"
    DECODER_SUPPLIED = "decoder_supplied"
    DERIVED = "derived"
    EXTERNAL = "external_corroboration"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class Observation:
    source_id: str
    transcription: str
    features: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class Claim:
    text: str
    kind: ClaimKind
    support: tuple[str, ...] = ()


@dataclass(frozen=True)
class DecoderContext:
    decoder_id: str
    assumptions: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class CandidateReading:
    source_id: str
    decoder_id: str
    claims: tuple[Claim, ...]
    mapping_claims: Mapping[str, str] = field(default_factory=dict)
    structural_claims: tuple[str, ...] = ()
    semantic_reading: str | None = None
    uncertainties: tuple[str, ...] = ()


class MetaOutcome(str, Enum):
    CONVERGENCE = "convergence"
    DIVERGENCE = "divergence"
    UNDETERMINED = "undetermined"


@dataclass(frozen=True)
class MetaObservation:
    outcome: MetaOutcome
    shared_mappings: Mapping[str, str]
    conflicting_mappings: Mapping[str, tuple[str, ...]]
    shared_structure: tuple[str, ...]
    note: str


def compare_readings(readings: Sequence[CandidateReading]) -> MetaObservation:
    if len(readings) < 2:
        return MetaObservation(
            MetaOutcome.UNDETERMINED, {}, {}, (),
            "At least two independently produced readings are required.",
        )

    if len({reading.source_id for reading in readings}) != 1:
        raise ValueError("All readings must refer to the same frozen source")

    mapping_keys = set().union(*(reading.mapping_claims.keys() for reading in readings))
    shared: dict[str, str] = {}
    conflicts: dict[str, tuple[str, ...]] = {}

    for key in mapping_keys:
        values = [reading.mapping_claims[key] for reading in readings if key in reading.mapping_claims]
        unique = tuple(sorted(set(values)))
        if len(values) == len(readings) and len(unique) == 1:
            shared[key] = unique[0]
        elif len(unique) > 1:
            conflicts[key] = unique

    structural_sets = [set(reading.structural_claims) for reading in readings]
    shared_structure = tuple(sorted(set.intersection(*structural_sets))) if structural_sets else ()

    if conflicts:
        return MetaObservation(
            MetaOutcome.DIVERGENCE, shared, conflicts, shared_structure,
            "Explicit source mappings conflict across decoder contexts.",
        )

    if shared or shared_structure:
        return MetaObservation(
            MetaOutcome.CONVERGENCE, shared, {}, shared_structure,
            "Explicit structural residue survives decoder variation; validation remains required.",
        )

    return MetaObservation(
        MetaOutcome.UNDETERMINED, {}, {}, (),
        "No explicit cross-decoder residue. Semantic plausibility alone is not evidence.",
    )
