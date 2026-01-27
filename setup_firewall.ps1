# Firewall setup script for Bank P2P Application
# Run this as Administrator on BOTH computers (Yours and your friend's)

Write-Host "Setting up Firewall rules for Bank P2P App (Port 65525)..." -ForegroundColor Cyan

$port = 65525
$ruleName = "BankP2P_Allow_65525"

# Check if rule exists
$existing = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

if ($existing) {
    Write-Host "Rule already exists. Removing old rule..." -ForegroundColor Yellow
    Remove-NetFirewallRule -DisplayName $ruleName
}

# Create new Inbound Rule
New-NetFirewallRule -DisplayName $ruleName `
                    -Direction Inbound `
                    -LocalPort $port `
                    -Protocol TCP `
                    -Action Allow `
                    -Profile Any `
                    -Description "Allows incoming connections for Bank P2P App"

Write-Host "Success! Port $port is now open." -ForegroundColor Green
Write-Host "IMPORTANT: Your friend MUST run this script too!" -ForegroundColor Red
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
