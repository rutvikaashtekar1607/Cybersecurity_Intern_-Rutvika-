Write-Host "[*] Starting CyberOS Firewall Engine Test Suite..." -ForegroundColor Cyan
cd ../src
python cli.py
Write-Host "[*] Running Unit Tests..." -ForegroundColor Cyan
cd ../tests
python test_analyzer.py
Write-Host "[+] All automated checks completed successfully!" -ForegroundColor Green