# PolyTranslator pilot — controlled comparison

Status: prospective protocol; no runs or findings reported.
Research direction and methodology: Linda Thorstensen.
Related: issues #5 and #6; EXPERIMENT-001-VOYNICH.md.

## Recovery boundary

The original PolyTranslator implementation, prompts, language frames and outputs have not been inspected for this protocol. Earlier conversational descriptions are recovery leads, not verified implementation history. A new implementation is a reconstruction until checked against original artifacts.

## Two separately controlled experiments

| Condition | Held fixed | Changed | Primary comparison |
| --- | --- | --- | --- |
| Context | Source, model/version, memory, generation settings | Declared decoder frame | Between-frame difference versus within-frame variability |
| History | Source, model/version, decoder frame, generation settings | Retained state from prior exposure | History-conditioned difference versus reset and swapped-memory controls |

Do not infer a history mechanism from a context experiment. A memory intervention changes the observer's current internal state; identical external input does not mean identical complete system state.

## First fixture: known-answer synthetic material

Before Voynich, use a synthetic symbolic source with an independently retained generating rule and known answer. Freeze the source, generating rule, expected structural claims and transformations before decoder runs. Give the decoder only the source, not the answer key.

Use at least three source conditions:
- original;
- a seeded permutation preserving symbol counts but disrupting order;
- a targeted ablation of a feature named in a decoder's predeclared prediction.

A permutation cannot test a count-only claim. Select a perturbation that actually changes the feature on which each claim depends.

The fixture tests measurement and source sensitivity. It does not establish transport to historical manuscripts.

## Candidate record

Every run records:
- exact source and source hash;
- exact prompt, decoder specification and version;
- model/version, settings, run identifier and any available seed;
- supplied memory and its hash, or explicit empty memory;
- observed spans with start/end offsets under a declared indexing convention;
- proposed segmentation;
- each claim, its supporting spans, declared assumptions and alternatives;
- confidence, marked as self-reported rather than calibrated;
- raw output, parse failures and missing fields.

A span citation proves that a claim points somewhere, not that the cited evidence supports it. Support requires independent adjudication.

## Freeze and blind

Freeze runs before comparison. Replace frame labels with random codes and retain the mapping separately. Blind adjudicators to frame and source condition where feasible; record when wording reveals the frame. Use an independently specified scoring rubric, and do not let the generating process silently adjudicate its own semantic correctness.

## Minimal measurements

1. Segmentation: exact boundary-set Jaccard; report both empty sets separately as no proposed boundaries.
2. Direct source observations: correctness against the synthetic key, separate from inferred semantics.
3. Unsupported claims: independently adjudicated unsupported claims divided by adjudicable claims; report the denominator and unadjudicable claims.
4. Source sensitivity: paired changes after targeted perturbation, compared with the predeclared prediction.
5. Decoder dependence: between-frame differences compared with repeated runs under the same frame.
6. Known-answer performance: score held-out material without changing the decoder after viewing its key.

Use at least five repeats per cell for an exploratory pilot. This is a practical starting point, not a powered sample size or a significance guarantee. Preserve all runs; predeclare exclusions.

## History arm

Begin with cloned identical observers. Expose them to different training histories using the same update rule. Retain only the state actually produced by that rule. Present exactly the same probe source.

Run:
- differing retained memories;
- reset memory for both;
- exchanged retained memories;
- repeated identical histories.

Decoder access excludes trajectory IDs, condition names, step labels, and the hidden answer key. Log the complete allowed input. If retained memory consists of raw examples, describe this as exemplar conditioning; do not claim learned structural change without an implemented and inspected update mechanism.

## What would count against the proposal?

- Between-frame differences are no larger than same-frame run variability.
- Claimed order-dependent interpretations survive order destruction unchanged.
- Semantic coherence remains high while known-answer accuracy fails.
- History effects persist after reset, suggesting uncontrolled differences.
- Output follows a visible condition label rather than retained content.
- Agreement vanishes under independent adjudication or is explained by shared priors.

Divergence alone is a manipulation check. Meaningful evidence requires the controls to distinguish source dependence from imposed priors, stochastic variability and label leakage.

## Next implementation deliverable

A small interactive runner should expose the unchanged source, declared decoder assumptions, retained state, generated candidates and blinded comparison as separate inspectable records. Export the complete run bundle. Use synthetic fixtures first; enable Voynich only after source provenance and transcription uncertainty are recorded.

The 1936 material remains an external historical analogy in issue #5. It supplies no decoder rule, validation evidence or conceptual provenance for this pilot.
