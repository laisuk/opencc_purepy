$env:TEMP = "C:\Temp"
$env:TMP = "C:\Temp"

$pathsToClean = @("dist", "build", "*.egg-info")
foreach ($path in $pathsToClean) {
    if (Test-Path $path) {
        Write-Host "🧹 Removing $path ..."
        Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "🚀 Building package..."
python -m build
