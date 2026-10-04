"""Evaluate explicit token mappings against a separate known reference."""
from __future__ import annotations

from dataclasses import dataclass

from .encoding import EncodedFixture
from .model import CandidateReading


@dataclass(frozen=True)
class RecoveryResult:
    source_id: str
    decoder_id: str
    recovered_tokens: tuple[str | None, ...]
    matched_tokens: int
    total_tokens: int
    unresolved_tokens: int
    collision_groups: tuple[tuple[str, tuple[str, ...]], ...]

    @property
    def token_accuracy(self) -> float:
        return self.matched_tokens / self.total_tokens

    @property
    def exact_recovery(self) -> bool:
        return self.matched_tokens == self.total_tokens


def evaluate_recovery(fixture: EncodedFixture, reading: CandidateReading) -> RecoveryResult:
    """Score positional token recovery, not prose fluency or decoder agreement.

    Each encoded position is resolved only by its explicit mapping claim.
    Missing mappings remain None. A multiword output is a mismatch with this
    one-token reference. Semantic prose is deliberately not used as evidence.
    This evaluator cannot verify independence or prevent a caller leaking gold.
    """
    if fixture.source_id != reading.source_id:
        raise ValueError("Reading and reference must have the same source identifier")
    recovered = tuple(reading.mapping_claims.get(t) for t in fixture.encoded_tokens)
    matched = sum(a == b for a, b in zip(fixture.original_tokens, recovered))
    return RecoveryResult(
        fixture.source_id, reading.decoder_id, recovered, matched,
        len(fixture.original_tokens), sum(t is None for t in recovered),
        fixture.collision_groups,
    )
