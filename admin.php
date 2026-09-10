<?php
$manifestPath = __DIR__ . '/manifest.json';
$output = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['sync_now'])) {
    // Jalankan python sync_malware_feed.py
    $cmd = 'python ' . escapeshellarg(__DIR__ . '/sync_malware_feed.py') . ' 2>&1';
    $output = shell_exec($cmd);
}

$manifest = file_exists($manifestPath) ? json_decode(file_get_contents($manifestPath), true) : null;
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>ApexGuard Server Update Control Panel</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0B0F19; color: #F9FAFB; padding: 40px 20px; margin: 0; }
        .container { max-width: 780px; margin: 0 auto; background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        h1 { color: #06B6D4; margin-top: 0; font-size: 24px; display: flex; align-items: center; gap: 10px; }
        .badge { background: #064E3B; color: #10B981; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; }
        .card { background: #1F2937; padding: 18px; border-radius: 8px; margin: 20px 0; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .btn { background: #10B981; color: white; border: none; padding: 12px 24px; font-size: 15px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.2s; display: inline-flex; align-items: center; gap: 8px; }
        .btn:hover { background: #059669; }
        pre { background: #080C14; color: #10B981; padding: 15px; border-radius: 8px; overflow-x: auto; font-family: Consolas, monospace; font-size: 13px; max-height: 250px; }
        .label { color: #9CA3AF; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
        .value { font-size: 18px; font-weight: bold; color: #F3F4F6; margin-top: 4px; }
    </style>
</head>
<body>

<div class="container">
    <h1>🛡️ ApexGuard Server Update Manager <span class="badge">Master Server</span></h1>
    <p style="color: #9CA3AF;">Halaman kontrol server untuk mengelola pembaruan <code>manifest.json</code> secara otomatis dari 3 sumber database global.</p>

    <div class="card">
        <div class="grid">
            <div>
                <div class="label">Versi Database di manifest.json</div>
                <div class="value" style="color: #06B6D4;"><?= htmlspecialchars($manifest['version'] ?? 'Belum ada') ?></div>
            </div>
            <div>
                <div class="label">Total Signature Aktif</div>
                <div class="value" style="color: #10B981;"><?= number_format($manifest['signatures_count'] ?? 0) ?> Signatures</div>
            </div>
            <div>
                <div class="label">Tanggal Rilis Server</div>
                <div class="value"><?= htmlspecialchars($manifest['release_date'] ?? '-') ?></div>
            </div>
            <div>
                <div class="label">File Manifest URL</div>
                <div class="value" style="font-size: 13px; color: #9CA3AF;"><a href="manifest.json" target="_blank" style="color: #06B6D4;">manifest.json</a></div>
            </div>
        </div>
    </div>

    <form method="POST">
        <button type="submit" name="sync_now" class="btn">
            🔄 Tarik Data Terbaru & Update manifest.json Sekarang
        </button>
    </form>

    <?php if ($output): ?>
        <h3 style="margin-top: 25px; color: #F3F4F6;">📋 Log Proses Sinkronisasi:</h3>
        <pre><?= htmlspecialchars($output) ?></pre>
    <?php endif; ?>
</div>

</body>
</html>
