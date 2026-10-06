# Source provenance and representation boundary

Status: experimental protocol support.

Mimulus treats the source artifact, transcriptions, preprocessing, decoder outputs and semantic interpretations as different layers. They must not be silently collapsed into one another.

## Precedence rule

For Voynich experiments, the manuscript image is the observational source layer.

A transcription is a derived representation of that image. A segmentation is a convention-dependent representation. A decoder output is a candidate derivation. A semantic reading is an interpretation.

When these layers conflict, the source image outranks the transcription or decoder representation as evidence of what is visibly present.

This does not imply that the image is self-interpreting. Visual ambiguity, damaged glyphs, uncertain boundaries and layout decisions must remain explicit.

## Required source record

Every historical fixture should retain, separately where applicable:

- source identifier and shelfmark;
- authority or holding institution;
- access pointer(s);
- folio/region identifier;
- local byte hash when exact source bytes are frozen;
- image extraction or crop procedure;
- transcription convention and version;
- uncertain or disputed glyphs;
- preprocessing operations;
- layout observations not represented in transcription.

Do not report a content hash unless the exact bytes were acquired and hashed.

## Representation classes

Use the following distinctions in fixture records:

- `SOURCE_IMAGE`: image evidence from the manuscript or a faithful scan;
- `SOURCE_METADATA`: externally supplied catalog or folio metadata;
- `TRANSCRIPTION`: a declared transcription system applied to visible glyphs;
- `PREPROCESSING`: normalization, segmentation, crop, ordering or transformation decisions;
- `DERIVED_STRUCTURE`: structure produced by a decoder or analytic procedure;
- `CANDIDATE_INTERPRETATION`: semantic or linguistic reading;
- `META_OBSERVATION`: comparison across decoder outputs after runs are frozen.

## Anti-collapse rule

Do not refer to EVA, another transliteration system, or any normalized token stream as "the Voynich text" without qualification. It is a representation of the manuscript under a transcription convention.

Likewise, cross-decoder agreement is not promoted to historical truth. It remains a meta-observation until independently supported.

## Authority image versus access copy

A folio-level authority image and a whole-manuscript access PDF are separate provenance objects. An unhashed transport copy does not invalidate an independently frozen authority folio, and a hash for one must never be silently attributed to the other.

For f113r, the Yale/Beinecke authority JPEG for image id `1006270` is frozen in `fixtures/voynich/f113r/authority-freeze.json` and independently re-fetched with the same SHA-256. The Archive.org manuscript PDF remains a separate convenience access copy whose exact bytes are not currently frozen.

## Repository storage boundary

The repository should normally store manifests, hashes, coordinates, derived fixtures and experiment records rather than duplicating an entire external manuscript PDF. A complete source artifact may be stored only when licensing, size and reproducibility requirements justify it.

The Archive.org Voynich PDF remains referenced externally as an access copy. Its missing hash does not substitute for or weaken the separately frozen Yale f113r authority image; it simply means claims tied specifically to that PDF's exact bytes or pagination should not be made without an additional PDF freeze.
