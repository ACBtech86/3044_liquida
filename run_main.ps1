# PowerShell script to run the main Python project

# Activate .venv if it exists
if (Test-Path ".venv") {
    Write-Host "Activating .venv..."
    $venvActivate = ".venv\Scripts\Activate.ps1"
    if (Test-Path $venvActivate) {
        & $venvActivate
        $python = "python"
    } else {
        Write-Host "Could not find .venv activation script."
        $python = "python"
    }
} else {
    Write-Host ".venv not found, using system Python."
    $python = "python"
}

$script = "main.py"

# Check if requirements.txt exists and install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    & $python -m pip install -r requirements.txt
}

# Run the main script
Write-Host "Running main.py..."
& $python $script
