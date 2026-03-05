# Python 股票查询示例
import requests

def get_stock(code):
    """获取股票数据"""
    url = f"https://api.example.com/stock/{code}"
    # 这里可以使用实际的股票 API
    return {"code": code, "price": "TBD"}

if __name__ == "__main__":
    stock = get_stock("600519")  # 茅台
    print(f"股票: {stock['code']}, 价格: {stock['price']}")
