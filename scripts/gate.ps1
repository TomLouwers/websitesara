param(
  [string]$ContentRoot = "content",
  [string]$Baseline = "docs/new/duplicate_baseline.json",
  [string]$Overrides = "docs/new/duplicate_gate_overrides.json"
)

$env:PYTHONIOENCODING = "utf-8"

py -3.13 tools/new/hard_duplicate_gate.py `
  --content-root $ContentRoot `
  --baseline $Baseline `
  --overrides $Overrides

exit $LASTEXITCODE
