const BASE = 'https://www.polytranslator.com/api/v1';

function json(data, status = 200) {
  return Response.json(data, { status, headers: { 'Cache-Control': 'no-store' } });
}

function authorized(request) {
  const expected = process.env.MIMULUS_BRIDGE_TOKEN;
  if (!expected) return true;
  const supplied = request.headers.get('x-mimulus-bridge-token') || '';
  return supplied.length === expected.length && supplied === expected;
}

export async function POST(request) {
  if (!authorized(request)) return json({ error: 'unauthorized' }, 401);

  const apiKey = process.env.POLYTRANSLATOR_API_KEY;
  if (!apiKey) return json({ error: 'server_not_configured', detail: 'POLYTRANSLATOR_API_KEY is missing.' }, 503);

  let input;
  try {
    input = await request.json();
  } catch {
    return json({ error: 'invalid_json' }, 400);
  }

  const text = typeof input.text === 'string' ? input.text.trim() : '';
  const src = typeof input.src === 'string' ? input.src : '';
  const tgt = typeof input.tgt === 'string' ? input.tgt : '';
  const tier = input.tier === 'advanced' ? 'advanced' : 'fast';

  if (!text || text.length > 50000) return json({ error: 'invalid_text', detail: 'Text must contain 1–50,000 characters.' }, 400);
  if (!src || !tgt) return json({ error: 'missing_language', detail: 'Both src and tgt are required.' }, 400);

  const serverCap = Math.max(0, Number(process.env.POLYTRANSLATOR_MAX_CREDITS || 5));
  const requestedCap = Number.isFinite(Number(input.max_credits)) ? Math.max(0, Number(input.max_credits)) : serverCap;
  const maxCredits = Math.min(serverCap, requestedCap);
  const requestId = crypto.randomUUID();

  try {
    const upstream = await fetch(`${BASE}/translate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Idempotency-Key': requestId
      },
      body: JSON.stringify({ src, tgt, text, tier, max_credits: maxCredits })
    });

    const raw = await upstream.text();
    let payload;
    try { payload = JSON.parse(raw); } catch { payload = { raw }; }

    if (!upstream.ok) {
      return json({
        error: 'polytranslator_error',
        status: upstream.status,
        request_id: requestId,
        upstream: payload
      }, upstream.status);
    }

    return json({
      object: 'mimulus_translation_bridge_result',
      status: 'completed',
      provider: 'PolyTranslator',
      provider_request_id: payload.request_id || requestId,
      input: {
        representation: input.representation || 'text',
        source_artifact_id: input.source_artifact_id || null,
        src,
        tgt,
        tier,
        chars: text.length
      },
      output: {
        text: payload.text,
        usage: payload.usage || null
      },
      mimulus: {
        classification: 'DERIVED_FROM_DECLARED_INPUT',
        independent_source_decoder: false,
        semantic_relay_warning: 'Translation of a prior decoder/transcription output is lineage-dependent and does not count as independent cross-decoder residue.'
      }
    });
  } catch (error) {
    return json({ error: 'upstream_unreachable', detail: String(error?.message || error), request_id: requestId }, 502);
  }
}
