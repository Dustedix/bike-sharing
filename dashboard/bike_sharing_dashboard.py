import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def highest_lowest_season(df):
    season_rent_df = df.groupby("season").total_count.sum().sort_values(ascending=False).reset_index()
    season_rename = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    season_rent_df['season'] = season_rent_df['season'].replace(season_rename)
    return season_rent_df

def total_user_month(df):
    user_month_df = df.groupby("month").registered.sum().reset_index()
    month_rename = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    user_month_df['month'] = user_month_df['month'].replace(month_rename)
    return user_month_df

def year_versus(df):
    registered_user_df = df.loc[:, ['year', 'month', 'registered']]

    ##Rename
    month_rename = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    registered_user_df['month'] = registered_user_df['month'].replace(month_rename)
    registered_user_df = registered_user_df.groupby(['year','month'])['registered'].sum().reset_index()

    ##Re Order Month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    registered_user_df = registered_user_df.sort_values(by=['year','month'],key=lambda x: x.map({month: i for i, month in enumerate(month_order)}))
    registered_user_df = registered_user_df.reset_index(drop=True)

    return registered_user_df

all_df = pd.read_csv("new_day_df.csv")

datetime_columns = ["datetime"]
all_df.sort_values(by="datetime", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Input
highest_lowest = highest_lowest_season(all_df)
total_user = total_user_month(all_df)
year_versus = year_versus(all_df)

#Header
st.header('Bike Sharing Analysis')

##Highest vs Lowest Season
st.subheader("Best & Worst Season for Bike Renting")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="total_count", y="season", data=highest_lowest.head(4), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Season for Renting", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=40)
ax[0].tick_params(axis='x', labelsize=40)

sns.barplot(x="total_count", y="season", data=highest_lowest.sort_values(by="total_count", ascending=True).head(4), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].set_title("Worst Season for Renting", loc="center", fontsize=40)
ax[1].tick_params(axis='y', labelsize=40)
ax[1].tick_params(axis='x', labelsize=40)
st.pyplot(fig)

#Total Registered User from 2011 to 2012

st.subheader("Total Registered Users 2011 to 2012")
fig, ax = plt.subplots(figsize=(35, 15))
plt.plot(total_user["month"], total_user["registered"], marker='o', linewidth=2, color="#0ec20e")
plt.title("Number of Registered Users per Month (2021)", loc="center", fontsize=50)
plt.xticks(rotation=45,fontsize=40)
plt.yticks(fontsize=40)
plt.grid()
st.pyplot(fig)

#2011 vs 2012 Registeres User
st.subheader("2011 vs 2012 Registered User per Month")
fig, ax = plt.subplots(figsize=(35, 15))
sns.barplot(data=year_versus, x='month', y='registered', hue='year', ci=None)

plt.xlabel('Month')
plt.ylabel('Total Orders')
plt.title('Total Orders by Month (2011 vs. 2012)',loc='center',fontsize=50)
plt.legend(title='Year', labels=['2011', '2012'])
plt.xticks(rotation=45,fontsize=40)
plt.yticks(fontsize=40)
plt.grid()
st.pyplot(fig)
