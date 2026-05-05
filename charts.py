# ============================================================
# to make charts
# ============================================================

# ============================================================
# libraries
# ============================================================
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Generate Plotly chart from DataFrame
# ============================================================
def generate_chart(df: pd.DataFrame, question: str):

    # Don't chart error results
    if "error" in df.columns:
        return None

    # Don't chart single column results
    if df.shape[1] == 1:
        return None

    # Get column types
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols    = df.select_dtypes(exclude="number").columns.tolist()

    # Need at least 1 text + 1 numeric to chart
    if not numeric_cols or not text_cols:
        return None

    x     = text_cols[0]
    y     = numeric_cols[0]
    title = question

    try:
        # Line chart if x column has date/month/year
        if any(k in x.lower() for k in ["date", "month", "year"]):
            fig = px.line(df, x=x, y=y, title=title, markers=True)
        # Pie chart if 3 or fewer categories
        elif df[x].nunique() <= 3:
            fig = px.pie(df, names=x, values=y, title=title)
        # Bar chart for everything else
        else:
            fig = px.bar(df, x=x, y=y, title=title,
                         color_discrete_sequence=["#636EFA"])

        fig.update_layout(
            title_font_size=16,
            title_font_color="black",
            xaxis_tickangle=-45,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                tickfont=dict(color="black"),
                title=dict(font=dict(color="black"))
            ),
            yaxis=dict(
                tickfont=dict(color="black"),
                title=dict(font=dict(color="black"))
            ),
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
            print("Chart generated successfully")
        else:
            print("No chart generated")
        print("=" * 50)