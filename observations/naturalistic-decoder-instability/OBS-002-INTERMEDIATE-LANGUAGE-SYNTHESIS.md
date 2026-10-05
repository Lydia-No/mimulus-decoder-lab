# OBS-002 — Plausible intermediate-language synthesis

Status: **NATURALISTIC / NON-BLIND / DECODER-BEHAVIOR OBSERVATION**

This observation records a naturally occurring decoder output sequence supplied after the clean f113v fixture had already been separated from this conversation. It is not a Voynich decipherment record and must not be used as evidence in the blind f113v run.

## Observation purpose

The decoder output is notable because it exposes an intermediate representation rather than only an English semantic gloss:

`opaque manuscript image -> claimed Sumerian-looking transliteration -> English rendering`

This creates two independently testable transformations rather than one:

1. source image -> intermediate transliteration;
2. intermediate transliteration -> English interpretation.

The existence of a plausible-looking intermediate layer does not establish provenance from the source.

## Supplied artifacts

### A — manuscript image

- file: `2B63B750-2C45-4B01-9DEF-57DAE2CC0E30.jpeg`
- dimensions: `1536 x 1151`
- SHA-256: `baa8ca01c30d80b3fe163b982d6e1b7f36d3345b5ce9ce9b65a982915b535aa9`
- directly visible: circular manuscript diagram with surrounding opaque script and illustrations

### B — intermediate output view 1

- file: `93BBA331-012B-4A40-9073-9F4C509F7C19.png`
- dimensions: `2732 x 2048`
- SHA-256: `0608abe44dbadf0ef685a4119416d1df3ea47b57b3c0e5f1dcc6dc72f2b31763`
- directly visible headings include `An-ki-a-ni-ta-e-a-bi`, `En-ne-en-gal`, `Nam-en-na`, and `An-ki-a-bi`
- directly visible body material includes forms such as `Utu`, `en-gal`, `an-ki`, `den-lil`, `den-ki`, and `nin-hur-sag`

### C — intermediate output view 2

- file: `35992F6C-DE55-429F-A655-AB6D5D0E2CFB.png`
- dimensions: `2732 x 2048`
- SHA-256: `1e0ffd48bee34a87bc47dbc24dcf38ac3e17c2fe54e25e832aaccc06fed4a054`
- directly visible: continuation of the same Sumerian-looking transliteration layer

### D — English rendering

- file: `E19230C3-2F31-45A0-9A09-84041793B5DE.jpeg`
- dimensions: `1536 x 1151`
- SHA-256: `e1c29a07f2d9dfc2515461d1c8294dff7461b5258800eee0b3482d70a3331ff8`
- directly visible semantic themes include heaven and earth, Utu, lordship, Sumer and Akkad, An, Enlil, Enki, Ninhursag, fate, and divine powers

The screenshots are provenance captures of displayed outputs. They do not establish the model, prompt, crop transform, target-language instruction, prior session history, or decoding procedure unless those are separately recovered and frozen.

## Direct observations

1. The decoder did not jump directly from the image to English prose in this captured sequence. It displayed a structured intermediate text with headings and hyphenated forms that visually resemble transliteration.
2. The intermediate layer contains recurring units and recurring proper-name-like forms.
3. The English rendering contains a coherent ancient-Mesopotamian semantic field rather than a generic literal-looking gloss.
4. The semantic rendering appears more specific and historically flavored than can be justified from the screenshots alone.
5. The intermediate layer and the English layer are both decoder outputs. Neither is a source observation.

## Provisional Mimulus classification

- source image: `DIRECT_OBSERVATION`
- displayed intermediate transliteration: `DECODER_OUTPUT`
- displayed English prose: `DECODER_OUTPUT`
- claim that the intermediate layer is genuine Sumerian: `UNVERIFIED_EXTERNAL_LANGUAGE_CLAIM`
- claim that the intermediate layer derives from the manuscript: `UNVERIFIED_MAPPING`
- claim that the English prose follows compositionally from the intermediate layer: `UNVERIFIED_SECOND_STAGE_MAPPING`
- overall case: `DECODER_DEPENDENT` unless later controlled replay establishes source sensitivity

No element in this record qualifies as `SOURCE_CONSTRAINED_RESIDUE`.

## Failure mode of interest

### Plausible intermediate-language synthesis

A decoder may create an epistemically persuasive bridge by generating an intermediate representation that contains:

- attested-looking morphemes or names;
- familiar orthographic conventions;
- culturally coherent vocabulary;
- an English rendering consistent with that cultural field.

This can produce a stronger appearance of evidence than English-only fluency even when the source-to-intermediate mapping has not been demonstrated.

The relevant Mimulus risk is:

`local plausibility of intermediate units != provenance of the whole mapping`

and separately:

`plausible intermediate layer != evidence that the English gloss follows from the source`

## Controlled replay questions

A later controlled experiment may test the following without importing the answers into the clean f113v fixture:

1. **Mapping consistency** — does the same frozen source segment map to the same intermediate unit across clean reruns?
2. **Source sensitivity** — if one source segment is perturbed, does the corresponding intermediate unit change as preregistered?
3. **Context sensitivity** — does the intermediate layer change under crop, prompt, target-language request, session reset, or prior-history changes?
4. **Independent language validation** — can an evaluator that sees only the intermediate text assess whether it is grammatically/compositionally valid without seeing the English rendering or manuscript image?
5. **Second-stage fidelity** — can an evaluator that sees only the intermediate text recover the displayed English meaning without access to the manuscript image or prior decoder context?
6. **Null recoverability** — can comparably coherent intermediate-language material be produced from matched perturbed or null inputs?

## Interpretation boundary

This case is valuable because it exposes a two-stage interpretive chain that can be audited separately. It does not show that the manuscript is Sumerian, that the displayed transliteration is historically attested, or that the English rendering is a translation of the source.

It should remain in the naturalistic decoder-instability track and must not be supplied to blind decoders used for Experiment 001.
