@echo off
title Auto Sync Database Threat Feeds
cd /d "%~dp0"
echo [*] Menjalankan sinkronisasi database dari MalwareBazaar, ThreatFox, dan ClamAV...
python sync_malware_feed.py
echo [OK] manifest.json dan paket update berhasil diperbarui!
timeout /t 5
