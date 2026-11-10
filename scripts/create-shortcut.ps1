param(
    [switch]$AddToStartup
)

$ws = New-Object -ComObject WScript.Shell
$repoRoot = (Get-Item $PSScriptRoot).Parent.FullName

# Desktop Shortcut
$desktop = [Environment]::GetFolderPath('Desktop')
$desktopLnk = Join-Path $desktop 'pendpost.lnk'
$sc = $ws.CreateShortcut($desktopLnk)
$sc.TargetPath = Join-Path $repoRoot 'AVVIA_IN_BACKGROUND.vbs'
$sc.WorkingDirectory = $repoRoot
$sc.IconLocation = Join-Path $repoRoot 'packaging\desktop\windows\pendpost.ico'
$sc.Description = 'pendpost - Social Media Automation'
$sc.Save()
Write-Host "Collegamento creato sul Desktop: $desktopLnk"

# Startup Shortcut
if ($AddToStartup) {
    $startup = [Environment]::GetFolderPath('Startup')
    $startupLnk = Join-Path $startup 'pendpost.lnk'
    $sc2 = $ws.CreateShortcut($startupLnk)
    $sc2.TargetPath = Join-Path $repoRoot 'AVVIA_IN_BACKGROUND.vbs'
    $sc2.WorkingDirectory = $repoRoot
    $sc2.IconLocation = Join-Path $repoRoot 'packaging\desktop\windows\pendpost.ico'
    $sc2.Description = 'pendpost - Social Media Automation'
    $sc2.Save()
    Write-Host "Avvio automatico configurato in: $startupLnk"
}
