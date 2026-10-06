from __future__ import annotations

from collections import Counter
from typing import Mapping

from .model import CandidateReading, Claim, ClaimKind, DecoderContext, Observation


def token_structure_decoder(observation: Observation, context: DecoderContext) -> CandidateReading:
    """A semantics-free baseline: report repeated token structure only."""
    tokens = observation.transcription.split()
    counts = Counter(tokens)
    repeated = sorted(token for token, count in counts.items() if count > 1)

    claims = tuple(
        Claim(
            text=f"Token {token!r} occurs {counts[token]} times.",
            kind=ClaimKind.DERIVED,
            support=("transcription",),
        )
        for token in repeated
    )
    structure = tuple(f"repeat:{token}:{counts[token]}" for token in repeated)

    return CandidateReading(
        source_id=observation.source_id,
        decoder_id=context.decoder_id,
        claims=claims,
        structural_claims=structure,
        uncertainties=("Tokenization inherits the supplied transcription convention.",),
    )


def explicit_mapping_decoder(
    observation: Observation,
    context: DecoderContext,
    mapping: Mapping[str, str],
) -> CandidateReading:
    """Apply only mappings declared by the caller; unknown tokens remain unresolved."""
    tokens = observation.transcription.split()
    rendered: list[str] = []
    used: dict[str, str] = {}
    unresolved: list[str] = []

    for token in tokens:
        if token in mapping:
            rendered.append(mapping[token])
            used[token] = mapping[token]
        else:
            rendered.append(f"[{token}]")
            unresolved.append(token)

    claims = tuple(
        Claim(
            text=f"{source!r} -> {target!r}",
            kind=ClaimKind.DECODER_SUPPLIED,
            support=(f"decoder:{context.decoder_id}",),
        )
        for source, target in sorted(used.items())
    )

    return CandidateReading(
        source_id=observation.source_id,
        decoder_id=context.decoder_id,
        claims=claims,
        mapping_claims=used,
        semantic_reading=" ".join(rendered),
        uncertainties=tuple(f"No mapping for {token!r}" for token in sorted(set(unresolved))),
    )
