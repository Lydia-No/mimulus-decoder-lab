# OBS-003 — Semantic relay / chained translation

Status: **NATURALISTIC / NON-BLIND / EXCLUDED FROM CLEAN FIXTURE**

This observation records a downstream translation step in the same naturalistic Voynich-decoder exploration captured by OBS-001 and OBS-002.

It is evidence about **lineage dependence in decoder outputs**, not evidence that the Voynich source has been deciphered and not independent corroboration of the earlier Sumerian-looking intermediate representation.

## Capture identities

### Capture A — downstream language output

- source file: `CE92CB13-707F-47A1-8CBF-3AC0692B9CD1.jpeg`
- SHA-256: `e09705cf96fa576349ee0e795e1a247f7357f64bba27a04e89a1920065137128`
- visible page header: `Sumerian Tra...`
- visible host: `polytranslator.com`
- visible output contains Latin-script forms such as `Aka pachanakaniamawa`, `taqe`, `inti`, `uka`, `uñstani`, `ch'amapampi`, and related text.

No language identification is treated as a source fact in this record. The visible form is simply preserved as a downstream decoder/translator output.

### Capture B — lineage context

- source file: `7B1AB4BB-93CD-4B8E-BC0F-79CC682DCB24.jpeg`
- SHA-256: `364c466cfe6bb239fcba533da82110097ad4d078ca4cac49232499d0c543912a`
- Discord screenshot shows the previously produced Sumerian-looking intermediate output and English rendering from OBS-002.
- A participant then states: `then I retranslated this into the language near lake titticaca- Arymaya I think- where other Shinning Ones landed`

The statement is recorded as **reported transformation lineage**, not as verified linguistic or historical information.

## Observed lineage

The available evidence indicates the following naturalistic chain was intended:

`opaque source / prior decoder output`
→ `Sumerian-looking intermediate representation`
→ `English rendering`
→ `downstream translation into another language-like representation`

The exact prompts, model state, source crop, translator settings, and whether the final translation consumed the English output or another intermediate representation are not yet fully reconstructed. Therefore the lineage is recorded with uncertainty rather than treated as a fully specified pipeline.

## Mimulus classification

Provisional labels:

- `DERIVED_FROM_DECODER_OUTPUT`
- `LINEAGE_DEPENDENT`
- `SEMANTIC_RELAY` — exploratory label for this naturalistic observation
- `NOT_INDEPENDENT_DECODER`
- `NOT_SOURCE_CONSTRAINED_RESIDUE`
- `CONTEXT_INCOMPLETE`

The key methodological rule is:

> A translation or transformation of a previous decoder output is not an independent decoder of the original source.

Semantic persistence across a relay may demonstrate preservation by the translation chain. It does not, by itself, demonstrate independent convergence on the opaque source.

## Why this matters

A relay can create an **illusion of corroboration**:

1. decoder A produces a semantically rich interpretation;
2. translator B preserves or reformulates that semantic content;
3. translator C preserves it again in another language;
4. repeated motifs across outputs may then appear to be cross-language confirmation.

But all downstream outputs may inherit the same upstream commitment. The effective number of independent source decoders remains one.

This is different from OBS-002's failure mode. OBS-002 concerns a plausible-looking intermediate language layer whose provenance from the source is unverified. OBS-003 concerns the **propagation of an already introduced semantic structure through downstream transformations**.

## Independence criterion

For two outputs to contribute independent Mimulus evidence about the opaque source, each must:

1. receive the original frozen source or independently frozen source representation;
2. receive its own declared decoder context;
3. not receive semantic conclusions, transliterations, translations, mappings, or inferred structures produced by the other decoder;
4. be frozen before cross-output comparison;
5. expose provenance linking claims to source observations and decoder assumptions.

If output B consumes output A, then B may be useful for studying transformation fidelity, semantic drift, attractors, or compression — but it does not increase the count of independent decoders.

## Controlled replay implied by OBS-003

A later experiment should compare at least three conditions:

### R1 — independent-source condition

Run two materially different decoders independently on the same frozen original source representation. Neither sees the other's output.

Question: what, if anything, converges independently?

### R2 — relay condition

Run decoder A on the original source, then feed A's frozen output to translator/decoder B.

Question: how much semantic structure is preserved, amplified, normalized, or replaced through the relay?

### R3 — null relay condition

Feed B a matched synthetic or semantically perturbed upstream output with similar surface properties.

Question: does B produce comparable thematic coherence even when the upstream semantics are deliberately altered?

The contrast `R1 vs R2` distinguishes **independent convergence** from **inherited semantic persistence**.

## Interpretation boundary

This observation does not establish:

- that the displayed downstream language is correctly identified;
- that the intermediate Sumerian-looking representation is valid;
- that the English rendering is faithful;
- that any repeated mythology, cosmology, divine names, geography, or cultural association comes from the Voynich source;
- that survival of a theme across chained translations increases confidence in source meaning.

It establishes only that a naturalistic workflow introduced at least one downstream transformation of prior decoder output, creating a lineage in which semantic persistence cannot be counted as independent corroboration.

## Separation from clean experiment

Do not expose OBS-003, its screenshots, its intermediate outputs, its reported language choice, or its semantic themes to the blind f113v fixture or any decoder intended to contribute independent evidence in Experiment 001.
