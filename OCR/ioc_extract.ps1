$patterns = @{
  IPv4='(?:25[0-5]|2[0-4]\d|[01]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[01]?\d?\d)){3}';
  Email='[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}';
  GUID='[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}';
  Onion='[a-z2-7]{16}\.onion|[a-z0-9]{56}\.onion';
}
Get-ChildItem -Recurse -File | ForEach-Object {
  $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
  foreach ($name in $patterns.Keys) {
    $regex = $patterns[$name]
    if ($content -match $regex) {
      $matches = [regex]::Matches($content,$regex)
      $matches | ForEach-Object { $_.Value } | Select-Object -Unique | Out-File "ioc_$name.txt" -Append
    }
  }
}
Write-Host 'IOC extraction complete.'