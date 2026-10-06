"""Learn explicit mappings only from aligned, labeled training examples."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .decoders import explicit_mapping_decoder
from .model import CandidateReading, DecoderContext, Observation


@dataclass(frozen=True)
class TrainingPair:
    example_id: str
    symbols: tuple[str, ...]
    targets: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.example_id or not self.symbols or len(self.symbols) != len(self.targets):
            raise ValueError("Training examples need an identifier and nonempty aligned sequences")
        if not isinstance(self.symbols, tuple) or not isinstance(self.targets, tuple):
            raise ValueError("Training sequences must be immutable tuples")
        if any(not isinstance(t, str) or not t or any(c.isspace() for c in t)
               for t in self.symbols + self.targets):
            raise ValueError("Training entries must be single nonempty tokens")


@dataclass(frozen=True)
class LearnedMapping:
    decoder_id: str
    training_ids: tuple[str, ...]
    mapping: tuple[tuple[str, str], ...]
    ambiguous_symbols: tuple[tuple[str, tuple[str, ...]], ...]

    def decode(self, observation: Observation) -> CandidateReading:
        if observation.source_id in self.training_ids:
            raise ValueError("Held-out source identifier overlaps training")
        reading = explicit_mapping_decoder(
            observation,
            DecoderContext(self.decoder_id, {"access": "aligned labeled training pairs only"}),
            dict(self.mapping),
        )
        ambiguity_notes = tuple(
            f"Training supports competing targets for {symbol!r}: {targets!r}"
            for symbol, targets in self.ambiguous_symbols
            if symbol in observation.transcription.split()
        )
        return CandidateReading(
            source_id=reading.source_id,
            decoder_id=reading.decoder_id,
            claims=reading.claims,
            mapping_claims=reading.mapping_claims,
            structural_claims=reading.structural_claims,
            semantic_reading=reading.semantic_reading,
            uncertainties=reading.uncertainties + ambiguity_notes,
        )


def learn_mapping(examples: Sequence[TrainingPair], decoder_id: str) -> LearnedMapping:
    """Infer unanimous symbol-target pairs; abstain on conflicts rather than vote.

    No encoder fixture, encoder codebook, or held-out reference is accepted.
    Labeled position alignment is supplied, not learned.
    """
    if not examples or not decoder_id:
        raise ValueError("Training examples and a decoder identifier are required")
    ids = tuple(e.example_id for e in examples)
    if len(set(ids)) != len(ids):
        raise ValueError("Training example identifiers must be unique")
    targets: dict[str, set[str]] = {}
    for example in examples:
        for symbol, target in zip(example.symbols, example.targets):
            targets.setdefault(symbol, set()).add(target)
    mapping = tuple((symbol, next(iter(values))) for symbol, values in sorted(targets.items())
                    if len(values) == 1)
    ambiguous = tuple((symbol, tuple(sorted(values))) for symbol, values in sorted(targets.items())
                      if len(values) > 1)
    return LearnedMapping(decoder_id, ids, mapping, ambiguous)
