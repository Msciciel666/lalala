#!/usr/bin/env bash
set -euo pipefail
# Maksymalny IOC grepper (LINUX)
TARGET_DIR="${1:?Podaj katalog do analizy!}"
OUT_DIR="ioc_results"
mkdir -p "$OUT_DIR"

PATTERNS=(
  "IPv4:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)(?:\\.(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)){3}"
  "IPv6:(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}"
  "URL:https?://[A-Za-z0-9\\-\\.]+(?:/[\\w\\-\\.~:/?#[\\]@!$&'()*+,;=%]*)?"
  "Email:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
  "Onion:[a-z2-7]{16}\\.onion|[a-z0-9]{56}\\.onion"
  "AWS_ID:AKIA[0-9A-Z]{16}"
  "AWS_Secret:[0-9a-zA-Z/+]{40}"
  "JWT:eyJ[A-Za-z0-9-_]+?\\.[A-Za-z0-9-_]+?\\.[A-Za-z0-9-_]+?"
  "MD5:[a-f0-9]{32}"
  "SHA1:[a-f0-9]{40}"
  "SHA256:[A-Fa-f0-9]{64}"
  "BTC:[13][a-km-zA-HJ-NP-Z1-9]{25,34}"
  "Phone:\\+?[0-9][0-9 \\-]{7,}[0-9]"
  "UUID:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
)

for pat in "${PATTERNS[@]}"; do
  IFS=":" read -r name regex <<< "$pat"
  rg --pcre2 -o "$regex" -n "$TARGET_DIR" | sort | uniq > "$OUT_DIR/${name}.ioc.txt"
  echo "[+] Zapisano $name → $OUT_DIR/${name}.ioc.txt"
done

# Dodatkowy OCR
if compgen -G "$TARGET_DIR"/*.{jpg,png} > /dev/null; then
  mkdir -p "$OUT_DIR/OCR"
  for img in "$TARGET_DIR"/*.{jpg,png}; do
    [ -e "$img" ] || continue
    tesseract "$img" stdout -l eng+pol | rg --pcre2 -o '\\w{4,}' | sort | uniq >> "$OUT_DIR/text.ioc.txt"
  done
  echo "[+] OCR zakończony"
fi
