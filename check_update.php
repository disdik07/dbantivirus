<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$manifestPath = __DIR__ . '/manifest.json';

if (!file_exists($manifestPath)) {
    http_response_code(404);
    echo json_encode([
        'success' => false,
        'message' => 'Manifest update tidak ditemukan.'
    ]);
    exit;
}

$content = file_get_contents($manifestPath);
echo $content;
