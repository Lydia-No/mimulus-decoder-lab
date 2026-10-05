# f113v decoder run template

Use one copy of this file per decoder run. Do not expose completed runs to later decoders before the experiment's independent-run freeze.

## Run identity

- fixture: `voynich-f113v-001`
- decoder id:
- decoder version:
- run id:
- date:
- provenance hash verified: `bccf2e0fdf11d6040ab87d55701eb23e2b6effc9e4ea5ad24c4aaf9e8a27f1c1`
- input representation id:
- representation parent id:
- representation transform record:
- representation hash / artifact id:

## Representation ancestry

List the complete ancestry from `R0` to the representation consumed by this decoder.

| stage | representation id | parent | transform / decision | frozen before decoder output? |
| --- | --- | --- | --- | --- |
| | | | | |

Any grouping, segmentation, tokenization, normalization, transcription, or manual correction in this ancestry is a dependency of the run and must be available to the meta-observer.

## Knowledge boundary

### Information supplied to this decoder

- 

### Explicit information budget

State what classes of information this decoder is permitted to consume.

- permitted representation stages:
- permitted spatial information:
- permitted recurrence information:
- permitted segmentation/grouping information:
- permitted symbolic/operator assumptions:
- permitted external priors:

### Information explicitly prohibited

State the decoder-specific prohibitions from `FIXTURE.md` plus any additional restrictions.

- outputs from other decoders
- proposed plaintext/translation
- external Voynich interpretations unless this run is explicitly designated as an external-prior decoder
- post-hoc preprocessing changes motivated by another run's output
- 

### Prior exposure / contamination declaration

State any relevant information the decoder already knew or saw before this run. If material prior exposure cannot be excluded, mark the run `CONTAMINATION_RISK` rather than treating it as blind.

- 

## Independence declaration

- Were any preprocessing decisions inherited from another decoder? yes / no
- If yes, identify them:
- Were any candidate conclusions from another decoder visible? yes / no
- Does this run share an `R3`/`R4` branch with another run? yes / no / unknown
- If yes, shared ancestry must not be counted as independent confirmation.

## Declared decoder context

Describe only the rules, assumptions, operators, or inference procedure this decoder is permitted to use.

- 

## Source observations used

Record observations by neutral identifier and name the representation stage on which each observation exists.

| observation id | representation stage | description | location / mapping | confidence |
| --- | --- | --- | --- | --- |
| | | | | |

Do not call a grouped sequence a direct observation if its grouping was introduced by preprocessing or the decoder.

## Decoder-supplied structure

Everything introduced by the decoder rather than directly observed belongs here.

| assumption / operator id | description | rationale |
| --- | --- | --- |
| | | |

## Candidate claims

Do not collapse structural claims into semantic claims.

| claim id | claim | evidence status | provenance | upstream dependencies |
| --- | --- | --- | --- | --- |
| | | | | |

Allowed provisional evidence statuses inside a run:

- `DIRECT_OBSERVATION`
- `PREPROCESSING_SUPPLIED`
- `DECODER_SUPPLIED`
- `DERIVED`
- `UNRESOLVED`
- `CONTAMINATION_RISK`

Cross-decoder labels such as `SOURCE_CONSTRAINED_RESIDUE` are assigned only by the later meta-observer.

## Predictions before intervention

For every non-trivial candidate claim, identify the source relation believed to support it and choose the relevant preregistered control(s) from `CONTROLS.md` before viewing intervention results.

| claim id | claimed source support | control id | predicted effect |
| --- | --- | --- | --- |
| | | | |

## Intervention result

Complete only after predictions are frozen.

| claim id | control id | intervention result | prediction matched? | notes |
| --- | --- | --- | --- | --- |
| | | | | |

Any newly invented post-hoc control must be labelled `EXPLORATORY` and cannot substitute for a failed preregistered prediction.

## Alternative representation check

Where feasible, rerun or audit the claim on an earlier or alternative frozen representation branch.

- alternate representation id:
- result preserved / weakened / lost / not tested:
- interpretation:

## Uncertainty / alternatives

- 

## Frozen output

- run status: `DRAFT` / `FROZEN` / `CONTAMINATION_RISK`
- freeze commit / artifact id:
- no semantic conclusions from other runs were viewed before freeze: yes / no
- no preprocessing was changed after viewing this run's substantive output: yes / no
