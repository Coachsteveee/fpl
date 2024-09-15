# Change directory to the FPL project folder
Set-Location -Path "C:\Users\NUDDY\Documents\GitHub\fpl"

# runner.ps1
$startTime = Get-Date
$logFile = "C:\Users\NUDDY\Documents\GitHub\fpl\scraper_log.txt"

# Function to run the scraper and return the output
function Run-Scraper {
    Add-Content -Path $logFile -Value "Attempting to run scraper..."
    try {
        $output = & python scraper.py 2>&1
        Add-Content -Path $logFile -Value "Scraper execution completed."
    }
    catch {
        Add-Content -Path $logFile -Value "Error running scraper: $_"
        $output = "Error: $_"
    }
    return $output
}

# Function to check if the output contains an error
function Check-Error {
    param($output)
    return $output -match "Error"
}

# Run the scraper and capture the output
$output = Run-Scraper
$endTime = Get-Date
$duration = $endTime - $startTime

# Determine the status
$status = if (Check-Error $output) { "Fail" } else { "Success" }

# Retry logic
while ($status -eq "Fail") {
    Write-Host "Scraper failed. Retrying..."
    $startTime = Get-Date
    $output = Run-Scraper
    $endTime = Get-Date
    $duration = $endTime - $startTime
    $status = if (Check-Error $output) { "Fail" } else { "Success" }
}

# Create log entry
$logEntry = @"
=====================================================================
Run Time: $startTime
Duration: $duration
End Time: $endTime
Status: $status
Output:
$output
=====================================================================

"@

# Append log entry to log file
$logFile = "C:\Users\NUDDY\Documents\GitHub\fpl\scraper_log.txt"
Add-Content -Path $logFile -Value $logEntry

# If successful, proceed with git operations
if ($status -eq "Success") {
    git pull
    git add fpl_standings.csv
    git commit -m "Update FPL standings"
    git push origin main
}

Write-Host "Scraper completed with status: $status"
Write-Host "Log appended to $logFile"