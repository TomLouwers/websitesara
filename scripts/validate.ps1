param(
  [string]$ContentRoot = "content",
  [string]$Schema = "docs/new/schemas/ExerciseSchema.json",
  [string]$Taskforms = "docs/new/taskvormen-canon.json"
)

$env:PYTHONIOENCODING = "utf-8"

py -3.13 tools/new/validate_all_exercises_multidomain.py `
  --content-root $ContentRoot `
  --schema $Schema `
  --taskforms $Taskforms

exit $LASTEXITCODE
