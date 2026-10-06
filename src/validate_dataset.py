import pandas as pd

df = pd.read_csv("data/quotes.csv", encoding="utf-8-sig")
print("Shape:", df.shape)
print("Columns:", list(df.columns))
print("\nQuotes per author:")
print(df["author"].value_counts())

print("\nEmpty values:\n", df.isna().sum())
print("\nQuote length (chars):")
print(df["quote"].str.len().describe())

print("\nSample:")
print(df.sample(5, random_state=1)[["author", "quote"]].to_string())