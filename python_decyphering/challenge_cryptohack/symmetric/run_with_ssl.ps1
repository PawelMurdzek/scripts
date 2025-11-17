# PowerShell script to run Python with SSL support
param(
    [Parameter(Mandatory=$true)]
    [string]$ScriptPath
)

$env:PATH = "C:\jezyki\python\anaconda\Library\bin;$env:PATH"
& C:/jezyki/python/anaconda/python.exe $ScriptPath
