# PowerShell script to run the main Python project
$python = "python"
$script = "main.py"

# Check if requirements.txt exists and install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    & $python -m pip install -r requirements.txt
}

# Run the main script
Write-Host "Running main.py..."
& $python $script
