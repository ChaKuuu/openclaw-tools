# Get A-share market data for analysis

# Major indices
$indices = Invoke-RestMethod -Uri 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f1,f2,f3,f4,f12,f13,f104,f105,f106&secids=1.000001,0.399001,0.399006,0.000300' -TimeoutSec 10

Write-Host "=== 大盘指数 ==="
$indices.data.diff | ForEach-Object { 
    $name = switch($_.f12) {
        "000001" { "上证指数" }
        "399001" { "深证成指" }
        "399006" { "创业板指" }
        "000300" { "沪深300" }
        default { $_.f13 }
    }
    $price = $_.f2
    $change = $_.f3
    Write-Host "$name : $price ($change%)"
}
