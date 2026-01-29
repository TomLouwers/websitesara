param(
  [string]$ContentRoot = "content",
  [string]$Schema = "docs/new/schemas/ExerciseSchema.json",
  [string]$Taskforms = "docs/new/taskvormen-canon.json",
  [string]$Baseline = "docs/new/duplicate_baseline.json",
  [string]$Overrides = "docs/new/duplicate_gate_overrides.json"
)

$env:PYTHONIOENCODING = "utf-8"

Write-Host "== VALIDATE =="
py -3.13 tools/new/validate_all_exercises_multidomain.py `
  --content-root $ContentRoot `
  --schema $Schema `
  --taskforms $Taskforms
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`n== QUALITY (warnings only) =="
py -3.13 tools/new/quality_pack_checks.py --content-root $ContentRoot
# quality script is warnings-only, do not fail pipeline on it

Write-Host "`n== HARD DUPLICATE GATE =="

$gateOut = py -3.13 tools/new/hard_duplicate_gate.py `
  --content-root $ContentRoot `
  --baseline $Baseline `
  --overrides $Overrides

$gateOut | ForEach-Object { Write-Host $_ }

# Pak breakdown-regel (als die er is)
$breakdown = $gateOut | Select-String -Pattern "Breakdown:" | Select-Object -First 1
if ($breakdown) {
  Write-Host "`n== HARD GATE SUMMARY =="
  Write-Host $breakdown.Line
}

exit $LASTEXITCODE