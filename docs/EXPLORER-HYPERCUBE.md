# Explorer hypercube integration

Explorer links to `hypercube.html`, a deterministic browser workspace using the
same four declared token-context axes as the Python workspace. No server-side
Python, API key, or model request is required. Source tokens and explicit mappings
remain in the browser; exporting a record is the persistence step.

The browser adapter implements the token decoder separately, with a CI parity
check against all 16 Python contexts. This is explicit mapping comparison, not
an automatic decoder or an image experiment. The source identifier hashes the
normalized encoded token sequence (UTF-8, single-space separators), not original
image bytes, raw formatting, or historical authenticity. Known originals and
codebooks remain evaluator fields; opaque inputs receive no accuracy.

The `beqube` export is a local adapter to the structural record types in
MIMULUS-V1-SCHEMA.md, not a connection to a separately deployed beQube engine.
It contains Source/Representation pointers, Context and Run records, state
snapshots, Intervention records, and BeQubeTransition pointers. Each one-bit move
records a context swap with before/intervention/after references. Direct jumps
remain inspection events, not one-axis transitions. History is explicitly none;
inspection chronology does not change subsequent decoder outputs. Navigation
cannot upgrade a run to independent evidence or source-constrained residue.

Both Vercel rewrites and the cPanel package/deploy builders include the browser
assets. This change prepares deployment artifacts; it does not deploy the site.
Frozen image results, protocols, and decoders remain separate.
