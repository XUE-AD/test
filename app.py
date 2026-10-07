"""
Streamlit 範例：銷售數據儀表板
功能：側邊欄篩選、KPI 指標卡、圖表、資料表、CSV 上傳與下載
部署：推上 GitHub 後，到 https://share.streamlit.io 連結 repo 即可
"""
import numpy as np
import pandas as pd
import streamlit as st

# ---------- 頁面設定（必須是第一個 st 指令）----------
st.set_page_config(page_title="銷售數據儀表板", page_icon="📊", layout="wide")


# ---------- 產生範例資料（cache 避免每次互動都重算）----------
@st.cache_data
def load_sample_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range("2026-01-01", "2026-09-30", freq="D")
    regions = ["台北", "台中", "高雄", "新竹"]
    products = ["筆電", "手機", "耳機", "平板"]
    n = len(dates) * 4
    df = pd.DataFrame(
        {
            "日期": rng.choice(dates, n),
            "地區": rng.choice(regions, n),
            "產品": rng.choice(products, n),
            "數量": rng.integers(1, 20, n),
            "單價": rng.choice([1500, 3200, 12000, 28000], n),
        }
    )
    df["營收"] = df["數量"] * df["單價"]
    return df.sort_values("日期").reset_index(drop=True)


# ---------- 側邊欄 ----------
st.sidebar.header("⚙️ 設定")
uploaded = st.sidebar.file_uploader("上傳自己的 CSV（選填）", type="csv")

if uploaded is not None:
    df = pd.read_csv(uploaded, parse_dates=["日期"])
    st.sidebar.success(f"已載入 {len(df)} 筆資料")
else:
    df = load_sample_data()
    st.sidebar.caption("目前使用範例資料")

regions = st.sidebar.multiselect("地區", sorted(df["地區"].unique()), default=sorted(df["地區"].unique()))
products = st.sidebar.multiselect("產品", sorted(df["產品"].unique()), default=sorted(df["產品"].unique()))

min_d, max_d = df["日期"].min().date(), df["日期"].max().date()
date_range = st.sidebar.date_input("日期區間", (min_d, max_d), min_value=min_d, max_value=max_d)

# date_input 在使用者只選一天時會回傳單一值，這裡做防呆
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range
else:
    start = end = date_range if not isinstance(date_range, tuple) else date_range[0]

# ---------- 篩選 ----------
mask = (
    df["地區"].isin(regions)
    & df["產品"].isin(products)
    & df["日期"].dt.date.between(start, end)
)
filtered = df[mask]

# ---------- 主畫面 ----------
st.title("📊 銷售數據儀表板")
st.caption("Streamlit 部署範例 — 調整左側條件，畫面會即時更新")

if filtered.empty:
    st.warning("沒有符合條件的資料，請調整篩選條件。")
    st.stop()

# KPI 指標卡
c1, c2, c3, c4 = st.columns(4)
c1.metric("總營收", f"NT$ {filtered['營收'].sum():,.0f}")
c2.metric("訂單數", f"{len(filtered):,}")
c3.metric("銷售數量", f"{filtered['數量'].sum():,}")
c4.metric("平均客單價", f"NT$ {filtered['營收'].mean():,.0f}")

st.divider()

# 分頁
tab1, tab2, tab3 = st.tabs(["📈 趨勢", "🗺️ 地區 / 產品", "📋 原始資料"])

with tab1:
    freq = st.radio("彙總單位", ["日", "週", "月"], horizontal=True, index=2)
    rule = {"日": "D", "週": "W", "月": "MS"}[freq]
    trend = filtered.set_index("日期").resample(rule)["營收"].sum()
    st.line_chart(trend, y_label="營收")

with tab2:
    left, right = st.columns(2)
    with left:
        st.subheader("各地區營收")
        st.bar_chart(filtered.groupby("地區")["營收"].sum())
    with right:
        st.subheader("各產品營收")
        st.bar_chart(filtered.groupby("產品")["營收"].sum())

    st.subheader("地區 × 產品 交叉表")
    pivot = filtered.pivot_table(index="地區", columns="產品", values="營收", aggfunc="sum", fill_value=0)
    st.dataframe(pivot.style.format("{:,.0f}"), width="stretch")

with tab3:
    st.dataframe(filtered, width="stretch", hide_index=True)
    st.download_button(
        "⬇️ 下載篩選後資料 (CSV)",
        filtered.to_csv(index=False).encode("utf-8-sig"),  # utf-8-sig 讓 Excel 開中文不亂碼
        file_name="filtered_sales.csv",
        mime="text/csv",
    )
