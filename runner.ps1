# runner.ps1
$startTime = Get-Date

# Function to run the scraper and return the output
function Run-Scraper {
    $output = & python scraper.py 2>&1
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
====================
Run Time: $startTime
Duration: $duration
Status: $status
Output:
$output
====================

"@

# Append log entry to log file
$logFile = "scraper_log.txt"
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
