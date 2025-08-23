# oczyszczanie_mp3.py
from mutagen.id3 import ID3, ID3NoHeaderError

in_f  = "kingaszczepanekcpun.mp3"
out_f = "kingaszczepanekcpun_clean.mp3"

try:
    tags = ID3(in_f)
    tags.delete()
    tags.save(out_f)
    print("Usunięto tagi ID3.")
except ID3NoHeaderError:
    print("Brak tagów ID3 — plik już czysty.")
