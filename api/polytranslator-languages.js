const BASE = 'https://www.polytranslator.com/api/v1';

export async function GET() {
  try {
    const upstream = await fetch(`${BASE}/languages`, {
      headers: { 'Accept': 'application/json' },
      cache: 'no-store'
    });
    const body = await upstream.text();
    return new Response(body, {
      status: upstream.status,
      headers: {
        'Content-Type': upstream.headers.get('content-type') || 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=3600'
      }
    });
  } catch (error) {
    return Response.json({ error: 'language_lookup_failed', detail: String(error?.message || error) }, { status: 502 });
  }
}
