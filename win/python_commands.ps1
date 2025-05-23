# Function to install a Python package using pip (for Windows)
function Install-PythonPackage {
    param(
        [string]$PackageName
    )
    Write-Host "Checking if 'python.exe' is in PATH..." -ForegroundColor DarkCyan
    if (-not (Get-Command python.exe -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Error: Python is not found in your PATH. Please install Python and ensure it's in your PATH." -ForegroundColor Red
        exit 1
    }

    Write-Host "Checking if Python package '$PackageName' is installed..." -ForegroundColor DarkCyan
    try {
        # Using pip show to check if package is installed
        $checkResult = (pip show $PackageName 2>&1 | Out-String)
        if ($checkResult -match "Name: $PackageName") {
            Write-Host "✔️ Python package '$PackageName' is already installed." -ForegroundColor Green
        } else {
            Write-Host "🔄 Installing Python package '$PackageName'..." -ForegroundColor Yellow
            # Using --break-system-packages (Python 3.11+) or --user for user-specific
            # Consider --user if you don't want to use sudo/admin
            pip install "$PackageName" --break-system-packages # Use --user if you prefer
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Error: Python package '$PackageName' installation failed. Pip exit code: $LASTEXITCODE" -ForegroundColor Red
                exit 1
            }
            Write-Host "✔️ Python package '$PackageName' installed successfully." -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Error checking/installing Python package: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}

# Function to uninstall a Python package using pip (for Windows)
function Uninstall-PythonPackage {
    param(
        [string]$PackageName
    )
    Write-Host "Checking if 'python.exe' is in PATH..." -ForegroundColor DarkCyan
    if (-not (Get-Command python.exe -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Error: Python is not found in your PATH. Cannot uninstall Python package." -ForegroundColor Red
        exit 1
    }

    Write-Host "Checking if Python package '$PackageName' is installed..." -ForegroundColor DarkCyan
    try {
        $checkResult = (pip show $PackageName 2>&1 | Out-String)
        if ($checkResult -match "Name: $PackageName") {
            Write-Host "🔄 Uninstalling Python package '$PackageName'..." -ForegroundColor Yellow
            pip uninstall -y "$PackageName" # -y automatically confirms
            if ($LASTEXITCODE -ne 0) {
                Write-Host "❌ Error: Python package '$PackageName' uninstallation failed. Pip exit code: $LASTEXITCODE" -ForegroundColor Red
                exit 1
            }
            Write-Host "✔️ Python package '$PackageName' uninstalled successfully." -ForegroundColor Green
        } else {
            Write-Host "✔️ Python package '$PackageName' is not installed." -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Error checking/uninstalling Python package: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}