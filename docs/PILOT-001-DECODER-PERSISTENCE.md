# Pilot 001 — decoder persistence gate

Status: deterministic known-answer measurement validation.

## Question

Can Mimulus distinguish structure that is supported by a frozen source and persists across materially different decoder families from structure that is decoder-dependent or unsupported?

This pilot validates the measurement scaffold before historical Voynich runs. It does not test a decipherment hypothesis.

## Frozen fixture

Fixture: `fixtures/synthetic/pilot-001-decoder-persistence/source.json`

The original source contains three four-value blocks arranged A–B–A, with known boundaries at zero-based indices 4 and 8.

Two interventions accompany the original source:

- a count-preserving permutation that destroys the A–B–A order;
- a targeted ablation that removes the large middle-block contrast while preserving the controlled block positions.

The answer key is retained independently of decoder outputs.

## Decoder families

### Q7 — local delta

Assumption: a boundary is indicated by an adjacent numeric change greater than 3.

### L4 — motif recurrence

Assumption: a repeated prefix/suffix motif indicates a recurrent outer unit and brackets an intervening unit.

### N9 — history adaptive

Assumption: a boundary is a change larger than the observer's retained mean adjacent change from prior exposure.

Two cloned observers receive different, reset, swapped or identical histories. The decoder-family output used by the meta-observer is their boundary intersection; their individual outputs remain preserved for audit.

The blind codes are comparison labels only. The decoder mapping remains inspectable in the full run record.

## Meta-observer classifications

For every boundary in either the answer key or at least one decoder output, record:

- whether it is in the frozen known answer;
- which decoder families propose it;
- the number of supporting families;
- one experimental classification.

Classification rules:

- all families + known answer → `SOURCE_SUPPORTED_INVARIANT`;
- subset of families + known answer → `DECODER_DEPENDENT_SUPPORTED`;
- no family + known answer → `MISSED_SOURCE_FEATURE`;
- all families + absent from answer key → `SHARED_UNSUPPORTED`;
- subset of families + absent from answer key → `DECODER_DEPENDENT_UNSUPPORTED`.

Agreement therefore never becomes evidence merely because several decoders agree.

## History-control test

The declared pattern is present only when:

1. differently trained observers diverge;
2. reset observers converge;
3. identical-history observers converge;
4. swapping retained histories exchanges the outputs.

This demonstrates that the synthetic output difference follows retained state under the declared deterministic rule. It is not evidence of human memory, cognition or learning.

## Expected falsification behavior

The scaffold should fail its intended gate if, for example:

- the permuted source is classified as source-supported merely because multiple decoders hallucinate boundaries;
- removing the local contrast does not alter the contrast-sensitive decoder as declared;
- reset fails to remove the designed history divergence;
- swapping retained histories fails to exchange history-conditioned outputs;
- answer-key disagreement is hidden by semantic or narrative interpretation.

## Historical gate

Passing this deterministic fixture only establishes that the implementation can represent the intended distinctions on a known-answer case. It does not establish transport to historical manuscripts.

Voynich remains separately governed by `docs/EXPERIMENT-001-VOYNICH.md` and `docs/SOURCE-PROVENANCE.md`.

Research direction, conceptual framing and methodology: Linda Thorstensen.
