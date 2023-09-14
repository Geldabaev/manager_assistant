import pandas as pd
import matplotlib.pyplot as plt


def is_result_marks(row):
    return (row['Status'] + row["Encouragement"]) - row['Reprimand']


df1 = pd.read_csv("attendance.csv")
df2 = pd.read_csv("statistics.csv")


df1 = df1.drop("Date", axis=1)
df2 = df2.drop("Date", axis=1)

df3 = pd.merge(df1, df2, how='outer')
df3 = df3.fillna(0)

print(df3)