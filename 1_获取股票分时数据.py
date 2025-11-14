import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import csv
# 设置股票代码
stock_code = "000001"


def get_historical_minute_data(stock_code, period='60', adjust=''):
    """
    获取历史分钟数据（支持更长周期）
    period: '1', '5', '15', '30', '60' 分钟
    adjust: 复权类型，默认为空
    """
    try:
        # 使用不同的接口
        df = ak.stock_zh_a_hist_min_em(symbol=stock_code, period=period, adjust=adjust)

        print(f"获取到 {len(df)} 条{period}分钟数据")
        print("数据列:", df.columns.tolist())

        return df

    except Exception as e:
        print(f"获取数据时出错: {e}")
        return pd.DataFrame()


# 获取不同周期的数据
print("=== 1分钟数据 ===")
minute_1_data = get_historical_minute_data(stock_code, '1')

print("\n=== 5分钟数据 ===")
minute_5_data = get_historical_minute_data(stock_code, '5')

print("\n=== 15分钟数据 ===")
minute_15_data = get_historical_minute_data(stock_code, '15')

minute_30_data = get_historical_minute_data(stock_code, '30')


