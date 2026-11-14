#!/usr/bin/env bash
set -e

# Renkli çıktı için ANSI kodları
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # Renk sıfırlama

echo -e "${GREEN}[*] apkcomd kurulumu başlatılıyor...${NC}"

# Python3 kontrolü
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[X] Hata: Python3 sisteminizde bulunamadı. Lütfen önce Python3 yükleyin.${NC}"
    exit 1
fi

# GitHub'daki apkcomd.py dosyasının Raw adresi (Kullanıcı adını kendi hesabınla değiştir)
SCRIPT_URL="https://raw.githubusercontent.com/ismailefeyuksel66-sudo/apkcomd/main/apkcomd.py"
INSTALL_PATH="/usr/local/bin/apkcomd"

echo -e "${GREEN}[*] Betik uzak depodan indiriliyor...${NC}"
# sudo yetkisiyle doğrudan /usr/local/bin altına indiriyoruz
if command -v curl &> /dev/null; then
    sudo curl -sSL "$SCRIPT_URL" -o "$INSTALL_PATH"
elif command -v wget &> /dev/null; then
    sudo wget -qO "$INSTALL_PATH" "$SCRIPT_URL"
else
    echo -e "${RED}[X] Hata: curl veya wget komutlarından biri gereklidir.${NC}"
    exit 1
fi

echo -e "${GREEN}[*] Çalıştırma izinleri tanımlanıyor...${NC}"
sudo chmod +x "$INSTALL_PATH"

echo -e "\n${GREEN}[✔] Kurulum başarıyla tamamlandı!${NC}"
echo "Artık terminalde herhangi bir yerde şu komutu kullanabilirsin:"
echo -e "  ${GREEN}apkcomd install <paket-adi>${NC}"
