# f113v decoder run template

Use one copy of this file per decoder run. Do not expose completed runs to later decoders before the experiment's independent-run freeze.

## Run identity

- fixture: `voynich-f113v-001`
- decoder id:
- decoder version:
- run id:
- date:
- source hash verified: `bccf2e0fdf11d6040ab87d55701eb23e2b6effc9e4ea5ad24c4aaf9e8a27f1c1`
- input representation id:

## Knowledge boundary

### Information supplied to this decoder

- 

### Information explicitly withheld

- outputs from other decoders
- proposed plaintext/translation
- external Voynich interpretations unless this run is explicitly designated as an external-prior decoder

### Prior exposure / contamination declaration

State any relevant information the decoder already knew or saw before this run. If material prior exposure cannot be excluded, mark the run `CONTAMINATION_RISK` rather than treating it as blind.

- 

## Declared decoder context

Describe only the rules, assumptions, operators or inference procedure this decoder is permitted to use.

- 

## Source observations used

Record observations by neutral identifier and link each one to the source or declared derived representation.

| observation id | description | location / mapping | confidence |
| --- | --- | --- | --- |
| | | | |

## Decoder-supplied structure

Everything introduced by the decoder rather than directly observed belongs here.

| assumption / operator id | description | rationale |
| --- | --- | --- |
| | | |

## Candidate claims

Do not collapse structural claims into semantic claims.

| claim id | claim | evidence status | provenance |
| --- | --- | --- | --- |
| | | | |

Allowed provisional evidence statuses inside a run:

- `DIRECT_OBSERVATION`
- `DECODER_SUPPLIED`
- `DERIVED`
- `UNRESOLVED`
- `CONTAMINATION_RISK`

Cross-decoder labels such as `SOURCE_CONSTRAINED_RESIDUE` are assigned only by the later meta-observer.

## Predictions before intervention

For every non-trivial candidate claim, state what should happen if the source feature believed to support it is altered.

| claim id | intervention | predicted effect |
| --- | --- | --- |
| | | |

## Intervention result

Complete only after predictions are frozen.

| claim id | intervention result | prediction matched? | notes |
| --- | --- | --- | --- |
| | | | |

## Uncertainty / alternatives

- 

## Frozen output

- run status: `DRAFT` / `FROZEN` / `CONTAMINATION_RISK`
- freeze commit / artifact id:
- no semantic conclusions from other runs were viewed before freeze: yes / no
