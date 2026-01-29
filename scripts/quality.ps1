param(
  [string]$ContentRoot = "content"
)

$env:PYTHONIOENCODING = "utf-8"

py -3.13 tools/new/quality_pack_checks.py --content-root $ContentRoot
exit $LASTEXITCODE
