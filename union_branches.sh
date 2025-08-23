#!/bin/bash

# Pobierz i zaktualizuj wszystkie branche z origin
git fetch --all

# Zrób nowego brancha MISTRZ na bazie main
git checkout main
git pull
git checkout -b MISTRZ

# Zbierz wszystkie istniejące branche do tablicy (poza HEAD)
branches=$(git branch -r | grep -v HEAD | grep -v main | grep -v MISTRZ | sed 's/origin\///g' | sort | uniq)

for branch in $branches
do
    echo "PRZETWARZAM: $branch"
    # Stwórz tymczasowy katalog
    mkdir -p /tmp/gitmerge_$branch

    # Przełącz się na danego brancha i skopiuj wszystkie pliki do tymczasowego katalogu
    git checkout $branch
    rsync -a --exclude='.git' ./ /tmp/gitmerge_$branch/

    # Wróć do brancha MISTRZ
    git checkout MISTRZ

    # Skopiuj wszystko z tymczasowego katalogu do projektu (nadpisuje pliki o tych samych nazwach!)
    rsync -a /tmp/gitmerge_$branch/ ./
done

# Usuń pliki tymczasowe
rm -rf /tmp/gitmerge_*

# Dodaj i zacommituj całość
git add .
git commit -m "TOTAL UNION wszystkich plików z każdego brancha do MISTRZ"
git push -u origin MISTRZ

echo "DONE. Wszystkie pliki ze wszystkich branchy powinny być w branchu MISTRZ"
