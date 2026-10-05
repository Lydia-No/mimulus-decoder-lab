from __future__ import annotations

import math
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable

LINE_RE = re.compile(r"^<(?P<locus>f[^>]+)>\s+(?P<text>.+)$")


@dataclass(frozen=True)
class VoynichLine:
    locus: str
    text: str
    tokens: tuple[str, ...]


@dataclass(frozen=True)
class StructuralReport:
    line_count: int
    token_count: int
    unique_tokens: int
    repeated_tokens: tuple[tuple[str, int], ...]
    initial_counts: tuple[tuple[str, int], ...]
    final_counts: tuple[tuple[str, int], ...]
    token_length_mean: float
    token_length_entropy: float
    adjacency: tuple[tuple[str, str, int], ...]


def parse_ivtff_folio(text: str) -> tuple[VoynichLine, ...]:
    lines: list[VoynichLine] = []
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#") or raw.startswith("<f1r>"):
            continue
        match = LINE_RE.match(raw)
        if not match:
            continue
        body = match.group("text")
        # Preserve uncertain glyph-bearing tokens; commas mark uncertain spaces in source.
        tokens = tuple(tok for tok in body.split(".") if tok)
        lines.append(VoynichLine(match.group("locus"), body, tokens))
    return tuple(lines)


def _entropy(values: Iterable[int]) -> float:
    counts = Counter(values)
    n = sum(counts.values())
    if not n:
        return 0.0
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def structural_report(lines: tuple[VoynichLine, ...]) -> StructuralReport:
    tokens = [t for line in lines for t in line.tokens]
    counts = Counter(tokens)
    initials = Counter(t[0] for t in tokens if t)
    finals = Counter(t[-1] for t in tokens if t)
    adjacency_counts: Counter[tuple[str, str]] = Counter()
    for line in lines:
        adjacency_counts.update(zip(line.tokens, line.tokens[1:]))

    repeated = tuple(sorted(((t, c) for t, c in counts.items() if c > 1), key=lambda x: (-x[1], x[0])))
    adjacency = tuple(sorted(((a, b, c) for (a, b), c in adjacency_counts.items() if c > 1), key=lambda x: (-x[2], x[0], x[1])))
    lengths = [len(t) for t in tokens]

    return StructuralReport(
        line_count=len(lines),
        token_count=len(tokens),
        unique_tokens=len(counts),
        repeated_tokens=repeated,
        initial_counts=tuple(initials.most_common()),
        final_counts=tuple(finals.most_common()),
        token_length_mean=(sum(lengths) / len(lengths)) if lengths else 0.0,
        token_length_entropy=_entropy(lengths),
        adjacency=adjacency,
    )


def permutation_null(lines: tuple[VoynichLine, ...], seed: int = 1) -> tuple[VoynichLine, ...]:
    """Shuffle tokens within each line, preserving vocabulary, counts, and line lengths.

    Any statistic unchanged by this null cannot be evidence for within-line token order.
    """
    rng = random.Random(seed)
    result: list[VoynichLine] = []
    for line in lines:
        tokens = list(line.tokens)
        rng.shuffle(tokens)
        result.append(VoynichLine(line.locus, ".".join(tokens), tuple(tokens)))
    return tuple(result)


def character_permutation_null(lines: tuple[VoynichLine, ...], seed: int = 1) -> tuple[VoynichLine, ...]:
    """Shuffle characters inside tokens while preserving token lengths and character inventory."""
    rng = random.Random(seed)
    result: list[VoynichLine] = []
    for line in lines:
        out: list[str] = []
        for token in line.tokens:
            chars = list(token)
            rng.shuffle(chars)
            out.append("".join(chars))
        result.append(VoynichLine(line.locus, ".".join(out), tuple(out)))
    return tuple(result)
