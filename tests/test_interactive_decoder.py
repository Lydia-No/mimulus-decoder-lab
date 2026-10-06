import json
from importlib.resources import files

import pytest

from mimulus_decoder.interactive import analyze


def payload():
    return {"mode": "known", "source": "sun water sun stone",
            "encoder": {"sun": "q", "water": "x", "stone": "z"},
            "decoder_a": {"q": "sun", "x": "water", "z": "stone"},
            "decoder_b": {"q": "king", "x": "war", "z": "crown"}}


def test_interactive_recovery_uses_real_backend_and_preserves_trace():
    report = analyze(payload())
    assert report["observation"]["transcription"] == "q x q z"
    assert report["results"][0]["recovery"]["token_accuracy"] == 1
    assert report["results"][1]["recovery"]["token_accuracy"] == 0
    assert report["comparison"]["outcome"] == "divergence"
    assert json.loads(json.dumps(report))["reference"]["original_tokens"] == ["sun", "water", "sun", "stone"]


def test_shared_wrong_keys_agree_but_fail_recovery():
    data = payload()
    data["decoder_a"] = data["decoder_b"]
    report = analyze(data)
    assert report["comparison"]["outcome"] == "convergence"
    assert all(r["recovery"]["token_accuracy"] == 0 for r in report["results"])


def test_opaque_mode_never_invents_reference_or_accuracy():
    data = {"mode": "opaque", "source": "q x q", "decoder_a": {"q": "sun"}, "decoder_b": {}}
    report = analyze(data)
    assert report["reference"] is None
    assert all(r["recovery"] is None for r in report["results"])
    assert report["results"][0]["reading"]["semantic_reading"] == "sun [x] sun"


def test_lossy_mode_requires_explicit_choice_and_reports_collisions():
    data = payload()
    data["encoder"]["water"] = "q"
    with pytest.raises(ValueError, match="allow_lossy"):
        analyze(data)
    data["allow_lossy"] = True
    report = analyze(data)
    score = report["results"][0]["recovery"]
    assert score["token_accuracy"] == 0.75
    assert score["collision_groups"]


@pytest.mark.parametrize("key,value", [("mode", "invented"), ("source", ""),
    ("source", 42), ("decoder_a", {"q": "two words"}), ("decoder_b", []),
    ("encoder", {"sun": ""}), ("allow_lossy", "false")])
def test_invalid_inputs_are_rejected(key, value):
    data = payload()
    data[key] = value
    with pytest.raises(ValueError):
        analyze(data)


def test_page_is_bundled_with_python_package():
    assert files("mimulus_decoder").joinpath("decoder.html").is_file()
