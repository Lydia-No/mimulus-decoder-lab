# Synthetic encoder benchmark v1

This is a bounded software benchmark with known answers. It does not infer an
unknown key, decipher Voynich, or validate the memory experiment.

## Success criteria fixed for v1

- Exact recovery: every original token is recovered in its original position.
- Token accuracy: matching positions divided by the total original positions.
- Missing explicit mappings remain unresolved and do not count as recovered.
- Agreement between decoders is reported separately from recovery accuracy.
- Codebook collisions remain visible even when one sample happens to recover.

Only one-symbol-per-token substitution is modeled. Original whitespace is not
preserved; insertion, deletion, variable-length encodings, structural recovery,
and semantic equivalence need separate specifications before being scored.

Reference construction validates nonempty equal sequence lengths, immutable
token records, unique source keys, and consistency with the recorded codebook.
Malformed references are rejected before scoring, including manually constructed
records; extra encoded tokens cannot be silently ignored as an exact recovery.

## Reference and decoder boundary

`encode_tokens` records the original token tuple, encoder identifier, encoded
symbols, and a copied codebook in an evaluator-only `EncodedFixture`. Reversible
mode rejects duplicate output symbols. A many-to-one codebook requires explicit
`allow_lossy=True` and its collisions are reported.

Pass only `fixture.observation()` to the decoder. It contains encoded symbols
and an opaque caller-chosen source identifier; it excludes the original and
codebook. Keep source identifiers free of answer hints. The evaluator receives
the reference and frozen candidate reading after decoding. The API separates
these inputs, but it does not enforce access isolation or verify independence.

Recovery is scored from explicit mapping claims. Fluent semantic text alone is
not a recovery record. The encoder and evaluator use copied immutable tuples;
existing decoder interfaces and comparison behavior are unchanged.

## Fixed controls

Input: `sun water sun stone`.

| Control | Expected token accuracy | Purpose |
| --- | --- | --- |
| Matching supplied key | 100% | Validate reversible software round trip |
| Two identical wrong keys | 0%, despite convergence | Expose misleading agreement |
| Incomplete key | 50%, two unresolved positions | Preserve uncertainty |
| Many-to-one encoding | 75% for the declared choice | Expose lost distinctions |

The matching key is deliberately supplied to the software control. An unseen
sequence test still uses that known key: it is not blind inference or evidence
of learned generalization. The benchmark performs no parameter fitting or
statistical significance testing.

Run from the repository root:

```sh
PYTHONPATH=src python -m mimulus_decoder.benchmark
python -m pytest -q
```

## Next research gate

Before testing inferred encodings, predeclare a training/held-out split,
decoder access rules, materially different encoding families, recovery metrics,
and null controls. Freeze inputs and decoder outputs before scoring. Keep the
Voynich source-policy gate separate: this synthetic benchmark does not resolve
the missing folio provenance for Experiment 001.
