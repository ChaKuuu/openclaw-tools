$content = Get-Content 'C:\Users\WUccc\.openclaw\openclaw.json' -Raw
$content = $content -replace '"main":', '"default":'
Set-Content -Path 'C:\Users\WUccc\.openclaw\openclaw.json' -Value $content -NoNewline
