<?php
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function respond($status, $data) {
    http_response_code($status);
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(405, array('error' => 'method_not_allowed'));
}

$configPath = __DIR__ . '/config.php';
if (!is_file($configPath)) {
    respond(503, array('error' => 'server_not_configured', 'detail' => 'Missing server config.'));
}
$config = include $configPath;
if (!is_array($config)) {
    respond(503, array('error' => 'server_not_configured', 'detail' => 'Invalid server config.'));
}

$expectedToken = isset($config['EXPLORER_TOKEN']) ? (string)$config['EXPLORER_TOKEN'] : '';
if ($expectedToken !== '') {
    $supplied = isset($_SERVER['HTTP_X_MIMULUS_EXPLORER_TOKEN']) ? (string)$_SERVER['HTTP_X_MIMULUS_EXPLORER_TOKEN'] : '';
    if (!hash_equals($expectedToken, $supplied)) {
        respond(401, array('error' => 'unauthorized'));
    }
}

$apiKey = isset($config['OPENAI_API_KEY']) ? trim((string)$config['OPENAI_API_KEY']) : '';
if ($apiKey === '') {
    respond(503, array('error' => 'server_not_configured', 'detail' => 'OPENAI_API_KEY is missing.'));
}

$raw = file_get_contents('php://input');
$body = json_decode($raw, true);
if (!is_array($body)) {
    respond(400, array('error' => 'invalid_json'));
}

$allowedModes = array('observe', 'structural', 'adversarial', 'explore');
$mode = isset($body['mode']) && in_array($body['mode'], $allowedModes, true) ? $body['mode'] : 'explore';
$profile = isset($body['profile']) && $body['profile'] === 'deep' ? 'deep' : 'fast';
$fastModel = !empty($config['FAST_MODEL']) ? (string)$config['FAST_MODEL'] : 'gpt-6-luna';
$deepModel = !empty($config['DEEP_MODEL']) ? (string)$config['DEEP_MODEL'] : 'gpt-6.1-sol';
$model = $profile === 'deep' ? $deepModel : $fastModel;

$note = isset($body['note']) && is_string($body['note']) ? trim(substr($body['note'], 0, 12000)) : '';
$transcription = isset($body['transcription']) && is_string($body['transcription']) ? trim(substr($body['transcription'], 0, 30000)) : '';
$image = isset($body['image_data_url']) && is_string($body['image_data_url']) ? $body['image_data_url'] : '';

if ($image === '' && $transcription === '' && $note === '') {
    respond(400, array('error' => 'missing_input'));
}
if ($image !== '' && !preg_match('#^data:image/(png|jpe?g|webp);base64,#i', $image)) {
    respond(400, array('error' => 'invalid_image', 'detail' => 'Use PNG, JPEG, or WEBP.'));
}
if (strlen($image) > 8000000) {
    respond(413, array('error' => 'image_too_large'));
}

$shared = "You are Mimulus Explorer, an experimental meta-observer for opaque symbolic material.\n\nYour job is NOT to announce a decipherment. Keep these layers separate:\n1. DIRECT OBSERVATION: what is visibly or explicitly present in the supplied source/representation.\n2. REPRESENTATION ASSUMPTIONS: crop, segmentation, transcription, token grouping, language assumption, or any other preprocessing supplied or inferred.\n3. DERIVED STRUCTURE: patterns that follow from those assumptions.\n4. SEMANTIC HYPOTHESES: possible meanings, always labelled as hypotheses.\n5. TESTS: concrete interventions that could weaken, falsify, or distinguish the hypotheses.\n\nNever treat fluent language, historical fit, repeated motifs, or a plausible intermediate language as proof. A translation of a previous decoder output is lineage-dependent, not independent corroboration. If the source is insufficient, say so. Preserve uncertainty.";
$modes = array(
    'observe' => 'Focus on neutral source observations and ambiguity. Avoid semantic interpretation unless needed to explain what NOT to infer.',
    'structural' => 'Look for recurrence, layout, adjacency, segmentation alternatives, symmetry, ordering, and possible operator/state structure. Offer competing structural accounts.',
    'adversarial' => 'Act as a skeptical competing decoder. Try to reproduce apparent regularities under alternative assumptions, identify shared-prior effects, and propose matched null or ablation controls.',
    'explore' => 'Explore bold possibilities, including language or symbolic hypotheses, but explicitly separate speculation from source-constrained evidence and propose tests for every non-trivial interpretation.'
);
$instructions = $shared . "\n\nMODE: " . $mode . "\n" . $modes[$mode];

$textParts = array();
if ($note !== '') $textParts[] = "USER NOTE / QUESTION:\n" . $note;
if ($transcription !== '') $textParts[] = "SUPPLIED TRANSCRIPTION OR INTERMEDIATE REPRESENTATION (not ground truth):\n" . $transcription;
$textParts[] = "Return a compact research record with these headings:\n- Direct observations\n- Representation assumptions\n- Candidate structures\n- Semantic hypotheses (if any)\n- Competing explanations\n- Best falsification / ablation tests\n- Evidence status";

$content = array(array('type' => 'input_text', 'text' => implode("\n\n", $textParts)));
if ($image !== '') {
    $content[] = array('type' => 'input_image', 'image_url' => $image, 'detail' => 'high');
}

$requestBody = array(
    'model' => $model,
    'instructions' => $instructions,
    'input' => array(array('role' => 'user', 'content' => $content)),
    'max_output_tokens' => $profile === 'deep' ? 3500 : 1800,
    'store' => false
);

$requestId = bin2hex(random_bytes(16));
$ch = curl_init('https://api.openai.com/v1/responses');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 15);
curl_setopt($ch, CURLOPT_TIMEOUT, 55);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Authorization: Bearer ' . $apiKey,
    'Content-Type: application/json',
    'Accept: application/json',
    'Idempotency-Key: ' . $requestId
));
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($requestBody, JSON_UNESCAPED_SLASHES));

$upstreamRaw = curl_exec($ch);
$curlError = curl_error($ch);
$status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($upstreamRaw === false) {
    respond(502, array('error' => 'model_unreachable', 'request_id' => $requestId, 'detail' => $curlError));
}
$payload = json_decode($upstreamRaw, true);
if (!is_array($payload)) $payload = array('raw' => $upstreamRaw);
if ($status < 200 || $status >= 300) {
    respond($status > 0 ? $status : 502, array('error' => 'model_error', 'request_id' => $requestId, 'upstream' => $payload));
}

$outputParts = array();
if (isset($payload['output']) && is_array($payload['output'])) {
    foreach ($payload['output'] as $item) {
        if (!isset($item['type']) || $item['type'] !== 'message' || empty($item['content']) || !is_array($item['content'])) continue;
        foreach ($item['content'] as $part) {
            if (isset($part['type'], $part['text']) && $part['type'] === 'output_text' && is_string($part['text'])) {
                $outputParts[] = $part['text'];
            }
        }
    }
}

respond(200, array(
    'object' => 'mimulus_explorer_run',
    'run_id' => $requestId,
    'model' => isset($payload['model']) ? $payload['model'] : $model,
    'profile' => $profile,
    'mode' => $mode,
    'source' => array(
        'image_supplied' => $image !== '',
        'transcription_supplied' => $transcription !== '',
        'note_supplied' => $note !== ''
    ),
    'output' => trim(implode("\n", $outputParts)),
    'usage' => isset($payload['usage']) ? $payload['usage'] : null,
    'mimulus' => array(
        'classification' => 'EXPLORATORY_DECODER_OUTPUT',
        'independent_evidence' => false,
        'warning' => 'This output is a decoder observation, not a decipherment result. Any downstream translation remains lineage-dependent unless independently run from the frozen source.'
    )
));
