# OpenClaw AI Tools Package

## 安装
```bash
pip install openclaw-ai-tools
```

## 使用
```python
from openclaw import stock, weather, news

# 股票分析
result = stock.analyze("600519")

# 天气查询
w = weather.get("北京")

# 新闻分析
n = news.analyze("今天股市大涨！")
```

## 功能
- 股票分析
- 天气查询
- 新闻情感分析
