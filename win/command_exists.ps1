# Function to check if a command exists in PowerShell
function Test-CommandExists {
    param(
        [string]$CommandName
    )
    if (Get-Command "$CommandName" -ErrorAction SilentlyContinue) {
        Write-Host "✔️ Command '$CommandName' exists." -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ Command '$CommandName' does not exist." -ForegroundColor Red
        return $false
    }
}