# Interactive decoder workspace

Run from the repository root:

```sh
PYTHONPATH=src python -m mimulus_decoder.interactive
```

Open `http://127.0.0.1:8765`. Use `--port 8766` to choose another local port.

## Known-original mode

Enter original tokens and explicit encoding rules, then provide two decoder
mappings. The workspace calls the existing Python encoder, decoder, comparison,
and recovery evaluator. It reports both agreement and actual positional token
recovery. Presets demonstrate matching, shared incorrect, incomplete, and lossy
mappings. Unknown symbols remain unresolved. Lossy encoding requires an explicit
selection and keeps collisions visible.

## Opaque-text mode

Enter already encoded material and proposed mappings. The workspace shows
candidate readings, conflicting or shared mappings, and repeated token counts.
No original is assumed and no recovery score is generated. It does not validate
historical meaning, language, or decipherment.

## Records and boundaries

Each run gets a distinct source identifier. Inputs are disabled during a request;
changing an input afterward clears the displayed result and disables export.
Export reveals a copyable JSON record and an optional file download. Known-original exports
include the original reference and codebook; opaque exports do not manufacture
those fields. Runs are not saved automatically, and the server has no collection
or persistence endpoint. It binds only to local loopback.

The workspace is a manual comparison instrument. It does not perform automatic
key discovery or invoke external models. The supervised learner remains a
separate versioned benchmark. Token boundaries and one-token substitutions are
supplied assumptions, and whitespace formatting is not a recovery target.

Validation: 59 tests passed. Browser checks covered matching and shared wrong
keys, lossy encoding, opaque text without a reference score, copyable JSON
export, and clearing stale results after an input edit. The optional browser
file-download event was not confirmed in the in-app browser; the copyable
record is the verified export path.
