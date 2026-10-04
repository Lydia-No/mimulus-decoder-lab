"""Run fixed synthetic controls: python -m mimulus_decoder.benchmark."""
from __future__ import annotations

import json
from dataclasses import asdict

from .decoders import explicit_mapping_decoder
from .encoding import encode_tokens
from .model import DecoderContext, compare_readings
from .recovery import evaluate_recovery


def run_benchmark() -> dict[str, object]:
    reversible = encode_tokens("synthetic-reversible-v1", "substitution-v1",
                               ("sun", "water", "sun", "stone"),
                               {"sun": "q", "water": "x", "stone": "z"})
    lossy = encode_tokens("synthetic-lossy-v1", "collision-v1",
                         ("sun", "water", "sun", "stone"),
                         {"sun": "q", "water": "q", "stone": "z"}, allow_lossy=True)
    controls = (
        ("matching-key", reversible, {"q": "sun", "x": "water", "z": "stone"}),
        ("wrong-key-a", reversible, {"q": "king", "x": "war", "z": "crown"}),
        ("wrong-key-b", reversible, {"q": "king", "x": "war", "z": "crown"}),
        ("incomplete-key", reversible, {"q": "sun"}),
        ("lossy-choice", lossy, {"q": "sun", "z": "stone"}),
    )
    results = []
    readings = {}
    for decoder_id, fixture, mapping in controls:
        reading = explicit_mapping_decoder(fixture.observation(), DecoderContext(decoder_id), mapping)
        readings[decoder_id] = reading
        score = evaluate_recovery(fixture, reading)
        results.append({**asdict(score), "token_accuracy": score.token_accuracy,
                        "exact_recovery": score.exact_recovery})
    agreement = compare_readings([readings["wrong-key-a"], readings["wrong-key-b"]])
    return {
        "benchmark": "synthetic-token-controls-v1",
        "scope": "Known-key software controls; no learned or blind decipherment claim.",
        "results": results,
        "shared_wrong_key_agreement": agreement.outcome.value,
    }


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2))
