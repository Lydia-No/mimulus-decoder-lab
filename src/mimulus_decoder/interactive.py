"""Local interactive workspace using the existing encoder and decoder code."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from uuid import uuid4

from .decoders import explicit_mapping_decoder, token_structure_decoder
from .encoding import encode_tokens
from .model import DecoderContext, Observation, compare_readings
from .recovery import evaluate_recovery

MAX_BODY = 32768


def _mapping(value: object, name: str) -> dict[str, str]:
    if not isinstance(value, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) or not k or not v
        or any(c.isspace() for c in k + v) for k, v in value.items()
    ):
        raise ValueError(f"{name} must contain single nonempty token pairs")
    return dict(value)


def analyze(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise ValueError("Provide an analysis object")
    mode = payload.get("mode")
    source = payload.get("source")
    if mode not in ("known", "opaque"):
        raise ValueError("Choose known-source or opaque-text mode")
    if not isinstance(source, str) or not source.split():
        raise ValueError("Enter source tokens")
    if len(source) > 16000:
        raise ValueError("Source exceeds the workspace limit")
    source_id = f"interactive-{uuid4()}"
    fixture = None
    if mode == "known":
        allow_lossy = payload.get("allow_lossy", False)
        if not isinstance(allow_lossy, bool):
            raise ValueError("Lossy encoding must be explicitly selected")
        fixture = encode_tokens(source_id, "interactive-substitution-v1", tuple(source.split()),
                                _mapping(payload.get("encoder"), "Encoder"), allow_lossy=allow_lossy)
        observation = fixture.observation()
    else:
        observation = Observation(source_id, source)
    readings = [explicit_mapping_decoder(observation, DecoderContext(name),
                                        _mapping(payload.get(key), name))
                for name, key in (("Decoder A", "decoder_a"), ("Decoder B", "decoder_b"))]
    results = []
    for reading in readings:
        recovery = evaluate_recovery(fixture, reading) if fixture else None
        results.append({
            "reading": asdict(reading),
            "recovery": ({**asdict(recovery), "token_accuracy": recovery.token_accuracy,
                          "exact_recovery": recovery.exact_recovery} if recovery else None),
        })
    return {
        "version": "interactive-decoder-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "observation": asdict(observation),
        "reference": asdict(fixture) if fixture else None,
        "results": results,
        "comparison": asdict(compare_readings(readings)),
        "structure": asdict(token_structure_decoder(observation, DecoderContext("Structure"))),
        "boundary": "Agreement does not establish correct meaning. Recovery scores require a known reference.",
    }


class WorkspaceHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass

    def _send(self, status: int, content: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        if self.path != "/":
            self._send(404, b"Not found", "text/plain")
            return
        self._send(200, files("mimulus_decoder").joinpath("decoder.html").read_bytes(), "text/html; charset=utf-8")

    def do_POST(self) -> None:
        if self.path != "/analyze":
            self._send(404, b"Not found", "text/plain")
            return
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            self._send(415, b'{"error":"Send JSON"}', "application/json")
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_BODY:
                raise ValueError("Request must contain at most 32 KiB of JSON")
            report = analyze(json.loads(self.rfile.read(size)))
        except (ValueError, UnicodeError) as error:
            self._send(400, json.dumps({"error": str(error)}).encode(), "application/json")
            return
        self._send(200, json.dumps(report).encode(), "application/json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Start the local Mimulus interactive decoder")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), WorkspaceHandler)
    print(f"Mimulus decoder: http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
