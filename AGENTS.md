# AGENTS.md

**Instrukcje dla agentów AI oraz narzędzi automatyzujących pracę z repozytorium darkweb666**

---

## Konwencje kodowania

- Stosuj PEP8 dla Pythona; dla JavaScript – ESLint Standard.
- Każda nowa funkcja/moduł wymaga docstringa i minimum 1 testu jednostkowego.
- Nazewnictwo plików: snake_case dla Python, kebab-case dla frontend.
- Unikaj duplikowania logiki, stosuj DRY (Don't Repeat Yourself).

## Organizacja projektu

- **/core** – logika główna, nie wolno zmieniać bez aktualizacji testów w /tests.
- **/scanner** – nowe pluginy mają mieć prefiks `plugin_`, muszą być rejestrowane w głównym module loadera.
- **/api** – endpointy REST, wymagany Swagger (OpenAPI) docstring dla każdego route.
- **/integrations** – osobne katalogi dla każdego SIEM/webhook/integracji.
- **/web** – frontend, minimalnie testowane E2E, preferowany Cypress.
- **/utils** – tylko uniwersalne funkcje; każda funkcja musi być użyta przynajmniej raz w projekcie.

## Testowanie

- Każda zmiana w /core i /scanner musi uruchamiać pytest:  
  `pytest --cov=core,scanner --maxfail=1`
- Dla frontend:  
  `npm run test`
- PR bez przechodzących testów automatycznie odrzucany.

## Bezpieczeństwo

- Nie zapisuj danych użytkownika na dysku poza katalogiem /dumps.
- Nie loguj credentiali, tokenów API, numerów kart, itp.
- Endpointy API wymagają walidacji wejścia i ograniczenia rate limiting.
- Kod ofensywny (brute-force, exploit) ma być domyślnie zakomentowany.

## Dobre praktyki

- Każdy commit powinien mieć opis zmian i numer powiązanego issue (jeśli dotyczy).
- Nowe funkcje i klasy muszą mieć komentarz wyjaśniający zastosowanie.
- Pull Requesty mają opis zmian oraz checklistę testów.
- Przed merge – automatyczne formatowanie kodu (`black`, `prettier`).

## Przykładowe zadania dla agenta

- "Przeprowadź audyt bezpieczeństwa kodu w katalogu /core i wygeneruj raport do SECURITY.md"
- "Dodaj testy jednostkowe do wszystkich endpointów w /api"
- "Zidentyfikuj powtarzający się kod w /utils i zaproponuj refaktoryzację"
- "Przeanalizuj najnowszy dump z /dumps pod kątem występowania nieprawidłowych rekordów"

---

**Ten plik nie zawiera żadnych danych personalnych. Może być publicznie analizowany przez dowolny agent AI.**
