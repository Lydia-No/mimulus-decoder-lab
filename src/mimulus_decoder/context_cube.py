"""A Q4 graph of declared decoder interventions over one fixed observation."""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Mapping

from .decoders import explicit_mapping_decoder
from .encoding import EncodedFixture
from .model import DecoderContext, Observation, compare_readings
from .recovery import evaluate_recovery

AXES = (
    {"id": "mapping", "label": "Base mapping", "choices": ("A", "B")},
    {"id": "coverage", "label": "Mapping coverage", "choices": ("Keep all", "Withhold first symbol")},
    {"id": "assignment", "label": "Target assignment", "choices": ("Declared", "Rotate targets")},
    {"id": "frequency", "label": "Symbol filter", "choices": ("All observed", "Repeated only")},
)


def context_hypercube(observation: Observation, mapping_a: Mapping[str, str],
                      mapping_b: Mapping[str, str], fixture: EncodedFixture | None = None) -> dict[str, object]:
    """Compare 16 explicit contexts, not 16 independent learned decoders.

    Bit k selects choice 0/1 on AXES[k]. Transform order is fixed: choose
    base, rotate targets over sorted mapping keys, withhold first observed
    symbol, filter to repeated symbols. The source is never transformed.
    """
    tokens = observation.transcription.split()
    counts = Counter(tokens)
    nodes = []
    readings = []
    for vertex in range(16):
        bits = tuple((vertex >> axis) & 1 for axis in range(4))
        mapping = dict(mapping_b if bits[0] else mapping_a)
        if bits[2] and mapping:
            keys = sorted(mapping)
            values = [mapping[k] for k in keys]
            mapping = dict(zip(keys, values[1:] + values[:1]))
        if bits[1] and tokens:
            mapping.pop(tokens[0], None)
        if bits[3]:
            mapping = {key: value for key, value in mapping.items() if counts[key] > 1}
        node_id = "".join(map(str, bits))
        context = DecoderContext(f"cube-{node_id}", {
            axis["id"]: axis["choices"][bit] for axis, bit in zip(AXES, bits)
        })
        reading = explicit_mapping_decoder(observation, context, mapping)
        readings.append(reading)
        score = evaluate_recovery(fixture, reading) if fixture else None
        nodes.append({"id": node_id, "vertex": vertex, "bits": bits,
                      "assumptions": dict(context.assumptions), "mapping": mapping,
                      "reading": asdict(reading),
                      "recovery": ({**asdict(score), "token_accuracy": score.token_accuracy,
                                    "exact_recovery": score.exact_recovery} if score else None)})
    edges = []
    for vertex in range(16):
        for axis in range(4):
            neighbor = vertex ^ (1 << axis)
            if vertex < neighbor:
                edges.append({"from": nodes[vertex]["id"], "to": nodes[neighbor]["id"],
                              "axis": AXES[axis]["id"],
                              "comparison": asdict(compare_readings([readings[vertex], readings[neighbor]]))})
    return {"version": "decoder-context-q4-v1", "dimensions": 4,
            "source_id": observation.source_id, "axes": AXES,
            "nodes": nodes, "edges": edges,
            "boundary": "Declared interventions can yield identical mappings. Vertices are not independent empirical runs; geometry does not establish meaning."}
