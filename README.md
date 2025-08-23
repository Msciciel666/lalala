1  # darkweb666
2
3  darkweb666 to modularne narzędzie do OSINT, monitoringu dark web oraz analizy wycieków z ukrytych forów i pastebinów.
4  Przeznaczone dla zespołów bezpieczeństwa, analityków threat intelligence oraz użytkowników chcących monitorować zagrożenia związane z .onion i wyciekami danych.
5
6  ## Kluczowe funkcjonalności
7
8  - Automatyczne skanowanie i indeksowanie stron .onion (Tor v3)
9  - Wyszukiwanie wycieków (email, nick, domena, numer telefonu)
10  - Crawler forów, parser dumpów .csv/.sql/.json
11  - Alerty o nowych wyciekach – integracja z webhookami, komunikatory
12  - Analiza metadanych (EXIF) z plików obrazów
13  - Integracja z narzędziami blue-team (SIEM, systemy automatyzacji)
14  - API REST (automatyzacja i zewnętrzne integracje)
15
16  ## Planowana architektura
17  Poniżej opisano katalogi przewidziane dla docelowej wersji projektu.
18  Aktualne repozytorium zawiera jedynie proste skrypty (`monitor_onion.py`,
19  `oczyszczanie_exif.py`) oraz statyczne zasoby w katalogu `docs`.
20  - `/core` – główny silnik skanowania i parser dumpów
21  - `/scanner` – crawler dla .onion (obsługa pluginów)
22  - `/api` – serwis HTTP (np. Flask/FastAPI)
23  - `/integrations` – adaptery do SIEM/webhooków/komunikatorów
24  - `/web` – panel webowy do obsługi alertów
25  - `/utils` – funkcje pomocnicze
26  - `/tests` – zestaw testów automatycznych
27
28  ## Wymagania
29
30  - Python 3.10+
31  - Tor (localhost:9050)
32  - Redis (opcjonalnie)
33  - Node.js 18+ (frontend)
34  - Docker (deployment całości)
35  - Linux/Mac/WSL (wsparcie Windows ograniczone)
36  - Git LFS (obsługa dużych plików multimedialnych)
37
38  ## Instalacja (dev)
39
40  ```bash
41  git clone <repo-url>
42  cd darkweb666
43  git lfs install
44  git lfs pull
45  python3 -m venv venv
46  source venv/bin/activate
47  pip install -r requirements.txt
48  # Uruchom TOR: service tor start
49  python core/main.py --scan --onion
50  Szybki start
51  Skonfiguruj plik .env na podstawie .env.example
52
53  Uruchom Tor na localhost:9050
54
55  Włącz silnik skanowania:
56  python core/main.py --scan --onion --threads 8
57
58  (Opcjonalnie) Uruchom panel web:
59  cd web && npm install && npm run dev
60
61  (Opcjonalnie) Skonfiguruj integracje: webhook, SIEM
62
63  Przykłady użycia
64  python core/main.py --scan --onion --search <email>
65
66  python scanner/crawl.py --forum <forum> --dump output.csv
67
68  curl http://localhost:8000/api/search?nick=<nickname>
69
70  Bezpieczeństwo i etyka
71  Narzędzie wyłącznie do celów badawczych/edukacyjnych.
72
73  Ataki ofensywne domyślnie wyłączone.
74
75  Wspiera odpowiedzialne ujawnianie podatności (responsible disclosure).

77  ## Licencja
78
79  Projekt udostępniany jest na licencji MIT. Szczegóły znajdują się w pliku
80  `LICENSE` w katalogu głównym repozytorium.