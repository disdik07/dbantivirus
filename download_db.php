<?php
$manifestPath = __DIR__ . '/manifest.json';

if (!file_exists($manifestPath)) {
    http_response_code(404);
    echo "Manifest not found.";
    exit;
}

$manifest = json_decode(file_get_contents($manifestPath), true);
$downloadUrl = $manifest['download_url'] ?? '';

// Fallback jika direct update file diminta
$filename = basename($downloadUrl);
$filePath = __DIR__ . '/updates/' . $filename;

if (file_exists($filePath)) {
    header('Content-Description: File Transfer');
    header('Content-Type: application/json');
    header('Content-Disposition: attachment; filename="' . $filename . '"');
    header('Expires: 0');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    header('Content-Length: ' . filesize($filePath));
    readfile($filePath);
    exit;
} else {
    http_response_code(404);
    echo "Update file not found.";
}
