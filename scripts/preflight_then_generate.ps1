param(
  [Parameter(Mandatory=$true)]
  [string]$PromptFile
)

.\scripts\preflight.ps1 -PromptFile $PromptFile
if ($LASTEXITCODE -ne 0) {
  Write-Host "❌ Preflight failed. Fix prompt first."
  exit $LASTEXITCODE
}

Write-Host "✅ Preflight OK. (Hook your generator here)"
exit 0
