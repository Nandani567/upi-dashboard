import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

df=pd.read_csv('clean_upi_data.csv')

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

st.sidebar.title('Filter')
year_filter = st.sidebar.multiselect('Select Year', options=df['Year'].unique(), default=df['Year'].unique())

app_filter = st.sidebar.multiselect('Select App', options=df['Application Name'].unique(), default=df['Application Name'].unique()[:5])

filtered_df = df[(df['Year'].isin(year_filter)) & (df['Application Name'].isin(app_filter))]

st.title('UPI Transaction Analysis')

# KPI's
total_value = filtered_df['Total_Value (Cr)'].sum()
total_volume = filtered_df['Total_Volume (Mn)'].sum()
apps = filtered_df['Application Name'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Transaction Value (Cr)", f"{total_value:,.0f}")
col2.metric("Total Transaction Volume (Mn)", f"{total_volume:,.0f}")
col3.metric("Active Apps", apps)

st.divider()

st.subheader("UPI Transaction Trend")

trend = filtered_df.groupby('Date')['Total_Value (Cr)'].sum()

fig, ax = plt.subplots(figsize=(10,4))
sns.lineplot(x=trend.index, y=trend.values, ax=ax)
ax.set_title("UPI Value Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Value (Cr)")
plt.xticks(rotation=45)

st.pyplot(fig)


st.subheader("Top Apps by Transaction Value")
top_apps = filtered_df.groupby('Application Name')['Total_Value (Cr)'].sum().sort_values(ascending=False).head(10)  
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=top_apps.values, y=top_apps.index, ax=ax)
ax.set_title("Top 10 Apps by Transaction Value")
ax.set_xlabel("Total Value (Cr)")
ax.set_ylabel("Application Name")
st.pyplot(fig)

st.subheader("Market share")
market_share = filtered_df.groupby('Application Name')['Total_Value (Cr)'].sum()
fig, ax = plt.subplots(figsize=(6,6))
ax.pie(market_share.values, labels=market_share.index, autopct='%1.1f%%', startangle=140)
ax.set_title("Market Share by Transaction Value")
st.pyplot(fig)

st.subheader("Correlation Analysis")
corr = filtered_df[['Total_Value (Cr)', 'Total_Volume (Mn)']].corr()
fig, ax = plt.subplots(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Correlation between Value and Volume")
st.pyplot(fig)

st.subheader("Value vs Volume")
fig, ax = plt.subplots(figsize=(10,6))  
sns.scatterplot(x='Total_Volume (Mn)', y='Total_Value (Cr)', data=filtered_df, ax=ax)
ax.set_title("Value vs Volume")
ax.set_xlabel("Total Volume (Mn)")
ax.set_ylabel("Total Value (Cr)")
st.pyplot(fig)

st.subheader("Yearly Growth")

yearly_total = filtered_df.groupby('Year')['Total_Value (Cr)'].sum()

yearly_growth = yearly_total.pct_change() * 100
fig, ax = plt.subplots(figsize=(10,4))

sns.lineplot(
    x=yearly_growth.index,
    y=yearly_growth.values,
    marker="o",
    ax=ax
)

ax.set_title("Yearly Growth in UPI Value (%)")
ax.set_xlabel("Year")
ax.set_ylabel("Growth %")

plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("Average Transaction Value")

filtered_df['Avg_Transaction'] = (
    filtered_df['Total_Value (Cr)'] /
    filtered_df['Total_Volume (Mn)']
)

avg_app = (
    filtered_df.groupby('Application Name')['Avg_Transaction']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=avg_app.values, y=avg_app.index, ax=ax)

ax.set_title("Average Transaction Value by App")

st.pyplot(fig)

st.markdown("### Key Insight")
st.write("PhonePe dominates total transaction value, indicating strong market leadership in UPI ecosystem.")


# yearly = filtered_df.groupby(['Application Name', 'Year'])['Total_Value (Cr)'].sum().reset_index()
# pivot = yearly.pivot(
#     index='Application Name',
#     columns='Year',
#     values='Total_Value (Cr)'
# )
# growth = pivot.pct_change(axis=1) * 100
# growth = growth.dropna()
# st.subheader("App-wise Growth Heatmap (%)")

# fig, ax = plt.subplots(figsize=(12,6))

# sns.heatmap(
#     growth,
#     cmap="RdYlGn",
#     center=0,
#     linewidths=0.5,
#     ax=ax
# )

# ax.set_title("Year-over-Year Growth (%) by Application")

# st.pyplot(fig)


st.subheader("Outlier Analysis - Value vs Volume")
fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(x='Total_Volume (Mn)', y='Total_Value (Cr)', data=filtered_df, ax=ax)
ax.set_title("Value vs Volume with Outliers")   
ax.set_xlabel("Total Volume (Mn)")
ax.set_ylabel("Total Value (Cr)")
st.pyplot(fig)


st.divider()
st.caption("Built using Streamlit | UPI Transaction Data Analysis Project")

