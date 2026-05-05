# ============================================================
# libraries
# ============================================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import anthropic
from dotenv import load_dotenv
import os
import json
 
load_dotenv()

# ============================================================
# Ask Claude to decide the best chart type and columns
# ============================================================
def decide_chart(df: pd.DataFrame, question: str) -> dict:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
 
    columns_info = df.dtypes.to_string()
    sample_data  = df.head(3).to_string()
 
    prompt = f"""
You have a DataFrame with these columns and types:
{columns_info}
 
Sample data:
{sample_data}
 
The user asked: "{question}"
 
Decide the best chart type and which columns to use.
 
Return ONLY a JSON object like this (no explanation, no markdown):
{{
    "chart_type": "bar",
    "x": "column_name",
    "y": "column_name",
    "title": "chart title"
}}
 
chart_type options:
- "bar"      → comparing categories
- "line"     → trends over time
- "pie"      → parts of a whole (max 8 categories)
- "scatter"  → relationship between two numbers
- "none"     → if data cannot be charted (single value or error)
"""
 
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
 
    response = message.content[0].text.strip()
 
    try:
        return json.loads(response)
    except Exception:
        return {"chart_type": "none"}
    

# ============================================================
# Generate Plotly chart from DataFrame
# ============================================================
def generate_chart(df: pd.DataFrame, question: str):
 
    # Don't chart error results
    if "error" in df.columns:
        return None
 
    # Don't chart single value results
    if df.shape == (1, 1):
        return None
 
    chart_info = decide_chart(df, question)
    chart_type = chart_info.get("chart_type", "none")
 
    if chart_type == "none":
        return None
 
    x = chart_info.get("x")
    y = chart_info.get("y")
    title = chart_info.get("title", question)
 
    try:
        if chart_type == "bar":
            fig = px.bar(df, x=x, y=y, title=title,
                         color_discrete_sequence=["#636EFA"])
 
        elif chart_type == "line":
            fig = px.line(df, x=x, y=y, title=title,
                          markers=True)
 
        elif chart_type == "pie":
            fig = px.pie(df, names=x, values=y, title=title)
 
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x, y=y, title=title)
 
        else:
            return None
 
        # Clean layout
        fig.update_layout(
            title_font_size=16,
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
 
        return fig
 
    except Exception as e:
        print(f"Chart error: {e}")
        return None
 

 
# ============================================================
# Test
# ============================================================
if __name__ == "__main__":
    from text_to_sql import ask
 
    test_questions = [
        "What are the top 5 customers by total sales?",
        "What is the total profit by category?",
        "What are the monthly sales in 2014?",
    ]
 
    for question in test_questions:
        print(f"\nQuestion: {question}")
        sql, df = ask(question)
        print(f"Result:\n{df}")
 
        fig = generate_chart(df, question)
        if fig:
            fig.show()
            print("Chart generated ✅")
        else:
            print("No chart generated")
        print("=" * 50)