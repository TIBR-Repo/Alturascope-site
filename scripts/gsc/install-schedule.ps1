# Registers the two Search Console reporting tasks.
#
# These are real Windows scheduled tasks, not a Claude session cron - they
# survive reboots and run whether or not anything else is open. Re-running this
# script is safe; -Force replaces the existing registrations.
#
#   powershell -ExecutionPolicy Bypass -File scripts\gsc\install-schedule.ps1

$py   = "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe"
$repo = "C:\Users\andre\alturascope-site"
$out  = "C:\Users\andre\Documents\Alturascope-SEO"

if (-not (Test-Path $py))   { throw "Python not found at $py" }
if (-not (Test-Path $repo)) { throw "Repo not found at $repo" }
New-Item -ItemType Directory -Force -Path $out | Out-Null

# StartWhenAvailable matters: if the machine was asleep at the trigger time,
# run at the next opportunity rather than silently skipping the day.
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 20)

# cmd /c wraps the call so stdout and stderr land in a log; a scheduled task
# otherwise discards both and a failure is invisible.
function New-ReportAction([string]$extraArgs) {
    New-ScheduledTaskAction -Execute "cmd.exe" -WorkingDirectory $repo `
        -Argument "/c `"`"$py`" scripts\gsc\report.py $extraArgs >> `"$out\run.log`" 2>&1`""
}

# Daily - index status only. Fast, and answers the live question: has Google
# picked up the pages from the August 2026 overhaul yet.
Register-ScheduledTask `
    -TaskName "Alturascope SEO - daily index check" `
    -Action (New-ReportAction "--quick") `
    -Trigger (New-ScheduledTaskTrigger -Daily -At 08:12) `
    -Settings $settings `
    -Description "Checks whether Google has indexed the pages from the Aug 2026 overhaul. Writes to Documents\Alturascope-SEO." `
    -Force | Out-Null

# Weekly - full performance report with week-over-week deltas and the
# before/after comparison around the deploy date.
Register-ScheduledTask `
    -TaskName "Alturascope SEO - weekly report" `
    -Action (New-ReportAction "") `
    -Trigger (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 08:23) `
    -Settings $settings `
    -Description "Full Search Console report: performance, themes, before/after the 2026-08-26 overhaul." `
    -Force | Out-Null

Get-ScheduledTask -TaskName "Alturascope SEO*" |
    Get-ScheduledTaskInfo |
    Select-Object TaskName, NextRunTime, LastTaskResult |
    Format-Table -AutoSize

Write-Host "Reports land in $out (latest.md is always the most recent)."
Write-Host "Run one now:  Start-ScheduledTask -TaskName 'Alturascope SEO - weekly report'"
Write-Host "Remove both:  Get-ScheduledTask -TaskName 'Alturascope SEO*' | Unregister-ScheduledTask -Confirm:`$false"
