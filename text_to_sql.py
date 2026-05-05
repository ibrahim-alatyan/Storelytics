# ============================================================
# libraries
# ============================================================
import sqlite3
import pandas as pd
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

# ============================================================
# Database schema - tells Claude what tables and columns exist
# ============================================================
DB_SCHEMA = """
You have access to a SQLite database with 3 tables:
 
TABLE: customers
- customer_id    (text)   primary key
- customer_name  (text)
- segment        (text)   values: Consumer, Corporate, Home Office
- city           (text)
- state          (text)
- country        (text)
- market         (text)   values: US, EU, APAC, LATAM, EMEA, Africa, Canada
- region         (text)
 
TABLE: products
- product_id     (text)   primary key
- product_name   (text)
- category       (text)   values: Technology, Furniture, Office Supplies
- sub_category   (text)
 
TABLE: orders
- order_id       (text)
- row_id         (integer)
- customer_id    (text)   foreign key -> customers.customer_id
- product_id     (text)   foreign key -> products.product_id
- order_date     (date)
- ship_date      (date)
- ship_mode      (text)   values: First Class, Second Class, Standard Class, Same Day
- order_priority (text)   values: Critical, High, Medium, Low
- sales          (real)
- quantity       (integer)
- discount       (real)
- profit         (real)
- shipping_cost  (real)
"""
 
# ============================================================
# Connect to database
# ============================================================
def get_connection():
    return sqlite3.connect("superstore.db")
 
# ============================================================
# Ask Claude to write SQL for the question
# ============================================================
def generate_sql(question: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
 
    prompt = f"""
{DB_SCHEMA}
 
Write a SQLite SQL query to answer this question:
{question}
 
Rules:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Always use table aliases (o for orders, c for customers, p for products)
- Use JOIN when data from multiple tables is needed
"""
 
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
 
    return message.content[0].text.strip()
 
# ============================================================
# Run the SQL on the database
# ============================================================
def run_sql(sql: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})
    finally:
        conn.close()

# ============================================================
# Main function - takes question, returns result
# ============================================================
def ask(question: str) -> tuple[str, pd.DataFrame]:
    sql = generate_sql(question)
    result = run_sql(sql)
    return sql, result
 


# ============================================================
# Test
# ============================================================
if __name__ == "__main__":
    test_questions = [
        "What are the top 5 customers by total sales?",
        "Which product category has the highest profit?",
        "How many orders were placed in 2014?",
    ]
 
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        sql, result = ask(question)
        print(f"SQL:\n{sql}")
        print(f"\nResult:\n{result}")
        print("=" * 50)