const OPENAI_URL = 'https://api.openai.com/v1/responses';

function json(res, status, data) {
  res.status(status).setHeader('Cache-Control', 'no-store').json(data);
}

function readOutputText(payload) {
  const parts = [];
  for (const item of payload?.output || []) {
    if (item?.type !== 'message') continue;
    for (const part of item.content || []) {
      if (part?.type === 'output_text' && typeof part.text === 'string') parts.push(part.text);
    }
  }
  return parts.join('\n').trim();
}

function modeInstructions(mode) {
  const shared = `You are Mimulus Explorer, an experimental meta-observer for opaque symbolic material.\n\nYour job is NOT to announce a decipherment. Keep these layers separate:\n1. DIRECT OBSERVATION: what is visibly or explicitly present in the supplied source/representation.\n2. REPRESENTATION ASSUMPTIONS: crop, segmentation, transcription, token grouping, language assumption, or any other preprocessing supplied or inferred.\n3. DERIVED STRUCTURE: patterns that follow from those assumptions.\n4. SEMANTIC HYPOTHESES: possible meanings, always labelled as hypotheses.\n5. TESTS: concrete interventions that could weaken, falsify, or distinguish the hypotheses.\n\nNever treat fluent language, historical fit, repeated motifs, or a plausible intermediate language as proof. A translation of a previous decoder output is lineage-dependent, not independent corroboration. If the source is insufficient, say so. Preserve uncertainty.`;

  const modes = {
    observe: `Focus on neutral source observations and ambiguity. Avoid semantic interpretation unless needed to explain what NOT to infer.`,
    structural: `Look for recurrence, layout, adjacency, segmentation alternatives, symmetry, ordering, and possible operator/state structure. Offer competing structural accounts.`,
    adversarial: `Act as a skeptical competing decoder. Try to reproduce apparent regularities under alternative assumptions, identify shared-prior effects, and propose matched null or ablation controls.`,
    explore: `Explore bold possibilities, including language or symbolic hypotheses, but explicitly separate speculation from source-constrained evidence and propose tests for every non-trivial interpretation.`
  };
  return `${shared}\n\nMODE: ${mode}\n${modes[mode] || modes.explore}`;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'method_not_allowed' });

  const expectedToken = process.env.MIMULUS_EXPLORER_TOKEN;
  if (expectedToken && req.headers['x-mimulus-explorer-token'] !== expectedToken) {
    return json(res, 401, { error: 'unauthorized' });
  }

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return json(res, 503, { error: 'server_not_configured', detail: 'OPENAI_API_KEY is missing.' });

  const body = req.body || {};
  const mode = ['observe', 'structural', 'adversarial', 'explore'].includes(body.mode) ? body.mode : 'explore';
  const profile = body.profile === 'deep' ? 'deep' : 'fast';
  const fastModel = process.env.MIMULUS_FAST_MODEL || 'gpt-6-luna';
  const deepModel = process.env.MIMULUS_DEEP_MODEL || 'gpt-6-sol';
  const model = profile === 'deep' ? deepModel : fastModel;

  const note = typeof body.note === 'string' ? body.note.trim().slice(0, 12000) : '';
  const transcription = typeof body.transcription === 'string' ? body.transcription.trim().slice(0, 30000) : '';
  const image = typeof body.image_data_url === 'string' ? body.image_data_url : '';

  if (!image && !transcription && !note) return json(res, 400, { error: 'missing_input' });
  if (image && !/^data:image\/(png|jpe?g|webp);base64,/i.test(image)) {
    return json(res, 400, { error: 'invalid_image', detail: 'Use a PNG, JPEG, or WEBP data URL.' });
  }
  if (image.length > 8_000_000) return json(res, 413, { error: 'image_too_large' });

  const userContent = [];
  const textParts = [];
  if (note) textParts.push(`USER NOTE / QUESTION:\n${note}`);
  if (transcription) textParts.push(`SUPPLIED TRANSCRIPTION OR INTERMEDIATE REPRESENTATION (not ground truth):\n${transcription}`);
  textParts.push(`Return a compact research record with these headings:\n- Direct observations\n- Representation assumptions\n- Candidate structures\n- Semantic hypotheses (if any)\n- Competing explanations\n- Best falsification / ablation tests\n- Evidence status`);
  userContent.push({ type: 'input_text', text: textParts.join('\n\n') });
  if (image) userContent.push({ type: 'input_image', image_url: image, detail: 'high' });

  const requestId = crypto.randomUUID();
  try {
    const upstream = await fetch(OPENAI_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Idempotency-Key': requestId
      },
      body: JSON.stringify({
        model,
        instructions: modeInstructions(mode),
        input: [{ role: 'user', content: userContent }],
        max_output_tokens: profile === 'deep' ? 3500 : 1800,
        store: false
      })
    });
    const payload = await upstream.json().catch(() => ({}));
    if (!upstream.ok) return json(res, upstream.status, { error: 'model_error', request_id: requestId, upstream: payload });

    const output = readOutputText(payload);
    return json(res, 200, {
      object: 'mimulus_explorer_run',
      run_id: requestId,
      model: payload.model || model,
      profile,
      mode,
      source: {
        image_supplied: Boolean(image),
        transcription_supplied: Boolean(transcription),
        note_supplied: Boolean(note)
      },
      output,
      usage: payload.usage || null,
      mimulus: {
        classification: 'EXPLORATORY_DECODER_OUTPUT',
        independent_evidence: false,
        warning: 'This output is a decoder observation, not a decipherment result. Any downstream translation remains lineage-dependent unless independently run from the frozen source.'
      }
    });
  } catch (error) {
    return json(res, 502, { error: 'model_unreachable', request_id: requestId, detail: String(error?.message || error) });
  }
}
