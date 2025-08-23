# Hosting statycznej strony w sieci Tor

Poniższe kroki pokazują jak skonfigurować serwer Nginx oraz Tor, aby opublikować statyczną stronę w sieci .onion.

## 1. Przygotowanie plików strony

1. Umieść wszystkie pliki HTML, CSS i inne zasoby w katalogu `/var/www/darkweb666` (lub innym wybranym). Na przykład:
   ```bash
   sudo mkdir -p /var/www/darkweb666
   sudo cp -r docs/* /var/www/darkweb666/
   ```
2. Upewnij się, że pliki mają odpowiednie uprawnienia do odczytu dla użytkownika `www-data` (domyślny użytkownik Nginx).

## 2. Konfiguracja Nginx

Przykładowa konfiguracja serwera w pliku `/etc/nginx/sites-available/darkweb666`:

```nginx
server {
    listen 8080 default_server;
    server_name _;
    root /var/www/darkweb666;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Po zapisaniu pliku utwórz dowiązanie symboliczne:

```bash
sudo ln -s /etc/nginx/sites-available/darkweb666 /etc/nginx/sites-enabled/
```

Następnie przetestuj konfigurację i uruchom ponownie Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

Serwer nasłuchuje lokalnie na porcie `8080`.

## 3. Konfiguracja usługi ukrytej Tor

Edytuj plik `torrc` (zwykle `/etc/tor/torrc`) i dodaj:

```torrc
HiddenServiceDir /var/lib/tor/darkweb666_service
HiddenServicePort 80 127.0.0.1:8080
```

Po zapisaniu pliku uruchom ponownie Tor:

```bash
sudo systemctl restart tor
```

Tor utworzy w katalogu `HiddenServiceDir` dwa pliki: `hostname` (adres .onion) oraz `private_key`. Odczytaj zawartość `hostname`, aby poznać swój adres:

```bash
sudo cat /var/lib/tor/darkweb666_service/hostname
```

## 4. Inne przydatne pliki

* `private_key` w katalogu usługi ukrytej przechowuje klucz prywatny hosta. Zadbaj o jego bezpieczeństwo.
* Plik `torrc` możesz trzymać w repozytorium jako szablon, ale w produkcji warto przechowywać go w domyślnym miejscu (`/etc/tor/torrc`).

Po wykonaniu powyższych kroków statyczna strona będzie dostępna pod otrzymanym adresem `.onion`.
