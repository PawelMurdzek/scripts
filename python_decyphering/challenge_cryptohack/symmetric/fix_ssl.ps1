# Script to diagnose and fix SSL issue in Anaconda

$anacondaPath = "C:\jezyki\python\anaconda"
$dllPath = "$anacondaPath\Library\bin"

Write-Host "Checking for OpenSSL DLLs in: $dllPath" -ForegroundColor Cyan

$requiredDlls = @("libssl-1_1-x64.dll", "libcrypto-1_1-x64.dll")

foreach ($dll in $requiredDlls) {
    $fullPath = Join-Path $dllPath $dll
    if (Test-Path $fullPath) {
        Write-Host "[OK] Found: $dll" -ForegroundColor Green
    } else {
        Write-Host "[MISSING] Not found: $dll" -ForegroundColor Red
    }
}

Write-Host "`nSearching for OpenSSL DLLs in Anaconda directory..." -ForegroundColor Cyan
Get-ChildItem -Path $anacondaPath -Recurse -Filter "libssl*.dll" -ErrorAction SilentlyContinue | Select-Object FullName
Get-ChildItem -Path $anacondaPath -Recurse -Filter "libcrypto*.dll" -ErrorAction SilentlyContinue | Select-Object FullName

Write-Host "`n=== SOLUTIONS ===" -ForegroundColor Yellow
Write-Host "1. Reinstall OpenSSL in conda:"
Write-Host "   conda install -c anaconda openssl"
Write-Host "`n2. Or reinstall Python in conda:"
Write-Host "   conda install python=3.8.5 --force-reinstall"
Write-Host "`n3. Or download OpenSSL DLLs manually from:"
Write-Host "   https://slproweb.com/products/Win32OpenSSL.html"
