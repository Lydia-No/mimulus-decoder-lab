"""Controlled token encodings with evaluator-only reference information."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .model import Observation


def _token(value: str) -> bool:
    return isinstance(value, str) and bool(value) and not any(c.isspace() for c in value)


@dataclass(frozen=True)
class EncodedFixture:
    """Keep this reference record with the evaluator, not the decoder."""

    source_id: str
    encoder_id: str
    original_tokens: tuple[str, ...]
    encoded_tokens: tuple[str, ...]
    codebook: tuple[tuple[str, str], ...]

    @property
    def collision_groups(self) -> tuple[tuple[str, tuple[str, ...]], ...]:
        groups: dict[str, list[str]] = {}
        for original, symbol in self.codebook:
            groups.setdefault(symbol, []).append(original)
        return tuple((symbol, tuple(tokens)) for symbol, tokens in sorted(groups.items())
                     if len(tokens) > 1)

    def observation(self) -> Observation:
        """Expose symbols only; no original tokens, inverse key, or gold labels."""
        return Observation(self.source_id, " ".join(self.encoded_tokens))


def encode_tokens(
    source_id: str,
    encoder_id: str,
    original_tokens: tuple[str, ...],
    mapping: Mapping[str, str],
    *,
    allow_lossy: bool = False,
) -> EncodedFixture:
    """Encode one symbol per input token, refusing undeclared information loss.

    This is a token benchmark: original spacing and punctuation outside the
    supplied tokens are not modeled. Many-to-one mappings require allow_lossy.
    """
    if not source_id or not encoder_id:
        raise ValueError("Source and encoder identifiers are required")
    tokens = tuple(original_tokens)
    pairs = tuple(sorted(mapping.items()))
    if not tokens or not all(_token(t) for t in tokens):
        raise ValueError("Input must contain nonempty, whitespace-free tokens")
    if not pairs or not all(_token(k) and _token(v) for k, v in pairs):
        raise ValueError("Codebook keys and values must be single nonempty tokens")
    codebook = dict(pairs)
    missing = set(tokens) - codebook.keys()
    if missing:
        raise ValueError(f"Encoder has no mapping for {sorted(missing)!r}")
    if not allow_lossy and len(set(codebook.values())) != len(codebook):
        raise ValueError("Many-to-one codebook requires explicit allow_lossy=True")
    return EncodedFixture(source_id, encoder_id, tokens,
                          tuple(codebook[t] for t in tokens), pairs)
