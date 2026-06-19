import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('UPI.xlsx')

print(df.head())
print("\nDataset Information")
print(df.info())
print("\nDataset statistics")
print(df.describe())

print("\nCheck Dataset have duplicates")
print(df.duplicated())

print("Total duplicates:", df.duplicated().sum())
print(df.shape)
print("\nCheck Null Values in dataset")
print(df.isnull())

df[df['On0us Transactions_Volume (Mn)'].isnull() | df['On0us Transactions_Value (Cr)'].isnull()]
print(df)
print("-------------------------------------------------------------")

df['On0us Transactions_Volume (Mn)']=(
    df["On0us Transactions_Volume (Mn)"].fillna(df["On0us Transactions_Volume (Mn)"].median())
)
df["On0us Transactions_Value (Cr)"]=(
    df["On0us Transactions_Value (Cr)"].fillna(
        df["On0us Transactions_Value (Cr)"].median()
    )
)
print("check the dataset after clean null value")
print(df.isnull().sum())


print("check the numeric value")
print(df.dtypes)

print((df.select_dtypes(include='number') < 0).sum())

df['year']=df['Date'].dt.year
df['Month']=df['Date'].dt.month

print(df)

avg_transaction=df['Avg_Transaction_Value'] = (
    df['Total_Value (Cr)'] /
    df['Total_Volume (Mn)']
)
print(avg_transaction)

print('Which UPI applications have the highest transaction volume?')

result=(df.groupby('Application Name')['Total_Volume (Mn)'].sum().sort_values(ascending=False).head(5))
print(result)

print(' Which apps grew fastest from 2022 to 2026?')
growth_df = df[df['year'].isin([2022, 2026])]

pivot = growth_df.pivot_table(
    index='Application Name',
    columns='year',
    values='Total_Volume (Mn)',
    aggfunc='sum'
).dropna()

pivot['growth'] = pivot[2026] - pivot[2022]
print(pivot.sort_values('growth', ascending=False).head(5))


print('What is the monthly trend of total UPI value?')
df['Month']=pd.to_datetime(df['Date']).dt.to_period('M')
monthly_trend=df.groupby('Month')['Total_Value (Cr)'].sum()
print(monthly_trend.head(5))


print('Which apps have the highest average transaction value?')
avg_check=df['average_transaction']=df['Total_Value (Cr)']/df['Total_Volume (Mn)']
avg_check = (
    df.groupby('Application Name')['average_transaction']
    .mean()
    .sort_values(ascending=False)
    .head(5)
)

print(avg_check)

print('Does transaction volume increase with time?')

df['Year'] = pd.to_datetime(df['Date']).dt.year

transaction = (
    df.groupby('Year')['Total_Volume (Mn)']
    .sum()
)

print(transaction)

print('Which application generated the highest total transaction value each year?')


highest_transaction=(df.groupby(['Year','Application Name'])['Total_Value (Cr)'].sum().reset_index())
highest_transaction = (
    highest_transaction.sort_values(['Year', 'Total_Value (Cr)'], ascending=[True, False])
    .groupby('Year')
    .head(1)
)

print(highest_transaction)


print('How does UPI grow over time?')
upi_growth=df.groupby('Date')['Total_Value (Cr)'].sum()
print(upi_growth.tail(3))


print("Which app dominates UPI")

total_volume = df['Total_Volume (Mn)'].sum()

app_volume = (
    df.groupby('Application Name')['Total_Volume (Mn)']
    .sum()
    .sort_values(ascending=False)
)

app_share = (app_volume / total_volume) * 100

print(app_share.head(5))


print('Which apps are losing transaction value?')

year_app = (
    df.groupby(['Application Name', 'Year'])['Total_Value (Cr)']
    .sum()
    .reset_index()
)

year_app['change'] = (
    year_app.groupby('Application Name')['Total_Value (Cr)']
    .diff()
)

print(year_app.sort_values('change').head(5))

print("Outlier Analysis")
print(df.describe())

print('check outliers using IQR method')
cols=['Total_Volume (Mn)',
    'Total_Value (Cr)']
for i in cols:
    Q1=df[i].quantile(0.25)
    Q3=df[i].quantile(0.75)
    IQR=Q3-Q1
    lower_bound=Q1-1.5*IQR
    upper_bound=Q3+1.5*IQR
    outliers=df[(df[i]<lower_bound) | (df[i]>upper_bound)]
    print(f"Outliers in {i}: {outliers.shape[0]}")

print(outliers[['Application Name', 'Date', i]]) 

print(
    df[['Application Name','Date','Total_Value (Cr)']]
    .sort_values('Total_Value (Cr)', ascending=False)
    .head(10)
)

print(df.groupby('Application Name')['Total_Value (Cr)'].sum().sort_values(ascending=False).head(10))

print('Correlation between Total Volume and Total Value')
correlateted=df[['Total_Volume (Mn)', 'Total_Value (Cr)']].corr()
print(correlateted)

print('which app has the most inconsistent transaction patterns?')

app_patterns = (
    df.groupby('Application Name')['average_transaction'].mean().sort_values(ascending=False) 
)
print(app_patterns.head(5))

print('What is the total transaction value, volume, and number of UPI applications?')
total_value=df['Total_Value (Cr)'].sum()
total_volume=df['Total_Volume (Mn)'].sum()
app_share = df['Application Name'].nunique()
print(f"Total Transaction Value: {total_value}")
print(f"Total Transaction Volume: {total_volume}")
print(f"Total UPI Applications: {app_share}")

sns.set_theme(style="whitegrid")
trend = df.groupby('Date')['Total_Value (Cr)'].sum()

plt.figure(figsize=(12,6))
sns.lineplot(x=trend.index, y=trend.values, marker='o')

plt.title("UPI Transaction Value Trend")
plt.xlabel("Date")
plt.ylabel("Total Value (Cr)")

plt.xticks(rotation=45)
plt.show()

share = (
    df.groupby('Application Name')['Total_Value (Cr)']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))

sns.barplot(
    x=share.values,
    y=share.index
)

plt.title("Top UPI Applications by Transaction Value")
plt.xlabel("Value (Cr)")
plt.ylabel("Application")

plt.show()

plt.figure(figsize=(11,10))

sns.scatterplot(
    data=df,
    x='Total_Volume (Mn)',
    y='Total_Value (Cr)'
)

plt.title("Transaction Volume vs Value")

plt.show()

plt.figure(figsize=(8,5))

sns.boxplot(
    y=df['Total_Value (Cr)']
)

plt.title("Transaction Value Outlier Check")

plt.show()

growth = (
    df.groupby(['Year','Application Name'])['Total_Value (Cr)']
    .sum()
    .reset_index()
)

pivot = growth.pivot(
    index='Application Name',
    columns='Year',
    values='Total_Value (Cr)'
)

pivot['Growth'] = pivot[2026] - pivot[2022]

top_growth = (
    pivot['Growth']
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(11,10))

sns.barplot(
    x=top_growth.values,
    y=top_growth.index
)

plt.title("Fastest Growing UPI Apps")

plt.show()

top5 = share.head(5)

plt.figure(figsize=(7,7))

plt.pie(
    top5.values,
    labels=top5.index,
    autopct='%1.1f%%'
)

plt.title("Top 5 UPI Market Share")

plt.show()

df['Avg_Transaction_Value'] = (
    df['Total_Value (Cr)'] /
    df['Total_Volume (Mn)']
)

top_avg = (
    df.groupby('Application Name')['Avg_Transaction_Value']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(11,10))

sns.barplot(
    x=top_avg.values,
    y=top_avg.index
)

plt.title("Average Transaction Value by App")

plt.show()

df.to_csv("clean_upi_data.csv", index=False)
