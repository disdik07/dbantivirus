import os
import json
import hashlib
import time
import sqlite3

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
UPDATES_DIR = os.path.join(SERVER_DIR, "updates")
CLIENT_DIR = os.path.abspath(os.path.join(SERVER_DIR, "..", "client"))
CLIENT_DATA_DIR = os.path.join(CLIENT_DIR, "data")
CLIENT_DB_PATH = os.path.join(CLIENT_DATA_DIR, "signatures.db")

os.makedirs(UPDATES_DIR, exist_ok=True)
os.makedirs(CLIENT_DATA_DIR, exist_ok=True)

# 1. Base initial signatures (ditanamkan di client v2026.09.10.01)
INITIAL_SIGNATURES = [
    {
        "threat_name": "Trojan.Win32.GenericBackdoor",
        "threat_type": "Trojan",
        "severity": "High",
        "hash_sha256": "44d88612fea8a8f36de82e1278abb02f1a23b4c5d6e7f8a9b0c1d2e3f4a5b6c7",
        "hash_md5": "44d88612fea8a8f36de82e1278abb02f",
        "description": "Backdoor trojan yang membuka port remote access."
    },
    {
        "threat_name": "Ransom.Win32.WannaCry.A",
        "threat_type": "Ransomware",
        "severity": "Critical",
        "hash_sha256": "ed01ebf83334a193731427b5b9479b17a4dd42283b0f7924f7b9e0d16df39a29",
        "hash_md5": "84c82835a5d21bbcf75a61706d8ab549",
        "description": "Varian ransomware WannaCry yang mengenkripsi file korban."
    },
    {
        "threat_name": "Spyware.KeyLogger.Zeus",
        "threat_type": "Spyware",
        "severity": "High",
        "hash_sha256": "25442f99d94943f05cefe57700e16e625a528e17b88939c39c4a864d4ef7495b",
        "hash_md5": "3f2e1a4b5c6d7e8f90a1b2c3d4e5f6a7",
        "description": "Perekam ketikan keyboard untuk mencuri kredensial perbankan."
    },
    {
        "threat_name": "CoinMiner.Win64.XMRigStealth",
        "threat_type": "CoinMiner",
        "severity": "Medium",
        "hash_sha256": "b5a92a548c267c7e0f2d7a6e1f0e4b8a2c1d3e5f7a9b0c2d4e6f8a1b3c5d7e9f",
        "hash_md5": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
        "description": "Penambang cryptocurrency ilegal yang membebani CPU sistem."
    },
    {
        "threat_name": "EICAR-Test-Hash",
        "threat_type": "Test.File",
        "severity": "Low",
        "hash_sha256": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
        "hash_md5": "44d88612fea8a8f36de82e1278abb02f",
        "description": "Hash standar untuk verifikasi deteksi EICAR."
    }
]

# 2. Update signatures v2026.09.11.01 (Ancaman baru yang ada di update server)
UPDATE_SIGNATURES = INITIAL_SIGNATURES + [
    {
        "threat_name": "Ransom.Win64.LockBit3.Black",
        "threat_type": "Ransomware",
        "severity": "Critical",
        "hash_sha256": "d8e8fca2dc0f896fd7cb4cb0031ba249f7cd90b34382cc39328229b47e2ef738",
        "hash_md5": "c0556277a942978a9c4033324c53c44e",
        "description": "Ransomware LockBit 3.0 yang menonaktifkan sistem pertahanan."
    },
    {
        "threat_name": "Infostealer.Win32.RedLine",
        "threat_type": "InfoStealer",
        "severity": "High",
        "hash_sha256": "71c08e50b7cae636b043b2a2b724f7e271cf5ff8c2ef40b8fb7b2fb0a187ff68",
        "hash_md5": "7b0a70f5e1b2c3d4e5f6a7b8c9d0e1f2",
        "description": "Pencuri cookie browser, password tersimpan, dan wallet crypto."
    },
    {
        "threat_name": "Worm.Win32.Morto.B",
        "threat_type": "Worm",
        "severity": "High",
        "hash_sha256": "9b71d224bd62f3785d96d46ad3ea3d733100e3046d1c022f2da6cce5a2cac832",
        "hash_md5": "9b71d224bd62f3785d96d46ad3ea3d73",
        "description": "Worm yang menyebar mandiri melalui port RDP Windows."
    },
    {
        "threat_name": "Rootkit.Win64.TDSS",
        "threat_type": "Rootkit",
        "severity": "Critical",
        "hash_sha256": "8f434346648f6b96df89dda901c5176b10e6d0ce180e058c4225d25e0c525f02",
        "hash_md5": "8f434346648f6b96df89dda901c5176b",
        "description": "Rootkit kernel mode yang menyembunyikan aktivitas berbahaya."
    }
]

def build_client_initial_db():
    """Inisialisasi database lokal bawaan client v2026.09.10.01"""
    if os.path.exists(CLIENT_DB_PATH):
        os.remove(CLIENT_DB_PATH)

    conn = sqlite3.connect(CLIENT_DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT)")
    cur.execute("""
        CREATE TABLE signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash_sha256 TEXT UNIQUE,
            hash_md5 TEXT,
            threat_name TEXT NOT NULL,
            threat_type TEXT DEFAULT 'Trojan',
            severity TEXT DEFAULT 'High',
            description TEXT,
            added_date TEXT
        )
    """)
    cur.execute("CREATE INDEX idx_sha256 ON signatures(hash_sha256)")
    cur.execute("CREATE INDEX idx_md5 ON signatures(hash_md5)")

    cur.execute("INSERT INTO metadata (key, value) VALUES ('version', '2026.09.10.01')")
    cur.execute("INSERT INTO metadata (key, value) VALUES ('last_updated', '2026-09-10 00:00:00')")

    for sig in INITIAL_SIGNATURES:
        cur.execute("""
            INSERT INTO signatures (hash_sha256, hash_md5, threat_name, threat_type, severity, description, added_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            sig["hash_sha256"].lower(),
            sig.get("hash_md5", "").lower(),
            sig["threat_name"],
            sig.get("threat_type", "Trojan"),
            sig.get("severity", "High"),
            sig.get("description", ""),
            "2026-09-10 00:00:00"
        ))
    conn.commit()
    conn.close()
    print(f"[OK] Database awal client dibuat: {len(INITIAL_SIGNATURES)} signatures.")

def build_server_update_package():
    """Membuat paket rilis update di server (v2026.09.11.01)"""
    update_file_name = "signatures_update_2026.09.11.json"
    update_file_path = os.path.join(UPDATES_DIR, update_file_name)

    payload = {
        "version": "2026.09.11.01",
        "release_date": "2026-09-11",
        "signatures_count": len(UPDATE_SIGNATURES),
        "signatures": UPDATE_SIGNATURES
    }

    content_bytes = json.dumps(payload, indent=2).encode('utf-8')
    with open(update_file_path, "wb") as f:
        f.write(content_bytes)

    # Hitung SHA-256 dari file rilis
    sha256_hash = hashlib.sha256(content_bytes).hexdigest()

    # Buat manifest.json di server
    manifest = {
        "version": "2026.09.11.01",
        "release_date": "2026-09-11",
        "signatures_count": len(UPDATE_SIGNATURES),
        "changelog": "Menambahkan signature untuk Ransomware LockBit 3.0, RedLine InfoStealer, Worm Morto, dan Rootkit TDSS.",
        "download_url": f"http://localhost/antivirus/server/updates/{update_file_name}",
        "sha256": sha256_hash,
        "format": "json"
    }

    manifest_path = os.path.join(SERVER_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[OK] Server update package dibuat: v2026.09.11.01 (SHA256: {sha256_hash[:16]}...)")

if __name__ == "__main__":
    build_client_initial_db()
    build_server_update_package()
