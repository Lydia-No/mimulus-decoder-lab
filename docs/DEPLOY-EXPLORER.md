# Deploy Mimulus Explorer

Mimulus Explorer is a small multimodal research surface for exploratory work on opaque symbolic material. It is not a decipherment service.

## What the deployed surface does

- accepts a PNG/JPEG/WEBP image;
- optionally accepts EVA, transliteration, or another intermediate representation;
- lets the user choose neutral observation, structural, adversarial, or bounded free-exploration mode;
- sends the material to the configured multimodal model;
- returns an explicitly layered research record rather than a single translation claim;
- exports a JSON run record.

## Required deployment secret

Set:

- `OPENAI_API_KEY`

Never put the key in the repository or browser code.

## Optional configuration

- `MIMULUS_EXPLORER_TOKEN` — shared access token. If omitted, the endpoint is public.
- `MIMULUS_FAST_MODEL` — defaults to `gpt-6-luna`.
- `MIMULUS_DEEP_MODEL` — defaults to `gpt-6-sol`.

A private/shared token is strongly recommended if the subdomain is internet-accessible because model usage is billed to the API-key owner.

## Vercel-style deployment

The repository includes a static interface at `explorer/index.html` and a serverless endpoint at `api/explore.js`.

For a dedicated subdomain project, route `/` to `/explorer/index.html` and retain `/api/*` as serverless functions. Add the environment variables above in the host dashboard, then attach the desired subdomain.

Example target:

`mimulus.arctopia.no`

The browser never receives the OpenAI API key.

## Evidence boundary

Explorer results are labelled `EXPLORATORY_DECODER_OUTPUT`.

If an Explorer result is translated by PolyTranslator or another tool, that downstream output is lineage-dependent. It is not an independent decoder of the original source.

For clean Mimulus experiments, freeze source/representation and run independent decoder contexts separately. Do not feed naturalistic Explorer outputs back into the blind first-pass fixture.
