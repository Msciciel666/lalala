#!/usr/bin/env python
# --------- local_analysis.py ---------
import argparse, os, re, json, pathlib, string
from collections import Counter
from tqdm import tqdm

import pytesseract
from PIL import Image
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# --------------- konfiguracja podstawowa ---------------
DEFAULT_LANG = "pol"
BAD_WORDS_PL = {
    "kurwa", "chuj", "pizda", "pierdol", "jebac", "skurwysyn", "cipa",
    "kutas", "dupa", "huj", "sukinsyn", "dziwka", "fiut"
}
# -------------------------------------------------------

def clean_text(txt: str) -> str:
    txt = txt.replace("\n", " ").replace("\r", " ")
    txt = re.sub(r"\s{2,}", " ", txt)           # wielokrotne spacje
    txt = re.sub(r"[^\x20-\x7EĄąĆćĘęŁłŃńÓóŚśŹźŻż]", "", txt)  # znak sterujący
    return txt.strip()

def basic_stats(txt: str) -> dict:
    words = txt.split()
    sentences = nltk.tokenize.sent_tokenize(txt, language="polish")
    word_count = len(words)
    sent_count = len(sentences) if sentences else 1
    upper_words = [w for w in words if w.isupper() and len(w) > 1]

    stats = {
        "char_count": len(txt),
        "word_count": word_count,
        "sentence_count": sent_count,
        "avg_word_len": round(sum(len(w) for w in words) / word_count, 2) if word_count else 0,
        "avg_sent_len": round(word_count / sent_count, 2) if sent_count else 0,
        "exclamation_count": txt.count("!"),
        "question_count": txt.count("?"),
        "upper_word_ratio": round(len(upper_words) / word_count, 3) if word_count else 0,
    }
    # wulgaryzmy
    lowered = [w.lower().strip(string.punctuation) for w in words]
    vulgar_hits = sum(1 for w in lowered if w in BAD_WORDS_PL)
    stats["vulgar_count"] = vulgar_hits
    return stats

def sentiment_vader(txt: str, sia: SentimentIntensityAnalyzer) -> dict:
    score = sia.polarity_scores(txt)
    return {
        "sent_neg": score["neg"],
        "sent_neu": score["neu"],
        "sent_pos": score["pos"],
        "sent_compound": score["compound"],
    }

def process_image(path: pathlib.Path, tess_cmd: str | None, sia: SentimentIntensityAnalyzer):
    if tess_cmd:
        pytesseract.pytesseract.tesseract_cmd = tess_cmd

    text = pytesseract.image_to_string(Image.open(path), lang=DEFAULT_LANG)
    text = clean_text(text)
    stats = basic_stats(text)
    senti = sentiment_vader(text, sia)
    return {
        "file_name": path.name,
        "text": text if text else "[brak tekstu]",
        **stats,
        **senti,
    }

def main():
    nltk.download("punkt", quiet=True)
    sia = SentimentIntensityAnalyzer()

    parser = argparse.ArgumentParser(description="Lokalna analiza screenshotów bez API")
    parser.add_argument("img_dir", nargs="?", default="./screenshots", help="katalog z obrazami")
    parser.add_argument("out_csv", nargs="?", default="results.csv", help="plik wynikowy CSV")
    parser.add_argument("--tess-cmd", help="pełna ścieżka do tesseract.exe (jeśli nie w PATH)")
    args = parser.parse_args()

    img_dir = pathlib.Path(args.img_dir)
    images = [p for p in img_dir.glob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    if not images:
        print(f"[!] Brak obrazów w {img_dir}")
        return

    rows = []
    for img in tqdm(images, desc="OCR + analiza"):
        rows.append(process_image(img, args.tess_cmd, sia))

    df = pd.DataFrame(rows)
    df.to_csv(args.out_csv, index=False, encoding="utf-8-sig")
    print(f"\n[✔] Zapisano {len(df)} rekordów do {args.out_csv}")

    # Zbiorcze podsumowanie
    summary = {
        "Średnia długość zdania": round(df["avg_sent_len"].mean(), 2),
        "Średni sentyment (-1..1)": round(df["sent_compound"].mean(), 3),
        "Średni udział wulgaryzmów": round(df["vulgar_count"].mean(), 2),
        "Średnia liczba wykrzykników": round(df["exclamation_count"].mean(), 2),
    }
    print("\n--- PODSUMOWANIE ---")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
# --------- EOF ----------------------------------------
