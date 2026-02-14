import pandas as pd
df = pd.read_csv("Expense_data.csv")
data = df[["Date", "Category", "Note", "Amount", "Income/Expense"]]
print(data.head())

def add_expense(date, category, note, amount, exp_type="Expense"):
    global data
    new_entry = {
        "Date": date,
        "Category": category,
        "Note": note,
        "Amount": amount,
        "Income/Expense": exp_type
    }
    data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
    print(f" Added: {note} - {amount} ({category})")

add_expense("2025-08-22 19:30", "Food", "Shawarma", 2500, "Expense")
add_expense("2025-08-23 08:00", "Subscriptions", "Netflix Monthly Plan", 4500, "Expense")
add_expense("2025-08-24 14:00", "Entertainment", "Outdoor Games with friends", 7000, "Expense")

def view_expenses(n=5):
    return data.tail(n)
print(view_expenses(5))

def summarize_expenses(by="Category"):
    summary = data[data["Income/Expense"]=="Expense"].groupby(by)["Amount"].sum()
    return summary.sort_values(ascending=False)
print(summarize_expenses())

import os

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

# Load local .env (if present) so OPENAI_API_KEY can be set from a project file.
if load_dotenv:
    load_dotenv()

# OpenAI client: use environment variable `OPENAI_API_KEY` and fail gracefully if unavailable.
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

api_key = os.getenv("OPENAI_API_KEY")
if OpenAI is None:
    client = None
    print("OpenAI SDK not installed; skipping auto-categorization.")
elif not api_key:
    client = None
    print("OPENAI_API_KEY not set; skipping auto-categorization.")
else:
    client = OpenAI(api_key=api_key)

def auto_categorize(note):
    prompt = f"""
    Categorize this expense note into one of these categories: 
    Food, Transportation, Entertainment, Other.
    Note: {note}
    """
    if client is None:
        return "Other"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Other"

data['Category'] = data.apply(
    lambda row: auto_categorize(row['Note']) if pd.isna(row['Category']) else row['Category'],
    axis=1
)

print(data[['Note', 'Category']].head(10))

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None
    print("matplotlib not installed; skipping plots.")

expense_summary = (
    data[data['Category'] != 'Income']
    .groupby("Category")["Amount"].sum()
    .sort_values(ascending=False)
)

if plt is not None:
    # Pie Chart
    plt.figure(figsize=(6,6))
    expense_summary.plot.pie(autopct='%1.1f%%', startangle=90, shadow=True)
    plt.title("Expenses Breakdown by Category")
    plt.ylabel("")
    plt.savefig("expense_pie.png", bbox_inches='tight')
    plt.show()

    # Bar Chart
    plt.figure(figsize=(8,5))
    expense_summary.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.savefig("expense_bar.png", bbox_inches='tight')
    plt.show()