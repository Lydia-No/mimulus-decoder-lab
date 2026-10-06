# Pilot 001 — decoder persistence laboratory

Open `index.html` in a browser with `engine.js` beside it. No installation, account, API key or network connection is required.

This is the known-answer gate before historical Voynich material. Three materially different decoder families inspect the same frozen synthetic source:

1. **local delta** — proposes boundaries from large adjacent changes;
2. **motif recurrence** — proposes boundaries from a repeated prefix/suffix unit;
3. **history adaptive** — uses retained mean change from prior exposure; the family result is the consensus of two cloned observers.

The UI hides decoder assumptions by default and exposes only blind codes (`Q7`, `L4`, `N9`) for the comparison view. Assumptions can be revealed for audit.

## Source conditions

- **original** — frozen A–B–A known-answer source;
- **permuted** — preserves value counts while destroying the A–B–A order;
- **ablated** — preserves the known block positions while removing the large middle-block contrast.

## Experimental classifications

The meta-observer labels candidate boundaries as:

- `SOURCE_SUPPORTED_INVARIANT`
- `DECODER_DEPENDENT_SUPPORTED`
- `DECODER_DEPENDENT_UNSUPPORTED`
- `SHARED_UNSUPPORTED`
- `MISSED_SOURCE_FEATURE`

These are experimental result labels, not ArcTopia canonical terminology.

## History controls

The history-aware family is checked under different retained histories, reset, swapped histories and identical histories. A designed history-control pattern requires:

- trained observers diverge;
- reset observers converge;
- identical-history observers converge;
- swapping retained histories exchanges the outputs.

The targeted ablation is expected to remove that pattern by removing the contrast on which this simple history rule acts.

## Validation

Run:

```bash
node test.js
```

The assertions verify the known-answer invariant case, decoder-dependent case, unsupported structure after order destruction, targeted ablation behavior, history-control pattern and the complete 12-cell matrix.

This is deterministic measurement validation. Re-running the same cell is reproducibility, not an independent replicate. No empirical cognition, general-theory or Voynich decipherment claim follows.

Research direction, conceptual framing and methodology: Linda Thorstensen.
