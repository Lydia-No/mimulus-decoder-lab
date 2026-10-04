# Source policy for Voynich experiments

For Experiment 001, do not manually infer Voynich glyphs from screenshots when a published transliteration exists.

## Primary machine-readable source

Use the Reference (RF) transliteration distributed through René Zandbergen's Voynich Manuscript transliteration resources. The current reference resource combines the Zandbergen-Landini and GC transliterations and is available in IVTFF format. Preserve the exact source version used in every experiment.

IVTFF provides page and locus identifiers and retains uncertainty conventions. Relevant distinctions include running text, labels, circular text, and radial text. These distinctions must not be flattened before the source fixture is frozen.

## Required fixture metadata

Every committed Voynich source fixture must record:

- manuscript folio/page identifier;
- locus identifier(s);
- transliteration source and version;
- transliteration alphabet;
- exact unmodified transliterated text;
- any preprocessing performed after freezing the raw source;
- unresolved/alternative readings as represented by the source;
- retrieval date and source URL/reference.

## Contamination boundary

The source fixture must be frozen before importing semantic outputs from Mimulus/The Green House's Hawaiian, Sumerian, Gaelic, or other polytranslator runs.

Those outputs may later become external decoder runs. They must not be used to select, normalize, segment, or repair the source transcription.

## Current blocker

The screenshot provenance available to this project does not yet establish the exact folio used by the external polytranslator run. Do not guess it from semantic content or choose a folio because it appears to fit a candidate reading.

Until the folio is established, executable v0 development may use synthetic fixtures for tests, but Experiment 001 remains source-unfrozen.
