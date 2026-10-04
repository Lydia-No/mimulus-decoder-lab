# Method boundary

## Unit of analysis

The lab does not begin with a presumed language or translation. Its primitive input is an observation record derived from a source segment.

A decoder context may transform that observation into a candidate reading. The decoder must expose enough of its assumptions that another run can distinguish what came from the source from what the decoder supplied.

## Minimal conceptual objects

### Observation
A bounded record of source-visible or source-derived features. It should not contain a desired interpretation.

### Decoder context
An explicit set of assumptions or operations used to derive structure from an observation.

### Candidate reading
The output of one decoder context, including provenance linking claims back to observations and decoder assumptions.

### Meta-observation
A statement about one or more candidate readings: agreement, disagreement, invariance, dependency, contradiction, or underdetermination.

A meta-observation is not automatically a claim about the historical meaning of the source.

## Independence rule

Do not give later decoders the semantic conclusions of earlier decoders when the experiment is intended to test independent convergence. Shared raw observations and explicitly declared common preprocessing are permitted; inherited conclusions are not.

## Provenance rule

Every substantive candidate claim should be classifiable as:

- directly observed;
- decoder-supplied;
- derived from observation + decoder;
- external corroboration;
- unresolved.

## Adversarial rule

A decoder is not strengthened merely because it produces coherent prose. Where possible, construct competing decoder contexts capable of producing alternative coherent readings and test what evidence discriminates among them.

## Cross-decoder residue

If a structure survives multiple materially different decoder contexts, record it as cross-decoder residue. Do not relabel it as decoded meaning without an additional evidential step.

## Current target

The first target is Voynich material. This is an experimental testbed for the method, not a prior commitment that Mimulus supplies a Voynich key.
