# Gives your account access to the 14 scratch folders in smc_hedge that the Codex
# sandbox account created and locked. cleanup_smc_hedge.py could not move them.
#
# Run from an elevated ("Run as administrator") PowerShell:
#
#   powershell -ExecutionPolicy Bypass -File C:\dev\projects\smc_research\tools\unlock_sandbox_folders.ps1
#
# It takes ownership of each folder and grants full control to -Account.
# It moves and deletes nothing. Afterwards, rerun cleanup_smc_hedge.py --apply
# from a normal terminal.
param(
    [string]$Repo = 'C:\dev\projects\smc_hedge',
    [string]$Account = 'aldoc'
)

$folders = @(
    'research\2026-10_alpha_w5_persistence_v1\fault_audit\temp_retry1',
    'research\2026-10_alpha_w5_pilot_v1\engineering\temp',
    'research\2026-10_alpha_w5_validation_v1\engineering\temp',
    'research\2026-10_alpha_w6_development_v1\checks\final_unit_tmp',
    'research\2026-10_alpha_w6_development_v1\checks\unit_tmp_02',
    'research\2026-10_alpha_w6_development_v1\checks\unit_tmp_03',
    'research\2026-10_alpha_w6_parallel_engineering_v1\tests_tmp_02',
    'research\2026-10_alpha_w6_variance_pilot_v1\checks\unit_temp_01',
    'research\2026-10_alpha_w6_variance_pilot_v1\checks\unit_temp_02',
    'research\2026-10_alpha_w6_variance_pilot_v1\checks\unit_temp_03',
    'research\2026-10_alpha_w6_verification_v1\checks\unit_temp_01',
    'research\2026-10_alpha_w6_verification_v1\checks\unit_temp_02',
    'research\2026-10_alpha_w6_verification_v1\checks\unit_temp_03',
    'research\2026-10_alpha_w6_verification_v1\checks\unit_temp_final'
)

$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$isAdmin = ([Security.Principal.WindowsPrincipal]$identity).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host 'This must be run from an elevated PowerShell (Run as administrator).'
    exit 1
}

$failed = 0
foreach ($rel in $folders) {
    $path = Join-Path $Repo $rel
    if (-not (Test-Path -LiteralPath $path)) {
        Write-Host "absent, skipped:  $rel"
        continue
    }
    takeown /f $path /r /d y | Out-Null
    icacls $path /grant "${Account}:(OI)(CI)F" /t /c /q | Out-Null
    try {
        $items = @(Get-ChildItem -LiteralPath $path -Recurse -Force -ErrorAction Stop)
        $bytes = ($items | Where-Object { -not $_.PSIsContainer } | Measure-Object Length -Sum).Sum
        Write-Host ("unlocked:  {0}   ({1} items, {2:N0} bytes)" -f $rel, $items.Count, [int64]$bytes)
    } catch {
        $failed++
        Write-Host "STILL LOCKED:  $rel   $($_.Exception.Message)"
    }
}

if ($failed) {
    Write-Host "`n$failed folder(s) are still locked."
    exit 1
}
Write-Host "`nAll folders are readable. Rerun cleanup_smc_hedge.py --apply from a normal terminal."
