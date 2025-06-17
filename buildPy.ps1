# Set strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Go to the automation folder
Write-Host "Navigating to automation folder..."
Set-Location -Path "./automation"

# Build using PyInstaller
Write-Host "Running PyInstaller build..."
pyinstaller .\main.spec --clean -y

# Define source and destination paths
$buildOutput = Join-Path -Path "dist" -ChildPath "main"
$destination = "..\coat-ui\src-tauri\src"

# Verify build output exists
if (-Not (Test-Path $buildOutput)) {
    Write-Error "Build output not found at $buildOutput"
    exit 1
}

# Ensure destination folder exists
if (-Not (Test-Path $destination)) {
    Write-Host "Creating destination directory at $destination..."
    New-Item -Path $destination -ItemType Directory -Force | Out-Null
}

# Copy all files to coat-ui/src-tauri/src
Write-Host "Copying built files to $destination..."
Copy-Item -Path "$buildOutput\*" -Destination $destination -Recurse -Force

Write-Host "✅ Build and copy complete."
