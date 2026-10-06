# f113r image-only run 001

Status: preregistered tooling; no decoder output is part of this document.

Research direction, conceptual framing and methodology: Linda Thorstensen.

## Purpose

Run the first historical Mimulus comparison directly from the frozen Yale/Beinecke f113r image, without a transcription, OCR layer, language hypothesis, semantic key, or previous decoder interpretation.

The run tests only two visual/layout questions:

1. `horizontal-repetition` — does the page exhibit repeated horizontal organization under the decoder's declared representation?
2. `left-margin-discrete-repetition` — does the left margin exhibit repeated discrete visual organization under the decoder's declared representation?

The proposition vocabulary is deliberately binary: `present` or `not_detected`. `not_detected` is not evidence of absence.

## Frozen source

Fixture: `voynich-f113r`.

Authority image SHA-256:

`ad748f9012b174be520b7ac837fdadf913e49a696323920ca655ecf5474afb5c`

The runner must fail before analysis if the fetched Yale IIIF bytes do not match this hash.

## Decoder A2 — row projection

Representation:

- grayscale;
- Lanczos resize to 1200 px width;
- central crop x=.18–.94, y=.05–.95;
- separate left-margin crop x=.03–.18, y=.05–.95;
- Otsu threshold independently within each crop.

Horizontal rule:

- smooth row dark-pixel fraction with radius 2;
- active row threshold = .012;
- merge gaps <=4 px; discard bands <2 px;
- `present` only if >=20 bands, median centre gap 12–90 px, and gap CV <=.90.

Margin rule:

- active row threshold = .010;
- merge gaps <=5 px; discard bands <2 px;
- `present` only if 8–35 bands and median centre gap 25–180 px.

## Decoder B5 — gradient autocorrelation

Representation:

- grayscale;
- bilinear resize to 900 px width;
- no binarization;
- vertical-gradient energy calculated independently in the central and left-margin crops.

Horizontal rule:

- smoothed gradient-energy series;
- normalized autocorrelation searched at lags 8–80 px;
- `present` if best autocorrelation >=.10.

Margin rule:

- normalized autocorrelation searched at lags 20–150 px;
- `present` if best autocorrelation >=.08.

## Decoder C8 — component geometry

Representation:

- grayscale;
- BOX resize to 360 px width;
- inner crop x=.02–.96, y=.04–.96;
- Otsu binarization;
- 8-neighbour connected components.

Horizontal rule:

- retain declared central components with area 2–250 px;
- bin component centroids into 72 vertical bins;
- a bin is active when it contains >=4 candidate components;
- `present` if >=20 bins are active.

Margin rule:

- restrict components to the declared left-margin zone;
- retain area 4–220 px, width 2–30 px, height 2–45 px;
- collapse component centroids within 5 px into one vertical locus;
- `present` if 8–35 loci remain and median locus gap is 5–45 px.

## Independence boundary

The three decoders share the same frozen source image, so agreement is not independent historical confirmation. They differ in representation and measurement procedure, not source ancestry.

The historical meta-observer may therefore emit only its descriptive labels (`CROSS_DECODER_RESIDUE`, `PARTIAL_CROSS_DECODER_RESIDUE`, `DECODER_SPECIFIC`, `INCOMPATIBLE_READINGS`). It must not emit a known-answer label from Pilot 001.

## Prospective rule

The thresholds and decision rules above are frozen before the first result-bearing CI run. If an implementation bug is discovered, it must be documented and versioned rather than silently tuning a threshold after inspection of f113r output.

This run cannot establish a Voynich translation, language identification, decipherment, or historical meaning.
