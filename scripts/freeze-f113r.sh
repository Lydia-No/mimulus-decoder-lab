#!/usr/bin/env bash
set -euo pipefail

URL='https://collections.library.yale.edu/iiif/2/1006270/full/full/0/default.jpg'
AUTHORITY='Beinecke Rare Book and Manuscript Library, Yale University'
IMAGE_ID='1006270'
FOLIO='f113r'
OUT='/tmp/f113r-freeze'
IMAGE="$OUT/f113r-yale-1006270.jpg"
HEADERS="$OUT/headers.txt"
RECORD="$OUT/freeze.json"
mkdir -p "$OUT"

curl --fail --location --silent --show-error \
  --retry 4 --retry-all-errors --connect-timeout 20 --max-time 240 \
  --dump-header "$HEADERS" --output "$IMAGE" "$URL"

python3 - "$IMAGE" <<'PY'
import sys
p=sys.argv[1]
with open(p,'rb') as f:
    if f.read(2) != b'\xff\xd8':
        raise SystemExit('Downloaded file is not a JPEG')
PY

SHA256="$(sha256sum "$IMAGE" | awk '{print $1}')"
BYTES="$(stat -c '%s' "$IMAGE")"
MIME="$(file --brief --mime-type "$IMAGE")"

read WIDTH HEIGHT < <(python3 - "$IMAGE" <<'PY'
import struct,sys
p=sys.argv[1]
with open(p,'rb') as f:
    data=f.read()
i=2
while i < len(data):
    if data[i] != 0xFF:
        i += 1; continue
    while i < len(data) and data[i] == 0xFF: i += 1
    if i >= len(data): break
    marker=data[i]; i += 1
    if marker in (0xD8,0xD9): continue
    if i+2 > len(data): break
    seglen=struct.unpack('>H',data[i:i+2])[0]
    if marker in range(0xC0,0xC4):
        h,w=struct.unpack('>HH',data[i+3:i+7])
        print(w,h); raise SystemExit
    i += seglen
raise SystemExit('JPEG dimensions not found')
PY
)

ETAG="$(awk 'BEGIN{IGNORECASE=1} /^etag:/{sub(/^[^:]*:[[:space:]]*/,""); sub(/\r$/,""); print; exit}' "$HEADERS" || true)"
LAST_MODIFIED="$(awk 'BEGIN{IGNORECASE=1} /^last-modified:/{sub(/^[^:]*:[[:space:]]*/,""); sub(/\r$/,""); print; exit}' "$HEADERS" || true)"
CONTENT_TYPE="$(awk 'BEGIN{IGNORECASE=1} /^content-type:/{sub(/^[^:]*:[[:space:]]*/,""); sub(/\r$/,""); print; exit}' "$HEADERS" || true)"

export URL AUTHORITY IMAGE_ID FOLIO SHA256 BYTES MIME WIDTH HEIGHT ETAG LAST_MODIFIED CONTENT_TYPE
python3 - "$RECORD" <<'PY'
import json,os,sys,datetime
record={
  'schema_version':'0.1',
  'fixture_id':'voynich-f113r',
  'folio':os.environ['FOLIO'],
  'authority':os.environ['AUTHORITY'],
  'authority_image_id':os.environ['IMAGE_ID'],
  'retrieval':{
    'url':os.environ['URL'],
    'method':'HTTP GET of Yale IIIF Image API full/full/0/default.jpg',
    'retrieved_by':'GitHub Actions ubuntu-latest',
    'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    'etag':os.environ.get('ETAG') or None,
    'last_modified':os.environ.get('LAST_MODIFIED') or None,
    'http_content_type':os.environ.get('CONTENT_TYPE') or None
  },
  'bytes':{
    'sha256':os.environ['SHA256'],
    'size':int(os.environ['BYTES']),
    'mime':os.environ['MIME'],
    'width':int(os.environ['WIDTH']),
    'height':int(os.environ['HEIGHT'])
  },
  'extraction':{
    'status':'frozen',
    'region':'full-folio',
    'iiif_region':'full',
    'iiif_size':'full',
    'iiif_rotation':'0',
    'iiif_quality_format':'default.jpg'
  },
  'boundary':'This record freezes the exact JPEG bytes returned by the authority IIIF URL at retrieval time. It does not establish a transcription or interpretation.'
}
with open(sys.argv[1],'w') as f: json.dump(record,f,indent=2,sort_keys=True)
PY

cat "$RECORD"
