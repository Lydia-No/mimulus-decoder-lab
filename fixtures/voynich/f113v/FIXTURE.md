# Frozen fixture — f113v

Status: **SOURCE-LOCK / PRE-DECODER**

This fixture instantiates `docs/EXPERIMENT-001-VOYNICH.md` on one fixed source lineage. It is not a decipherment record and does not import an external Voynich theory into the experiment.

## Fixture identity

- fixture id: `voynich-f113v-001`
- external identifier: `f113v` — metadata only; the identifier carries no semantic assumptions into decoder runs
- provenance capture: user-supplied screenshot
- provenance filename: `4C485E75-FE73-453E-BFC6-D8CEDBA1656B.jpeg`
- provenance dimensions: `1536 x 1151`
- provenance SHA-256: `bccf2e0fdf11d6040ab87d55701eb23e2b6effc9e4ea5ad24c4aaf9e8a27f1c1`

The screenshot is the immutable **provenance capture (`R0`)**, not automatically the analytical source. It contains interface framing around the manuscript image.

Any analytical representation must descend from `R0` through an explicit transformation record. A crop, rotation, rescale, contrast change, transcription, segmentation, tokenization, glyph grouping, or normalization is a **derived representation** and must be versioned with:

- parent representation id;
- exact transform or rule;
- parameters;
- output identity/hash where applicable;
- uncertainty or manual judgment introduced;
- whether the transform was fixed before decoder outputs were seen.

No decoder may silently redefine its input representation.

## Representation lineage

The fixture distinguishes representation stages so preprocessing cannot masquerade as cross-decoder agreement.

### R0 — provenance capture

The exact user-supplied screenshot identified above. It preserves provenance and context but includes non-manuscript UI.

### R1 — manuscript-region representation

A content-region representation derived from `R0` by a recorded crop/mask transform. Its transform must be frozen before blind decoder runs begin.

`R1` may not include semantic labels or a transcription.

### R2 — mark-level representation

Optional. Records visually separable marks or strokes with neutral ids and source coordinates. No grouping into lexical or functional units is assumed.

### R3 — candidate glyph representation

Optional. Groups marks into candidate glyph units. Every grouping rule and ambiguity must be explicit. Different plausible segmentations may coexist as separate representation branches rather than being collapsed.

### R4 — candidate sequence / transcription representation

Optional. Encodes ordered candidate glyph units into neutral symbols or a declared transcription convention. It is never treated as ground truth merely because multiple decoders consume it.

The intended lineage is therefore:

`R0 pixels → R1 manuscript region → R2 marks → R3 candidate glyphs → R4 candidate sequences`

Every arrow is a modelled transformation, not a free observation.

A decoder may consume an earlier representation directly. Agreement that appears only after `R3` or `R4` must be tested for preprocessing dependence before it can count as source-constrained residue.

## Contamination boundary

Before the independent decoder runs are frozen, do not encode the following as source facts:

- a proposed language;
- a proposed plaintext or translation;
- a proposed manuscript purpose or genre;
- historical interpretations of this folio;
- claims imported from Voynich scholarship about paragraph grammar, positional morphology, recipes, stars, gallows, or token meaning;
- conclusions from another Mimulus decoder run.

Such material may later be introduced as an explicitly labelled **external prior** in a separate decoder context. It must never be silently merged into the observation layer.

## Observation layer

The observation pass may record only features recoverable from the declared input representation, with the representation stage named.

Examples:

- visible spatial marks and their coordinates at `R1`/`R2`;
- candidate line or region boundaries, with uncertainty;
- repeated visual configurations at the representation stage actually used;
- exact or approximate recurrence relations;
- local adjacency and position;
- ambiguity where a mark, glyph, boundary, or grouping cannot be distinguished reliably.

Do not name a feature by presumed function. For example, record `left-margin visual marker` rather than `entry marker`; record `candidate sequence G17` rather than a lexical gloss.

A phrase such as `repeated glyph sequence` is not a primitive observation unless the glyph segmentation itself has already been declared and frozen. At earlier stages record repeated visual configurations instead.

No transcription is authoritative merely because it is convenient. If a transcription is introduced, record its convention, source, uncertainty, and mapping back through the representation lineage.

## Pre-decoder observation freeze

Before D0–D4 begin, freeze:

1. the allowed representation branches;
2. every transformation from `R0` to those branches;
3. ambiguity annotations;
4. the preregistered control transforms in `CONTROLS.md`.

Decoders may challenge a segmentation by consuming an earlier representation or an alternative pre-frozen branch. They may not silently repair or reinterpret preprocessing after seeing attractive output.

## Initial decoder set

The first pass is deliberately narrow. It tests the Mimulus mechanism before attempting semantic translation.

Decoder names alone do not establish independence. Each decoder has an **information budget** that constrains what it may consume.

### D0 — null / recurrence baseline

Permitted input: `R1`, and optionally `R2` if frozen independently of D0.

May use:

- counts;
- raw spatial positions;
- distances/adjoining relations;
- recurrence of neutral visual configurations;
- preregistered permutation/null controls.

May not use:

- candidate token meaning;
- externally supplied grammar;
- D1–D4 groupings or conclusions.

Produces no semantic reading.

### D1 — layout / segmentation decoder

Permitted input: `R1` and optionally `R2`.

May infer candidate grouping or boundary structure from spatial organization.

May not use:

- token meaning;
- historical claims;
- `R3`/`R4` segmentation created by another decoder;
- another decoder's candidate boundaries.

Its purpose is to propose segmentation rather than inherit it.

### D2 — symbolic relation decoder

Permitted input: one explicitly frozen `R3` or `R4` branch, plus the mapping back to source.

May infer relations among recurring neutral candidate units and positions. It may assign neutral identifiers or explicit operators but no natural-language meanings.

May not use:

- D1 conclusions unless the chosen representation branch was frozen before D1 ran;
- D3 state variables or operators;
- semantic/historical priors.

### D3 — state / transformation decoder

Permitted input: a declared frozen representation branch, preferably one not produced by D3 itself.

May test whether observations are parsimoniously represented as transformations over a state. Any state variables and operators are decoder-supplied and must be exposed explicitly.

May not treat D2's symbolic relations as observations. If reused in a later secondary run, they must be labelled inherited decoder structure and cannot contribute independent evidence.

### D4 — adversarial/null competitor

Permitted input: the same declared representation used by the target claim plus preregistered perturbed/null variants.

Attempts to reproduce apparent regularity after controlled disruptions or under an alternative equally explicit rule set. Its purpose is to identify structure that a flexible decoder could manufacture.

A natural-language or historical decoder is **not** part of the first pass. It may be added only after the source/structure pass is frozen, so semantic fluency cannot steer what the experiment decides is structurally present.

## Independence rule for this fixture

Each decoder receives:

1. one explicitly named frozen representation branch;
2. its own declared information budget and decoder context;
3. no candidate conclusions from the other decoders;
4. no post-hoc preprocessing changes made in response to decoder output.

Runs are frozen before the meta-observer compares them.

Two outputs do **not** count as independent evidence merely because they came from different decoder labels. The meta-observer must record shared representation ancestry and shared assumptions.

## Evidence dependency rule

When two decoders agree, the meta-observer must ask whether the agreement is already encoded upstream.

Examples:

- agreement inherited from the same `R4` tokenization is evidence about that tokenization branch, not automatically about `R0`;
- agreement inherited from the same segmentation cannot independently validate that segmentation;
- agreement surviving materially different representation branches is stronger than agreement within one branch.

Cross-decoder residue must therefore carry a **dependency trace** back through representation ancestry.

## Meta-observer labels

The meta-observer may emit only the following evidence-status labels initially:

- `SOURCE_CONSTRAINED_RESIDUE` — survives materially different decoder contexts, is not explained by shared preprocessing ancestry, and can be traced to source features;
- `DECODER_DEPENDENT` — changes or disappears when decoder assumptions change;
- `PREPROCESSING_DEPENDENT` — depends on crop, transcription, segmentation, normalization, tokenization, or another shared transform;
- `UNDERDETERMINED` — multiple incompatible readings remain equally supported;
- `CONTAMINATED` — a run used knowledge it was not supposed to receive;
- `NO_RESIDUE` — no non-trivial cross-decoder result survives.

`SOURCE_CONSTRAINED_RESIDUE` is not equivalent to historical meaning or decipherment.

## Required interventions

Controls are preregistered in `CONTROLS.md` **before** decoder output is inspected.

For every non-trivial candidate claim, the decoder must state in advance which source relation is believed to support it and which preregistered intervention should weaken or destroy the claim.

A claimed source relation should weaken or disappear when its supporting source relation is destroyed. If it does not, treat the claim as decoder-generated or underdetermined until shown otherwise.

Post-hoc controls may be added, but they must be labelled exploratory and cannot replace the preregistered tests.

## First question

Do materially different non-semantic decoders, operating under distinct information budgets and representation ancestries, recover any of the same structural distinctions from this source lineage, and do those distinctions survive preregistered matched controls without being explained by shared preprocessing?

That question is intentionally narrower than `What does f113v say?`.

## Freeze condition

This file fixes the experimental boundary, not the result. Any later addition of observations, transcription, decoder output, semantic hypotheses, or external scholarship must be added as a new versioned artifact rather than rewritten into this source-lock record.
