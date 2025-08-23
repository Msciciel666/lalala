$inputFile  = 'podejrzane_base64.txt'
$outputFile = 'decoded_base64.txt'

# Pattern: szukamy wrażliwych słów w wyniku dekodowania
$sensitivePattern = 'haslo|password|pass|key|secret|token|login|auth|api|credential|private|jwt'

# Zerujemy plik wyjściowy
Set-Content -Path $outputFile -Value ""

Get-Content $inputFile | ForEach-Object {
    $base64 = $_.Trim()
    try {
        # Próbujemy dekodować jako base64 do bajtów
        $bytes = [System.Convert]::FromBase64String($base64)
        # Próbujemy zamienić na tekst (UTF-8)
        $decoded = [System.Text.Encoding]::UTF8.GetString($bytes)
        # Filtrujemy "drukowalne" wyniki oraz te zawierające wrażliwe frazy
        if ($decoded -match '\p{L}' -and $decoded -match $sensitivePattern) {
            # Format: oryginał -> dekod
            Add-Content -Path $outputFile -Value "$base64 -> $decoded"
        }
    } catch {
        # Jeśli niepoprawne base64, pomijamy
        continue
    }
}
Write-Host "Decoding complete. Results in $outputFile" -ForegroundColor Green

