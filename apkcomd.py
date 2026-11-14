#!/usr/bin/env python3
import os
import sys
import urllib.request

REMOTE_DB_URL = "https://raw.githubusercontent.com/ismailefeyuksel66-sudo/apkcomd/main/packages.txt"

def load_remote_database():
    """Uzak sunucudaki (GitHub) paket listesini indirir ve okur."""
    db = {}
    try:
        req = urllib.request.Request(
            REMOTE_DB_URL, 
            headers={"User-Agent": "apkcomd-cli-client"}
        )
        with urllib.request.urlopen(req) as response:
            for line in response:
                decoded_line = line.decode("utf-8").strip()
                if not decoded_line or decoded_line.startswith("#"):
                    continue
                parts = decoded_line.split(maxsplit=1)
                if len(parts) == 2:
                    name, url = parts
                    db[name.lower()] = url
    except Exception as e:
        print(f"[X] Merkezi veritabanına bağlanılamadı: {e}")
    return db

def download_with_progress(url, output_filename):
    """Terminal üzerinde yüzde ve boyut gösteren progress bar."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "apkcomd-cli-client"}
        )
        with urllib.request.urlopen(req) as response:
            total_size = int(response.info().get("Content-Length", 0))
            block_size = 8192
            downloaded = 0

            print(f"\n[+] İndiriliyor: {output_filename}")
            with open(output_filename, "wb") as f:
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        percent = downloaded / total_size
                        bar_len = 30
                        filled_len = int(bar_len * percent)
                        bar = "█" * filled_len + "-" * (bar_len - filled_len)
                        sys.stdout.write(
                            f"\r[{bar}] {percent * 100:.1f}% ({downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB)"
                        )
                        sys.stdout.flush()
                    else:
                        sys.stdout.write(f"\r[Bilgi] İndirilen: {downloaded / 1024 / 1024:.2f} MB")
                        sys.stdout.flush()

            print("\n[✔] İndirme başarıyla tamamlandı!")
    except Exception as e:
        print(f"\n[X] İndirme sırasında hata oluştu: {e}")

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "install":
        print("Kullanım: apkcomd install <paket-adı>")
        sys.exit(1)

    pkg_name = sys.argv[2].lower()
    print("[*] Merkezi veritabanı sorgulanıyor...")
    db = load_remote_database()

    if not db:
        print("[X] Hata: Paket veritabanı yüklenemedi veya boş!")
        sys.exit(1)

    if pkg_name not in db:
        print(f"[X] Hata: '{pkg_name}' paketi depoda bulunamadı!")
        sys.exit(1)

    url = db[pkg_name]
    filename = f"{pkg_name}.apk"

    print(f"Paket Adı : {pkg_name}")
    print(f"Kaynak URL: {url}")
    print(f"Hedef Dizin: {os.getcwd()}/{filename}")

    cevap = input("\nEmin misin? [E/h]: ").strip().lower()
    if cevap in ["h", "hayir", "hayır"]:
        print("[-] İşlem kullanıcı tarafından iptal edildi.")
        sys.exit(0)

    download_with_progress(url, filename)

if __name__ == "__main__":
    main()
