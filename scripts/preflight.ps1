param(
  [Parameter(Mandatory=$true)]
  [string]$PromptFile
)

$env:PYTHONIOENCODING = "utf-8"

if (!(Test-Path $PromptFile)) {
  Write-Host "❌ Prompt file not found: $PromptFile"
  exit 2
}

py -3.13 tools/new/preflight_prompt_checks.py --prompt-file $PromptFile
exit $LASTEXITCODE
