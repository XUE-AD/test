# 銷售數據儀表板（Streamlit 範例）

## 專案結構

```
your-repo/
├── app.py             # 主程式
├── requirements.txt   # 套件清單（雲端部署時自動安裝）
├── .gitignore
└── README.md
```

## 本機執行

```bash
pip install -r requirements.txt
streamlit run app.py
```

瀏覽器會自動開啟 http://localhost:8501

## 部署到 Streamlit Community Cloud（免費）

### 1. 推上 GitHub

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/<你的帳號>/<repo名稱>.git
git push -u origin main
```

> repo 設為 Public 最簡單；Private 也可以，但授權時要允許 Streamlit 讀取私有 repo。

### 2. 在 Streamlit Cloud 建立 App

1. 前往 https://share.streamlit.io ，用 GitHub 帳號登入
2. 點 **Create app** → **Deploy a public app from GitHub**
3. 填入：
   - Repository：`<你的帳號>/<repo名稱>`
   - Branch：`main`
   - Main file path：`app.py`
   - App URL：自訂網址（選填）
4. 點 **Deploy**，等 1–3 分鐘安裝套件後就上線了

### 3. 之後更新

只要 `git push` 到 main，雲端會自動重新部署。

## 常見問題

| 狀況 | 原因 / 解法 |
|---|---|
| `ModuleNotFoundError` | `requirements.txt` 漏寫套件，補上後 push |
| 需要 API Key 等機密 | **不要寫進程式碼或 push 上 GitHub**。在 App 設定 → Secrets 填入，程式用 `st.secrets["KEY"]` 讀取；本機則放 `.streamlit/secrets.toml`（已列入 .gitignore） |
| App 一段時間沒人用就休眠 | 免費方案的正常行為，開啟網址點「wake up」即可 |
| 指定 Python 版本 | 在 Deploy 畫面的 Advanced settings 選擇 |

## 自訂 CSV 格式

上傳的 CSV 需包含欄位：`日期, 地區, 產品, 數量, 單價, 營收`
