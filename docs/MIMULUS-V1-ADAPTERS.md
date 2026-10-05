# Mimulus v1 adapter boundary

Status: design freeze candidate

This document defines how Mimulus v1 may use local models, deterministic tools, remote model APIs, external websites, corpora, lexicons, and manual handoffs without making any provider part of the core architecture.

The rule is simple:

- `Decoder` describes the observer mechanism.
- `ExecutionAdapter` describes how that mechanism is actually run.
- `ReferenceAdapter` describes evidence-supporting lookup against a corpus, lexicon, catalogue, or attestation source.
- provider names belong in adapter configuration, not in Mimulus semantics.

This keeps Mimulus able to use new tools without redesigning the research model.

## Why this distinction exists

A language model, a deterministic cipher utility, a locally hosted specialist model, and a human analyst can all act as decoders.

But they execute very differently:

- in-browser code
- local/server model
- remote API
- external website handoff
- manual human procedure

Likewise, a corpus search is not automatically a decoder.

A lookup answering:

> Is this form attested in a known corpus?

must not silently become:

> This corpus independently decoded the source.

Mimulus therefore keeps decoding and reference checking separate.

## ExecutionAdapter

An ExecutionAdapter records how a decoder or transformation is executed.

```ts
export type ExecutionKind =
  | 'local_algorithm'
  | 'local_model'
  | 'remote_model'
  | 'external_web_tool'
  | 'human_manual'
  | 'other';

export type ExecutionMode =
  | 'browser'
  | 'server'
  | 'remote_api'
  | 'external_handoff'
  | 'manual_import'
  | 'other';

export type ExecutionAdapter = {
  id: string;
  label: string;
  kind: ExecutionKind;
  mode: ExecutionMode;
  provider?: string;
  implementationRef?: string;
  model?: string;
  version?: string;
  endpointRef?: string;
  license?: string;
  reproducibilityNotes?: string[];
  costClass?: 'none' | 'local_compute' | 'free_provider_limit' | 'metered' | 'unknown';
};
```

Rules:

- `provider` is metadata, not semantics.
- two adapters using the same underlying model are not automatically independent.
- external handoff does not weaken lineage requirements.
- manual copy/paste back into Mimulus must create an explicit import event.
- `free_provider_limit` means provider-controlled free usage and must not be treated as guaranteed capacity.
- a self-hosted model may have zero per-call fee while still having local compute cost.

## Decoder-to-adapter relation

A Decoder may be executed through one or more adapters.

Examples of allowed patterns:

```text
linguistic decoder
  -> local specialist model adapter

linguistic decoder
  -> remote general model adapter

symbolic decoder
  -> deterministic browser tool adapter

historical-language hypothesis
  -> external web handoff adapter
```

The adapter does not define the scientific claim. It only records the execution path.

A Run SHOULD therefore record both:

```ts
decoderId: string;
executionAdapterId?: string;
```

This allows Mimulus to distinguish:

- same decoder, different execution implementation
- different decoder, same underlying model
- different providers wrapping the same transformation

without claiming independence prematurely.

## External web handoff

Mimulus v1 may integrate a web tool without an API.

The minimum handoff flow is:

1. freeze the input representation;
2. create a pending Run / handoff record;
3. record the target adapter and intended operation;
4. copy or prepare the input for the external tool;
5. open the external tool;
6. user performs the operation;
7. user imports or pastes the result back into Mimulus;
8. Mimulus records the imported output and completes lineage.

Conceptually:

```text
frozen representation
  -> external handoff
  -> external tool
  -> manual import
  -> run output
```

The result remains lineage-dependent on the exact exported input.

If a user sends a previous decoder output rather than the frozen source representation, the returned result cannot count as an independent source decoder.

## ReferenceAdapter

A ReferenceAdapter is for lookup, attestation, lexical evidence, catalogue evidence, or corpus comparison.

```ts
export type ReferenceKind =
  | 'corpus'
  | 'lexicon'
  | 'dictionary'
  | 'catalogue'
  | 'attestation_search'
  | 'reference_database'
  | 'other';

export type ReferenceAdapter = {
  id: string;
  label: string;
  kind: ReferenceKind;
  provider?: string;
  accessMode:
    | 'local_data'
    | 'browser'
    | 'remote_api'
    | 'external_handoff'
    | 'manual_lookup'
    | 'other';
  datasetVersion?: string;
  license?: string;
  citationRef?: string;
  notes?: string[];
};
```

## ReferenceCheck

Reference checks are not Runs unless they themselves perform decoding.

```ts
export type ReferenceCheck = {
  id: string;
  referenceAdapterId: string;
  queryRef: string;
  derivedFromRunId?: string;
  sourceRepresentationId?: string;
  resultRef: string;
  resultType:
    | 'attested'
    | 'not_attested'
    | 'partial_match'
    | 'ambiguous'
    | 'lookup_result'
    | 'other';
  createdAt: string;
  notes?: string[];
};
```

Rules:

- attestation is not decipherment.
- dictionary membership is not source attribution.
- a corpus match derived from a decoder output remains downstream evidence about that output unless independently tied back to the source.
- absence from a corpus is not proof of impossibility unless corpus coverage justifies that claim.
- reference results must preserve dataset/version/citation context where available.

## Tool Dock

The v1 product may expose a Tool Dock, but the UI categories should map onto research roles rather than vendor brands.

Recommended groups:

### Decode

Observer mechanisms that produce a representation or interpretation.

Possible adapter modes:

- local model
- remote model
- deterministic external tool
- external web handoff
- human/manual decoder

### Check

Reference and corpus operations.

Examples of operation types:

- lexical attestation
- corpus search
- dictionary lookup
- catalogue lookup
- known-example comparison

### Transform

Deterministic preprocessing and source-preserving operations.

Examples:

- transcription conversion
- symbol substitution
- normalization
- segmentation
- permutation
- recurrence-preserving transform

A specific provider can appear in the UI as an installed adapter without becoming part of the core schema.

## Evidence boundary

Mimulus must not infer evidential independence from adapter multiplicity.

These are NOT automatically independent:

```text
same model via two providers
same source -> decoder output -> two translators
same transcription -> multiple tools sharing the same preprocessing assumption
same external tool rerun with cosmetic changes
```

These may contribute stronger independence only when the relevant mechanism actually varies and shared dependencies are accounted for.

Reference checks are supporting evidence, not independent decoders, unless the reference system actually takes the frozen source and performs an independently specified decoding operation.

## Lineage additions

The lineage model should support execution and reference provenance without turning either into semantic conclusions.

Recommended additional relations:

```ts
| 'executed_with'
| 'exported_to'
| 'imported_from'
| 'queried_against'
| 'attested_by'
```

`attested_by` records a reference relationship only. It does not mean `confirmed_by`.

## Cost and availability

Mimulus should treat cost/availability as operational metadata.

A tool may be:

- free and local
- free but externally rate-limited
- self-hosted with compute cost
- metered API
- manually accessed

No evidential weight follows from cost class.

The preferred v1 default is:

1. local deterministic operation where practical;
2. local/open model where practical and validated;
3. free external handoff where appropriate;
4. paid API only when automation materially improves the experiment.

This is a product/runtime policy, not a scientific rule.

## Provider policy

The core architecture must not hard-code specific services.

Concrete integrations belong in adapters, for example:

```text
adapter/external-web/<provider>
adapter/local-model/<model>
adapter/reference/<dataset>
```

Adapters may be added, removed, replaced, or disabled without changing Source, Run, Lineage, Decoder, Hypothesis, TestPlan, or beQube semantics.

## v1 implementation boundary

For the first working Tool Dock, Mimulus only needs to support:

1. one local deterministic adapter;
2. one remote model adapter;
3. one external web handoff + manual import adapter;
4. one ReferenceAdapter + ReferenceCheck flow.

This is sufficient to test the architecture without prematurely building a catalogue of integrations.

## Required invariants

1. Every tool-derived Run identifies its Decoder and execution path.
2. Every external handoff preserves the exact exported representation reference.
3. Every imported external result records provenance to the handoff.
4. Reference checks cannot silently promote themselves into decoder agreement.
5. Multiple adapters do not imply independent evidence.
6. Provider identity does not define scientific semantics.
7. Replacing an adapter must not require changing the Mimulus core research objects.
8. A downstream translation through a free or paid tool remains lineage-dependent in exactly the same way.
