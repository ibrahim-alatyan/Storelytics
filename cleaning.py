# ============================================================
# Cleaning the data for the project
# ============================================================

# ============================================================
# libraries
# ============================================================
import pandas as pd
import sqlite3

# ============================================================
# read the data
# ============================================================
df = pd.read_csv('Global_Superstore2.csv', encoding="latin1")

# ============================================================
# explore the data
# ============================================================
print("\nhead:\n"+ str(df.head()))
print("\ninfo:\n"+ str(df.info()))
print("\ndescribe:\n"+ str(df.describe()))
print("\nisnull:\n"+ str(df.isnull().sum()))
print(f"\nOriginal shape: {df.shape[0]:,} rows x {df.shape[1]} columns")

# ============================================================
# drop Postal Code (have 41296 missing values- no analytical value)
# ============================================================
df.drop(columns=['Postal Code'], inplace=True)
print("dropped Postal Code column")

# ============================================================
# convert dates from string to datetime
# ============================================================
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="%d-%m-%Y")

# ============================================================
# extract year and month
# ============================================================
df["Order Year"]  = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month

# ============================================================
# Normalization - split into 3 tables
# ============================================================
print("\nNormalizing into 3 tables...")
 
# === Customers table ===
customers = df[[
    "Customer ID", "Customer Name", "Segment",
    "City", "State", "Country", "Market", "Region"
]].drop_duplicates(subset=["Customer ID"]).copy()
 
customers.columns = [
    "customer_id", "customer_name", "segment",
    "city", "state", "country", "market", "region"
]
customers.reset_index(drop=True, inplace=True)
print(f"customers: {len(customers):,} unique customers")


# === Products table ===
products = df[[
    "Product ID", "Product Name", "Category", "Sub-Category"
]].drop_duplicates(subset=["Product ID"]).copy()
 
products.columns = ["product_id", "product_name", "category", "sub_category"]
products.reset_index(drop=True, inplace=True)
print(f"products: {len(products):,} unique products")
 

# === Orders table ===
orders = df[[
    "Order ID", "Row ID", "Customer ID", "Product ID",
    "Order Date", "Ship Date", "Ship Mode", "Order Priority",
    "Sales", "Quantity", "Discount", "Profit", "Shipping Cost",
    "Order Year", "Order Month"
]].copy()

orders.columns = [
    "order_id", "row_id", "customer_id", "product_id",
    "order_date", "ship_date", "ship_mode", "order_priority",
    "sales", "quantity", "discount", "profit", "shipping_cost",
    "order_year", "order_month"
]
print(f"orders: {len(orders):,} orders")

# ============================================================
# Save to SQLite
# ============================================================
db_path = "superstore.db"
print("Successfully created database")
conn = sqlite3.connect(db_path)
 
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products",   conn, if_exists="replace", index=False)
orders.to_sql("orders",       conn, if_exists="replace", index=False)

conn.close()
print(f"Saved to {db_path}")