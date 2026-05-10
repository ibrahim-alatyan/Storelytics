# 📊 Storelytics

> An AI-powered conversational analytics tool that lets you query retail data using plain English or Arabic — with automatic chart generation and voice input support.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Text-to-SQL** | Ask questions in natural language; Claude converts them to SQL automatically |
| 🌍 **Bilingual** | Supports both **English** and **Arabic** queries |
| 🎤 **Voice Input** | Record your question and get it transcribed via Groq Whisper |
| 📊 **Auto Charts** | Results are visualized automatically with Plotly (bar, line, pie) |
| 💬 **Chat History** | Full conversation memory within the session |
| 🗄️ **SQLite Backend** | Normalized 3-table database (customers, products, orders) |

---

## 🏗️ Architecture

```
User Question (text / voice)
        │
        ▼
┌───────────────────┐
│   Streamlit UI    │  ◄──  app.py
└────────┬──────────┘
         │
   ┌─────┴──────┐
   │            │
   ▼            ▼
src/voice.py    src/text_to_sql.py
(Groq            (Claude Sonnet
 Whisper)         → SQL → SQLite)
                      │
                      ▼
                 src/charts.py
               (Plotly charts)
```

---

## 📁 Project Structure

```
storelytics/
├── app.py                    # Main Streamlit application
├── src/
│   ├── text_to_sql.py        # LLM → SQL → DataFrame pipeline
│   ├── charts.py             # Automatic chart generation
│   ├── voice.py              # Audio transcription via Groq
│   └── cleaning.py           # Data cleaning & SQLite setup
├── data/
│   ├── Global_Superstore2.csv
│   └── Global_Superstore2.xlsx
├── superstore.db             # SQLite database (auto-generated)
├── .env                      # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🗄️ Database Schema

The raw CSV is cleaned and normalized into **3 tables**:

### `customers`
| Column | Type | Description |
|---|---|---|
| customer_id | TEXT | Primary key |
| customer_name | TEXT | Full name |
| segment | TEXT | Consumer / Corporate / Home Office |
| city, state, country | TEXT | Location |
| market | TEXT | US / EU / APAC / LATAM / EMEA / Africa / Canada |
| region | TEXT | Geographic region |

### `products`
| Column | Type | Description |
|---|---|---|
| product_id | TEXT | Primary key |
| product_name | TEXT | Full product name |
| category | TEXT | Technology / Furniture / Office Supplies |
| sub_category | TEXT | Detailed category |

### `orders`
| Column | Type | Description |
|---|---|---|
| order_id | TEXT | Order identifier |
| customer_id | TEXT | FK → customers |
| product_id | TEXT | FK → products |
| order_date / ship_date | DATE | Timeline |
| ship_mode | TEXT | First Class / Second Class / Standard Class / Same Day |
| order_priority | TEXT | Critical / High / Medium / Low |
| sales, profit | REAL | Financial metrics |
| quantity, discount, shipping_cost | REAL | Order details |
| order_year | INTEGER | Extracted from order_date |
| order_month | INTEGER | Extracted from order_date (1–12) |

> **Note:** `order_year` and `order_month` are extracted from `order_date` for easier time-based filtering.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/storelytics.git
cd storelytics
```

### 2. Install dependencies

```bash
pip install streamlit anthropic groq pandas plotly python-dotenv
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 📥 Download the dataset

Download `Global_Superstore2.csv` from Kaggle:
[Global Super Store Dataset](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset/code)

Place it inside the `data/` folder before continuing.

### 4. Prepare the database

```bash
python src/cleaning.py
```

This reads `data/Global_Superstore2.csv`, cleans the data, and generates `superstore.db` in the root directory.

### 5. Run the app

```bash
streamlit run app.py
```

---

## 🔑 API Keys Required

| Service | Used For | Get it at |
|---|---|---|
| [Anthropic](https://console.anthropic.com) | Text-to-SQL generation | console.anthropic.com |
| [Groq](https://console.groq.com) | Voice transcription (Whisper) | console.groq.com |

---

## 💡 Example Questions

```
What are the top 5 customers by total sales?
Which product category has the highest profit margin?
Show me monthly sales trend for 2014
ما هي المنتجات الأكثر مبيعاً؟
ما هو إجمالي الأرباح حسب الفئة؟
```

---

## 📦 Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | Web UI |
| Claude Sonnet | Text-to-SQL |
| Groq Whisper | Voice transcription |
| Plotly | Charts |
| SQLite | Database |
| Pandas | Data processing |

---

Made by Ibrahim Alatyan
