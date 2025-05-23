# Requires PowerShell 5.1 or later.
# Run this script with Administrator privileges for package installations.

# Function to check if Chocolatey is installed
function Test-ChocolateyInstalled {
    if (Get-Command choco.exe -ErrorAction SilentlyContinue) {
        return $true
    } else {
        return $false
    }
}

# Function to install Chocolatey if not present
function Install-Chocolatey {
    if (-not (Test-ChocolateyInstalled)) {
        Write-Host "🔄 Installing Chocolatey..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072 #TLS 1.2
        try {
            Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
            if (-not (Test-ChocolateyInstalled)) {
                Write-Host "❌ Error: Chocolatey installation failed." -ForegroundColor Red
                exit 1
            }
            Write-Host "✔️ Chocolatey installed successfully." -ForegroundColor Green
        } catch {
            Write-Host "❌ Error: Chocolatey installation failed. $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✔️ Chocolatey is already installed." -ForegroundColor Green
    }
}

# Function to install a Chocolatey package
function Install-ChocoPackage {
    param(
        [string]$PackageName
    )
    Install-Chocolatey # Ensure Chocolatey is installed
    Write-Host "Checking if package '$PackageName' is installed..." -ForegroundColor DarkCyan
    if ((choco list --local-only -r "$PackageName" | Select-String -Quiet "$PackageName")) {
        Write-Host "✔️ '$PackageName' is already installed." -ForegroundColor Green
    } else {
        Write-Host "🔄 Installing package '$PackageName'..." -ForegroundColor Yellow
        try {
            choco install "$PackageName" -y --no-progress
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Error: '$PackageName' installation failed. Chocolatey exit code: $LASTEXITCODE" -ForegroundColor Red
                exit 1
            }
            Write-Host "✔️ '$PackageName' installed successfully." -ForegroundColor Green
        } catch {
            Write-Host "❌ Error: '$PackageName' installation failed. $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }
}

# Function to uninstall a Chocolatey package
function Uninstall-ChocoPackage {
    param(
        [string]$PackageName
    )
    Install-Chocolatey # Ensure Chocolatey is installed
    Write-Host "Checking if package '$PackageName' is installed..." -ForegroundColor DarkCyan
    if ((choco list --local-only -r "$PackageName" | Select-String -Quiet "$PackageName")) {
        Write-Host "🔄 Uninstalling package '$PackageName'..." -ForegroundColor Yellow
        try {
            choco uninstall "$PackageName" -y --no-progress
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Error: '$PackageName' uninstallation failed. Chocolatey exit code: $LASTEXITCODE" -ForegroundColor Red
                exit 1
            }
            Write-Host "✔️ '$PackageName' uninstalled successfully." -ForegroundColor Green
        } catch {
            Write-Host "❌ Error: '$PackageName' uninstallation failed. $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✔️ '$PackageName' is not installed." -ForegroundColor Green
    }
}

# Function to update a Chocolatey package or all packages
function Update-ChocoPackage {
    param(
        [string]$PackageName = "" # Optional parameter
    )
    Install-Chocolatey # Ensure Chocolatey is installed
    if ([string]::IsNullOrEmpty($PackageName)) {
        Write-Host "🔄 Updating all Chocolatey packages..." -ForegroundColor Yellow
        try {
            choco upgrade all -y --no-progress
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Error: All Chocolatey packages update failed. Chocolatey exit code: $LASTEXITCODE" -ForegroundColor Red
                exit 1
            }
            Write-Host "✔️ All Chocolatey packages updated successfully." -ForegroundColor Green
        } catch {
            Write-Host "❌ Error: All Chocolatey packages update failed. $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Checking if package '$PackageName' is installed..." -ForegroundColor DarkCyan
        if ((choco list --local-only -r "$PackageName" | Select-String -Quiet "$PackageName")) {
            Write-Host "🔄 Updating package '$PackageName'..." -ForegroundColor Yellow
            try {
                choco upgrade "$PackageName" -y --no-prress
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "❌ Error: '$PackageName' update failed. Chocolatey exit code: $LASTEXITCODE" -ForegroundColor Red
                    exit 1
                }
                Write-Host "✔️ '$PackageName' updated successfully." -ForegroundColor Green
            } catch {
                Write-Host "❌ Error: '$PackageName' update failed. $($_.Exception.Message)" -ForegroundColor Red
                exit 1
            }
        } else {
            Write-Host "❌ Package '$PackageName' is not installed. Use Install-ChocoPackage to install it first." -ForegroundColor Red
        }
    }
}