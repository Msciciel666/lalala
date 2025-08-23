# -*- coding: utf-8 -*-
import os
import pytesseract
import zipfile
from PIL import Image
import io
import csv
import sys

# === Konfiguracja ścieżek ===
TESSERACT_CMD = r"C:\Users\Kinga\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
TESSDATA_PREFIX = r"C:\Users\Kinga\AppData\Local\Programs\Tesseract-OCR\tessdata\\"
ZIP_PATH = 'zdjecia.zip'           # Ścieżka do ZIP ze zdjęciami
OUT_CSV = 'ocr_zip_results.csv'    # Ścieżka do CSV z wynikami
LOG_PATH = 'ocr_errors.log'        # Log błędów
LANGS = 'pol'                      # Języki do OCR (np. 'pol', 'eng', 'pol+eng')

# === Ustawienia środowiska ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Kinga\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
os.environ['TESSDATA_PREFIX'] = r"C:\Users\Kinga\AppData\Local\Programs\Tesseract-OCR\tessdata\\"

# === Walidacja obecności ZIP ===
if not os.path.exists(ZIP_PATH):
    print(f"[FATAL] Brak pliku: {ZIP_PATH}")
    sys.exit(1)

# === Otwarcie pliku logów ===
logf = open(LOG_PATH, 'w', encoding='utf-8')

# === Przetwarzanie obrazów z ZIP ===
with zipfile.ZipFile(ZIP_PATH, 'r') as zipf, open(OUT_CSV, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['plik', 'tekst'])
    writer.writeheader()
    images = [f for f in zipf.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    total = len(images)
    print(f"[INFO] Znaleziono {total} obrazów w ZIP!")

    for idx, fname in enumerate(images, 1):
        try:
            with zipf.open(fname) as img_file:
                img = Image.open(io.BytesIO(img_file.read()))
                # Dla bezpieczeństwa konwertuj do RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # OCR
                text = pytesseract.image_to_string(img, lang=LANGS)
            writer.writerow({'plik': fname, 'tekst': text})
            print(f"[{idx}/{total}] {fname} OK")
        except Exception as e:
            writer.writerow({'plik': fname, 'tekst': f'BŁĄD: {e}'})
            logf.write(f"[{idx}/{total}] {fname} BŁĄD: {e}\n")
            print(f"[{idx}/{total}] {fname} BŁĄD: {e}")

logf.close()
print(f"\n✅ Gotowe! Wszystko zapisane w {OUT_CSV}")
print(f"❗ Błędy zapisane w {LOG_PATH} (jeśli wystąpiły)")
