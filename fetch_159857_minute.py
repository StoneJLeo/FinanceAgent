import os
import sys
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(df.columns)
    dt_col = None
    for c in ("datetime", "time", "date", "day", "时间", "交易时间"):
        if c in cols:
            dt_col = c
            break
    if dt_col is None:
        for c in cols:
            if "time" in c or "date" in c:
                dt_col = c
                break
    if dt_col is None:
        raise RuntimeError("no datetime column")
    if not pd.api.types.is_datetime64_any_dtype(df[dt_col]):
        df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce")
    price_col = None
    for c in ("close", "收盘", "Close", "c"):
        if c in cols:
            price_col = c
            break
    if price_col is None:
        raise RuntimeError("no close column")
    out = df[[dt_col, price_col]].rename(columns={dt_col: "datetime", price_col: "close"}).dropna()
    return out

def _filter_today(df: pd.DataFrame) -> pd.DataFrame:
    t = date.today()
    return df[df["datetime"].dt.date == t]

def fetch_akshare(code: str) -> pd.DataFrame:
    import akshare as ak
    df = None
    try:
        df = ak.fund_etf_minute_sina(symbol=code)
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df
    except Exception:
        df = None
    try:
        df = ak.stock_zh_a_minute(symbol="sz" + code, period="1", adjust="")
        if isinstance(df, pd.DataFrame) and not df.empty:
            return df
    except Exception:
        df = None
    return pd.DataFrame()

def main():
    code = "159857"
    df_raw = fetch_akshare(code)
    if df_raw is None or df_raw.empty:
        print("fetch failed")
        sys.exit(2)
    df = _normalize(df_raw)
    today_df = _filter_today(df)
    if today_df.empty:
        today_df = df
    today_df = today_df.sort_values("datetime")
    fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
    ax.plot(today_df["datetime"], today_df["close"], color="#4cc9f0")
    ax.set_title("159857 今日分时")
    ax.set_xlabel("时间")
    ax.set_ylabel("价格")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    out_path = os.path.join(os.getcwd(), "159857_today.png")
    fig.savefig(out_path, bbox_inches="tight")
    print(out_path)

if __name__ == "__main__":
    main()