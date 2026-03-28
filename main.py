import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


df = pd.read_csv("insurance.csv")

print("Dataset Preview:\n", df.head())
print("\nColumns in dataset:", df.columns)


df = df.dropna()


conn = sqlite3.connect("insurance.db")


df.to_sql("customers", conn, if_exists="replace", index=False)


bmi_col = "bmi"          
value_col = "charges"   



query_avg = f"SELECT ROUND(AVG({value_col}), 2) AS Avg_Value FROM customers"
avg_result = pd.read_sql_query(query_avg, conn)
print(f"\nAverage {value_col}: {avg_result.iloc[0,0]}")


query_high = f"SELECT * FROM customers WHERE {value_col} > (SELECT AVG({value_col}) FROM customers)"
high_value = pd.read_sql_query(query_high, conn)
print(f"\nHigh {value_col} Customers:\n", high_value)


df["HighRisk"] = df[value_col].apply(lambda x: 1 if x > df[value_col].mean() else 0)

print("\nRisk Distribution:\n", df["HighRisk"].value_counts())


df.plot(x=bmi_col, y=value_col, kind="bar")
plt.title(f"{bmi_col} vs {value_col}")
plt.show()


conn.close()