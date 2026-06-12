<#
Prepare IR Support packages for a PyPI release.

Run from the ir_support repository root, or call this file directly:

    .\tools\prepare_pypi_release.ps1

The script updates package versions, refreshes the root Poetry lock file, runs
optional tests, and builds all four distributions. It does not upload anything
to PyPI; upload/release is still a separate deliberate step.
#>

[CmdletBinding()]
param(
    [string]$Python = "C:\robotics_41013_Python\.venv\Scripts\python.exe",
    [switch]$SkipTests,
    [switch]$SkipBuild
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PackageFiles = [ordered]@{
    Core = Join-Path $RepoRoot "pyproject.toml"
    ExtraRobots = Join-Path $RepoRoot "ir_support_extra_robots\pyproject.toml"
    ExtraParts = Join-Path $RepoRoot "ir_support_extra_parts\pyproject.toml"
    Full = Join-Path $RepoRoot "ir_support_full\pyproject.toml"
}

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory)] [string]$WorkingDirectory,
        [Parameter(Mandatory)] [string]$FilePath,
        [Parameter(ValueFromRemainingArguments)] [string[]]$Arguments
    )

    Push-Location $WorkingDirectory
    try {
        Write-Host "`n> $FilePath $($Arguments -join ' ')" -ForegroundColor Cyan
        & $FilePath @Arguments
        if ($LASTEXITCODE -ne 0) {
            throw "Command failed with exit code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
    }
}

function Get-PoetryVersion {
    param([Parameter(Mandatory)] [string]$Path)

    $text = Get-Content -LiteralPath $Path -Raw
    $match = [regex]::Match($text, '(?m)^version\s*=\s*"(?<version>[^"]+)"')
    if (-not $match.Success) {
        throw "Could not find [tool.poetry] version in $Path"
    }
    return $match.Groups['version'].Value
}

function Set-PoetryVersion {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [string]$Version
    )

    $text = Get-Content -LiteralPath $Path -Raw
    $text = [regex]::Replace($text, '(?m)^version\s*=\s*"[^"]+"', "version = `"$Version`"", 1)
    Set-Content -LiteralPath $Path -Value $text -Encoding UTF8
}

function Set-DependencyConstraint {
    param(
        [Parameter(Mandatory)] [string]$Path,
        [Parameter(Mandatory)] [string]$DependencyName,
        [Parameter(Mandatory)] [string]$Constraint
    )

    $escapedName = [regex]::Escape($DependencyName)
    $pattern = '(?m)^' + $escapedName + '\s*=\s*"[^"]+"'
    $replacement = $DependencyName + ' = "' + $Constraint + '"'
    $text = Get-Content -LiteralPath $Path -Raw
    if ($text -notmatch $pattern) {
        throw "Could not find dependency '$DependencyName' in $Path"
    }
    $text = [regex]::Replace($text, $pattern, $replacement, 1)
    Set-Content -LiteralPath $Path -Value $text -Encoding UTF8
}

function Read-VersionWithDefault {
    param(
        [Parameter(Mandatory)] [string]$PackageName,
        [Parameter(Mandatory)] [string]$DefaultVersion
    )

    while ($true) {
        $value = Read-Host "$PackageName version [$DefaultVersion]"
        if ([string]::IsNullOrWhiteSpace($value)) {
            $value = $DefaultVersion
        }
        if ($value -match '^\d+\.\d+\.\d+([A-Za-z0-9\.\-\+]+)?$') {
            return $value
        }
        Write-Warning "Please enter a version like 1.3.1 or 0.2.0."
    }
}

function Get-NextMajorUpperBound {
    param([Parameter(Mandatory)] [string]$Version)
    $parts = $Version.Split('.')
    return "$(1 + [int]$parts[0]).0.0"
}

function Get-NextMinorUpperBound {
    param([Parameter(Mandatory)] [string]$Version)
    $parts = $Version.Split('.')
    return "$($parts[0]).$([int]$parts[1] + 1).0"
}

function Ensure-PythonModule {
    param(
        [Parameter(Mandatory)] [string]$ModuleName,
        [Parameter(Mandatory)] [string]$InstallSpec
    )

    & $Python -m $ModuleName --version *> $null
    if ($LASTEXITCODE -eq 0) {
        return
    }

    $answer = Read-Host "Python module '$ModuleName' is not available. Install '$InstallSpec' into $Python now? [y/N]"
    if ($answer -notmatch '^(y|yes)$') {
        throw "Missing required Python module '$ModuleName'."
    }
    Invoke-CheckedCommand -WorkingDirectory $RepoRoot -FilePath $Python -Arguments @('-m', 'pip', 'install', $InstallSpec)
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python executable not found: $Python"
}

Write-Host "IR Support PyPI release preparation" -ForegroundColor Green
Write-Host "Repository: $RepoRoot"
Write-Host "Python:    $Python"

$currentCore = Get-PoetryVersion $PackageFiles.Core
$currentExtraRobots = Get-PoetryVersion $PackageFiles.ExtraRobots
$currentExtraParts = Get-PoetryVersion $PackageFiles.ExtraParts
$currentFull = Get-PoetryVersion $PackageFiles.Full

Write-Host "`nCurrent versions in pyproject files:" -ForegroundColor Green
Write-Host "  ir-support:              $currentCore"
Write-Host "  ir-support-extra-robots: $currentExtraRobots"
Write-Host "  ir-support-extra-parts:  $currentExtraParts"
Write-Host "  ir-support-full:         $currentFull"
Write-Host "`nPress Enter to keep a current value, or type a new release version."

$coreVersion = Read-VersionWithDefault "ir-support" $currentCore
$extraRobotsVersion = Read-VersionWithDefault "ir-support-extra-robots" $currentExtraRobots
$extraPartsVersion = Read-VersionWithDefault "ir-support-extra-parts" $currentExtraParts
$fullVersion = Read-VersionWithDefault "ir-support-full" $currentFull

$coreConstraint = ">=$coreVersion,<$(Get-NextMajorUpperBound $coreVersion)"
$extraRobotsConstraint = ">=$extraRobotsVersion,<$(Get-NextMinorUpperBound $extraRobotsVersion)"
$extraPartsConstraint = ">=$extraPartsVersion,<$(Get-NextMinorUpperBound $extraPartsVersion)"

Write-Host "`nWill prepare these release versions:" -ForegroundColor Green
Write-Host "  ir-support:              $coreVersion"
Write-Host "  ir-support-extra-robots: $extraRobotsVersion  (depends on ir-support $coreConstraint)"
Write-Host "  ir-support-extra-parts:  $extraPartsVersion   (depends on ir-support $coreConstraint)"
Write-Host "  ir-support-full:         $fullVersion         (depends on extras $extraRobotsConstraint and $extraPartsConstraint)"

$confirm = Read-Host "Continue and update files/build packages? [y/N]"
if ($confirm -notmatch '^(y|yes)$') {
    Write-Host "Cancelled."
    exit 0
}

Set-PoetryVersion $PackageFiles.Core $coreVersion
Set-PoetryVersion $PackageFiles.ExtraRobots $extraRobotsVersion
Set-PoetryVersion $PackageFiles.ExtraParts $extraPartsVersion
Set-PoetryVersion $PackageFiles.Full $fullVersion

Set-DependencyConstraint $PackageFiles.ExtraRobots 'ir-support' $coreConstraint
Set-DependencyConstraint $PackageFiles.ExtraParts 'ir-support' $coreConstraint
Set-DependencyConstraint $PackageFiles.Full 'ir-support' $coreConstraint
Set-DependencyConstraint $PackageFiles.Full 'ir-support-extra-robots' $extraRobotsConstraint
Set-DependencyConstraint $PackageFiles.Full 'ir-support-extra-parts' $extraPartsConstraint

Ensure-PythonModule -ModuleName 'poetry' -InstallSpec 'poetry==2.1.3'
if (-not $SkipBuild) {
    Ensure-PythonModule -ModuleName 'build' -InstallSpec 'build'
}

Write-Host "`nRefreshing root Poetry lock file..." -ForegroundColor Green
Invoke-CheckedCommand -WorkingDirectory $RepoRoot -FilePath $Python -Arguments @('-m', 'poetry', 'lock')

if (-not $SkipTests) {
    Write-Host "`nRunning tests..." -ForegroundColor Green
    Invoke-CheckedCommand -WorkingDirectory $RepoRoot -FilePath $Python -Arguments @('-m', 'pytest')
}

if (-not $SkipBuild) {
    Write-Host "`nCleaning old dist folders..." -ForegroundColor Green
    foreach ($distPath in @(
        (Join-Path $RepoRoot 'dist'),
        (Join-Path $RepoRoot 'ir_support_extra_robots\dist'),
        (Join-Path $RepoRoot 'ir_support_extra_parts\dist'),
        (Join-Path $RepoRoot 'ir_support_full\dist')
    )) {
        if (Test-Path -LiteralPath $distPath) {
            Remove-Item -LiteralPath $distPath -Recurse -Force
        }
    }

    Write-Host "`nBuilding packages..." -ForegroundColor Green
    Invoke-CheckedCommand -WorkingDirectory $RepoRoot -FilePath $Python -Arguments @('-m', 'poetry', 'build')
    Invoke-CheckedCommand -WorkingDirectory $RepoRoot -FilePath $Python -Arguments @('-m', 'build', '.\ir_support_extra_robots')
    Invoke-CheckedCommand -WorkingDirectory $RepoRoot -FilePath $Python -Arguments @('-m', 'build', '.\ir_support_extra_parts')
    Invoke-CheckedCommand -WorkingDirectory $RepoRoot -FilePath $Python -Arguments @('-m', 'build', '.\ir_support_full')
}

Write-Host "`nRelease preparation complete." -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  1. Review: git diff"
Write-Host "  2. Commit and PR these version/build-prep changes into master."
Write-Host "  3. After merge, run the GitHub 'Release to PyPI' workflow from master."
Write-Host "     The workflow publishes ir-support, ir-support-extra-robots, ir-support-extra-parts, and ir-support-full."
Write-Host "  4. Confirm the GitHub secret PYPI_API_TOKEN can upload all four PyPI projects."

