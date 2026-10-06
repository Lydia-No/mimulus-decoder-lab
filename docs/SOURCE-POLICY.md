# Source policy for Voynich experiments

This document governs transliteration-based token fixtures in the Python
decoder workspace. The repository's historical source and representation
precedence is defined in [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md): the
manuscript image is the observational source, and a transcription is a derived
representation. This policy does not require image-only experiments to receive
transcriptions or supersede their frozen protocols.

For a transliteration-based experiment, do not manually infer Voynich glyphs
from screenshots when a published transliteration exists.

## Preferred machine-readable transcription

Use the Reference (RF) transliteration distributed through René Zandbergen's Voynich Manuscript transliteration resources. The current reference resource combines the Zandbergen-Landini and GC transliterations and is available in IVTFF format. Preserve the exact source version used in every experiment.

IVTFF provides page and locus identifiers and retains uncertainty conventions. Relevant distinctions include running text, labels, circular text, and radial text. These distinctions must not be flattened before the source fixture is frozen.

## Required fixture metadata

Every committed Voynich transcription fixture must record:

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

## External polytranslator provenance boundary

The earlier screenshot-based external polytranslator material did not establish
its exact folio. Do not guess that folio from semantic content or substitute
the separately frozen f113r source because it fits a candidate reading.

The repository now has a separately frozen f113r authority image, recorded in
`fixtures/voynich/f113r/authority-freeze.json`. That image freeze does not establish
the external polytranslator run's folio or freeze a transcription for the Python
token workspace. This workspace continues to use synthetic fixtures for its
known-answer benchmarks. Any historical token experiment requires its own
declared representation and authorization under the current source policy.
