$a = New-Object System.Collections.Generic.List[byte[]]
while ($true) {
  $chunk = New-Object byte[] (33554432)   # 32 MB
  $a.Add($chunk)
  Start-Sleep -Milliseconds 150
}
