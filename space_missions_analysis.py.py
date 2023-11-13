# -*- coding: utf-8 -*-
"""Space_Missions_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MmlFiO5aOB0EE80wpSeiGTSYdJpGL4Ou

# Introduction

<center><img src="https://i.imgur.com/9hLRsjZ.jpg" height=400></center>

This dataset was scraped from [nextspaceflight.com](https://nextspaceflight.com/launches/past/?page=1) and includes all the space missions since the beginning of Space Race between the USA and the Soviet Union in 1957!

## For Downloading the Data
link : https://www.kaggle.com/agirlcoding/all-space-missions-from-1957

### Install Package with Country Codes
"""

pip install iso3166

"""### Upgrade Plotly

Run the cell below if you are working with Google Colab.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install --upgrade plotly

pip install jupyter nbconvert

"""### Import Statements"""

import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.preprocessing import LabelEncoder

import warnings
warnings.filterwarnings("ignore")

# These might be helpful:
from iso3166 import countries
from datetime import datetime, timedelta

"""### Notebook Presentation
Once you run this code, it will affect how Pandas displays floating-point numbers in DataFrames and Series. Numbers will be displayed with two decimal places and with commas as thousands separators.
"""

pd.options.display.float_format = '{:,.2f}'.format

"""### Load the Data"""

from google.colab import drive
drive.mount('/content/drive')

df_data = pd.read_csv('/content/drive/MyDrive/ML/space mission analysis/mission_launches.csv')

"""# Preliminary Data Exploration


"""

df_data.head()

df_data.shape

df_data.isnull().sum()

df_data.info()

"""## Data Cleaning - Check for Missing Values and Duplicates

Consider removing columns containing junk data.
"""

# Dropping columns
df_data.drop(columns=['Unnamed: 0.1','Unnamed: 0'],inplace=True)

df_data.head(2)

df_data.tail(2)

"""## Descriptive Statistics"""

df_data.describe()

"""# Number of Launches per Company

A chart that shows the number of space mission launches by organisation.
"""

df_data['Organisation'].value_counts()

launch_counts = df_data['Organisation'].value_counts()

import random

random_colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(df_data))]

plt.figure(figsize=(20,5))  # Set the figure size
launch_counts.plot(kind='bar', color=random_colors)  # Plot the bar chart
plt.title('Number of Space Mission Launches by Organization')  # Set the title
plt.xlabel('Organization')  # Set the x-axis label
plt.ylabel('Number of Launches')  # Set the y-axis label
plt.xticks(rotation=90)  # Rotate the x-axis labels for better readability
plt.show()  # Display the chart

df_data['Country'] = df_data['Location'].str.split(', ').str[-1]
df_data.columns

df_data['Country'].value_counts()

country_counts = df_data['Country'].value_counts()

plt.figure(figsize=(20,5))  # Set the figure size
country_counts.plot(kind='bar', color=random_colors)  # Plot the bar chart
plt.title('Number of Space Mission Launches by Countries')  # Set the title
plt.xlabel('Countries')  # Set the x-axis label
plt.ylabel('Number of Launches')  # Set the y-axis label
plt.xticks(rotation=90)  # Rotate the x-axis labels for better readability
plt.show()  # Display the chart

"""# Number of Active versus Retired Rockets


"""

rocket_sta = df_data["Rocket_Status"].value_counts()

rocket_sta

import plotly.express as px

# Assuming rocket_sta is your DataFrame

fig = px.pie(rocket_sta, values="Rocket_Status", names=rocket_sta.index, title="Rocket Status")
fig.show()



"""# Distribution of Mission Status

How many missions were successful?
How many missions failed?
"""

mission_status = df_data["Mission_Status"].value_counts()
mission_status

fig = px.bar(mission_status, x=mission_status.index, y="Mission_Status", title="Mission Status")
fig.show()

"""# How Expensive are the Launches?

A histogram and visualise the distribution. The price column is given in USD millions (careful of missing values).

## Rocket Cost Distribution with Rocket Status
"""

np.sum(pd.isna(df_data.loc[:, 'Price']))

money= df_data.dropna(subset=['Price'], axis = "rows")
len(money)

np.sum(pd.isna(money.loc[:,'Price']))

money.loc[:, 'Price']

money.loc[:, 'Price'] = money.loc[:,'Price'].fillna(0.0).str.replace(",","")
money.loc[:, 'Price'] = money.loc[:,'Price'].astype(np.float64).fillna(0.0)

money_data= money[money.loc[:, 'Price']<1000]
plt.figure(figsize = (22,6))
sns.histplot(data = money_data, x = 'Price', hue = "Rocket_Status")
plt.show()

"""## Rocket Cost Distribution with Mission Status"""

np.sum(pd.isna(df_data.loc[:,"Mission_Status"]))

plt.figure(figsize = (22,6))
sns.histplot(data = money_data, x = 'Price', hue = "Mission_Status")
plt.show()

"""## Countries and Mission Status"""

encoder = LabelEncoder()
encoder.fit(df_data["Mission_Status"])
encoder

colors = {0: "red",
          1 : "Orange",
          2 : "Yellow",
          3 : "Green"}
colors

countries_dict = {
    'Russia' : 'Russian Federation',
    'New Mexico' : 'USA',
    "Yellow Sea": 'China',
    "Shahrud Missile Test Site": "Iran",
    "Pacific Missile Range Facility": 'USA',
    "Barents Sea": 'Russian Federation',
    "Gran Canaria": 'USA'
}
df_data["Country"] = df_data["Location"].str.split(", ").str[-1].replace(countries_dict)
df_data.head()

fig = make_subplots(rows = 4, cols = 4, subplot_titles = df_data["Country"].unique())
for i, country in enumerate(df_data["Country"].unique()):
    counts = df_data[df_data["Country"] == country]["Mission_Status"].value_counts(normalize = True)*100
    color = [colors[x] for x in encoder.transform(counts.index)]
    trace = go.Bar(x = counts.index, y = counts.values, name = country, marker = {"color" : color}, showlegend = False)
    fig.add_trace(trace, row = (i//4) + 1, col = (i%4)+1)
fig.update_layout(title = {"text":"Countries and Mission Status"}, height = 1000, width = 1100)
for i in range(1,5):
    fig.update_yaxes(title_text = "Percentage", row = i, col = 1)
fig.show()

"""## Use a Choropleth Map to Show the Mission Status By Countries

    Create a choropleth map using the plotly documentation
    Experiment with plotly's available colours. I quite like the sequential colour matter on this map.
    You'll need to extract a country feature as well as change the country names that no longer exist.

Wrangle the Country Names

You'll need to use a 3 letter country code for each country. You might have to change some country names.

    Russia is the Russian Federation
    New Mexico should be USA
    Yellow Sea refers to China
    Shahrud Missile Test Site should be Iran
    Pacific Missile Range Facility should be USA
    Barents Sea should be Russian Federation
    Gran Canaria should be USA

You can use the iso3166 package to convert the country names to Alpha3 format.
"""

country_dict = dict()
for c in countries:
    country_dict[c.name] = c.alpha3
df_data["alpha3"] = df_data["Country"]
df = df_data.replace({
    "alpha3":country_dict
})
df.loc[df["Country"]== "North Korea","alpha3"] = "PRK"
df.loc[df["Country"]== "South Korea","alpha3"] = "KOR"
df.head()

mapdf = df.groupby(["Country","alpha3"])["Mission_Status"].count().reset_index()
mapdf.head()

fig = px.choropleth(mapdf, locations = "alpha3", hover_name = "Country", color = "Mission_Status", title ="Status Mission by Countries")
fig.show()

"""# Use a Choropleth Map to Show the Number of Failures by Country

"""

import plotly.express as px

# Assuming df_data is your DataFrame with the modifications you mentioned
# (e.g., "alpha3" column for country codes, and "Mission_Status" column indicating success/failure)

# Group by country and count the number of failures
failures_by_country = df_data[df_data['Mission_Status'] == 'Failure'].groupby(['Country', 'alpha3']).size().reset_index(name='Number of Failures')

# Create a choropleth map
fig = px.choropleth(failures_by_country,
                    locations="alpha3",
                    color="Number of Failures",
                    hover_name="Country",
                    title="Number of Failures by Country",
                    color_continuous_scale=px.colors.sequential.Reds)

fig.show()



"""# Create a Plotly Sunburst Chart of the countries, organisations, and mission status."""

sun = df_data.groupby(['Country','Organisation','Mission_Status'])["Detail"].count().reset_index()
sun.head()

sun = sun[(sun.Country == "USA") | (sun.Country == "China") | (sun.Country == "Russian Federation") | (sun.Country == "France")]
sun.head()

fig = px.sunburst(sun, path=["Country", "Organisation", "Mission_Status"], values="Detail", title="Sunburst Chart for Countries")
fig.show()

"""# Analyse the Total Amount of Money Spent by Organisation on Space Missions

# Analyse the Amount of Money Spent by Organisation per Launch
"""

money.head()

df_money = money.groupby(["Organisation"])["Price"].sum().reset_index()
df_money = df_money[df_money['Price'] > 0]
df_money.head()

df_money_ = df_money.sort_values(by = ["Price"], ascending = False)[:15]
df_money_.head()

fig = px.bar(df_money_, x = "Organisation", y = "Price", title = "Total Spent Money for each Company")
fig.show()

"""# Chart the Number of Launches per Year"""

import pandas as pd

# Assuming df_data is your DataFrame
# Convert the 'Date' column to datetime, coercing errors to NaT for non-convertible values
df_data['Date'] = pd.to_datetime(df_data['Date'], errors='coerce', utc=True)

# Filter out rows where the 'Date' is NaT (not a valid date)
df_data = df_data.dropna(subset=['Date'])

# Convert all datetime values to a specific timezone, for example, UTC
df_data['Date'] = df_data['Date'].dt.tz_convert('UTC')

# Now you can extract the year
df_data['Year'] = df_data['Date'].dt.year

df_data["year"] = df_data["Date"].apply(lambda datetime: datetime.year)
df_data.head()

ds = df_data["year"].value_counts().reset_index()
ds

ds['random_color'] = np.random.choice(px.colors.qualitative.Set1, size=len(ds))#onlyy for producing the random colrs
fig = px.bar(ds, x = "index", y = "year", title = "Missions Number by Year",color="random_color")
fig.update_layout(showlegend=False)#to remove the side hashtags this is not neede for the random colrs
fig.show()

"""## Rough cost of Space missions in last 10 years (in million dollars)"""

df_data['Year'].astype(int)
last_ten_years_df = df_data[df_data['Year']>2009]
last_ten_years_df['Organisation'].count()

last_ten_years_df.Price.astype('float').sum() ## in dolll

last_ten_years_df['Price'] = last_ten_years_df['Price'].astype(float).fillna(0)
#last_ten_years_df['Rocket'] = pd.to_numeric(last_ten_years_df['Rocket'],errors='coerce')

x = last_ten_years_df.groupby(['Year','Organisation'])['Price'].sum()
x.unstack(level=0)

plt.figure(figsize=(15,6))

sns.scatterplot(x='Date',y='Country', data=df_data)
plt.xlabel('')
plt.ylabel('')
plt.yticks(fontsize=11);
plt.title('Launches Over the years');

"""## Status of Missions in last 10 years"""

last_ten_years_df['Mission_Status'].value_counts()

import seaborn as sns
import matplotlib.pyplot as plt

# Assuming last_ten_years_df is your DataFrame
plt.figure(figsize=(20,5))
sns.countplot(x='Year', data=last_ten_years_df, hue='Mission_Status')
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Mission Status Count for Each Year')

# Remove the log scale
# plt.yscale('log')

plt.show()

"""# Chart the Number of Launches Month-on-Month until the Present

Which month has seen the highest number of launches in all time? Superimpose a rolling average on the month on month time series chart.
"""

import pandas as pd

# Assuming space_mission_df is your DataFrame
# Convert the 'Date' column to datetime, coercing errors to NaT for non-convertible values
df_data['Date'] = pd.to_datetime(df_data['Date'], errors='coerce', utc=True)

# Group by month and count the number of missions
month_wise_missions = df_data.groupby(df_data['Date'].dt.strftime('%B'))['Date'].count()

# Display the result
print(month_wise_missions)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Assuming month_wise_missions is your Pandas Series
plt.figure(figsize=(20,5))
plt.title('Missions per month')
sns.barplot(x=pd.to_datetime(month_wise_missions.index, format='%B').month_name(), y=month_wise_missions, palette='bright')
plt.xticks(rotation=60)
plt.ylabel('Number of missions')
plt.xlabel('')
plt.show()

"""## Chart the Total Number of Mission Failures Year on Year."""

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file

# Convert the "Date" column to a datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'])

# Extract the year from the "Date" column
df_data['Year'] = df_data['Date'].dt.year

# Filter the data for mission failures
failures = df_data[df_data['Mission_Status'] == 'Failure']

# Group the data by year and count the number of failures
failure_counts = failures.groupby('Year').size()

# Plot the chart
plt.figure(figsize=(20,5))
plt.plot(failure_counts.index, failure_counts.values, marker='o')
plt.xlabel('Year')
plt.ylabel('Number of Failures')
plt.title('Total Number of Mission Failures Year on Year')
plt.show()



"""## Chart the Percentage of Failures over Time

Did failures go up or down over time? Did the countries get better at minimising risk and improving their chances of success over time?
"""

import pandas as pd
import matplotlib.pyplot as plt

# Assuming df_data is your DataFrame
# Convert the "Date" column to a datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'])

# Extract the year from the "Date" column
df_data['Year'] = df_data['Date'].dt.year

# Calculate the total number of launches and failures for each year
launch_counts = df_data.groupby('Year').size()
failure_counts = df_data[df_data['Mission_Status'] == 'Failure'].groupby('Year').size()

# Calculate the percentage of failures for each year
failure_percentage = (failure_counts / launch_counts) * 100

# Plot the chart
plt.figure(figsize=(20,5))

plt.plot(failure_percentage.index, failure_percentage.values, marker='o')
plt.xlabel('Year')
plt.ylabel('Percentage of Failures')
plt.title('Percentage of Failures over Time')
plt.show()

# Determine the trend of failures over time
trend = 'up' if failure_percentage.iloc[-1] > failure_percentage.iloc[0] else 'down'
print(f"The trend of failures over time is {trend}.")

# Analyze the improvement over time
improvement = "Yes" if trend == 'down' else "No"
print(f"Did the countries get better at minimizing risk and improving their chances of success over time? {improvement}")

"""# For Every Year Show which Country was in the Lead in terms of Total Number of Launches up to and including including 2020)

Do the results change if we only look at the number of successful launches?
"""

import pandas as pd

# Assuming df_data is your DataFrame
# Convert the "Date" column to a datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'])

# Extract the year from the "Date" column
df_data['Year'] = df_data['Date'].dt.year

# Count the total number of launches and successful launches for each year and country
total_launches = df_data.groupby(['Year', 'Country']).size().reset_index(name='Total Launches')
successful_launches = df_data[df_data['Mission_Status'] == 'Success'].groupby(['Year', 'Country']).size().reset_index(name='Successful Launches')

# Find the country in the lead for each year based on total launches
leading_countries_total = total_launches.loc[total_launches.groupby('Year')['Total Launches'].idxmax()]

# Find the country in the lead for each year based on successful launches
leading_countries_successful = successful_launches.loc[successful_launches.groupby('Year')['Successful Launches'].idxmax()]

# Display the results
print("Country in the Lead for Total Launches Each Year:")
print(leading_countries_total)

print("\nCountry in the Lead for Successful Launches Each Year:")
print(leading_countries_successful)



"""# Create a Year-on-Year Chart Showing the Organisation Doing the Most Number of Launches

Which organisation was dominant in the 1970s and 1980s? Which organisation was dominant in 2018, 2019 and 2020?
"""

import pandas as pd

# Assuming df_data is your DataFrame
# Convert the "Date" column to a datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'])

# Extract the year from the "Date" column
df_data['Year'] = df_data['Date'].dt.year

# Count the total number of launches and successful launches for each year and country
total_launches = df_data.groupby(['Year', 'Country']).size().reset_index(name='Total Launches')
successful_launches = df_data[df_data['Mission_Status'] == 'Success'].groupby(['Year', 'Country']).size().reset_index(name='Successful Launches')

# Find the country in the lead for each year based on total launches
leading_countries_total = total_launches.loc[total_launches.groupby('Year')['Total Launches'].idxmax()]

# Find the country in the lead for each year based on successful launches
leading_countries_successful = successful_launches.loc[successful_launches.groupby('Year')['Successful Launches'].idxmax()]

# Display the results
print("Country in the Lead for Total Launches Each Year:")
print(leading_countries_total)

print("\nCountry in the Lead for Successful Launches Each Year:")
print(leading_countries_successful)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming df_data is your DataFrame
# Convert the "Date" column to a datetime format
df_data['Date'] = pd.to_datetime(df_data['Date'])

# Extract the year from the "Date" column
df_data['Year'] = df_data['Date'].dt.year

# Group by Year and Organization and count the number of launches
launch_counts = df_data.groupby(['Year', 'Organisation']).size().reset_index(name='Launch Count')

# Find the organization with the most launches for each year
leading_organization = launch_counts.loc[launch_counts.groupby('Year')['Launch Count'].idxmax()]

# Plot the Year-on-Year chart
plt.figure(figsize=(50,10))
sns.barplot(x='Year', y='Launch Count', hue='Organisation', data=leading_organization)
plt.xlabel('Year')
plt.ylabel('Number of Launches')
plt.title('Year-on-Year Chart - Organization with the Most Launches')
plt.legend(title='Organization', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Plot the Year-on-Year chart with vertical bars
plt.figure(figsize=(5, 20))
sns.barplot(x='Launch Count', y='Year', hue='Organisation', data=leading_organization, orient='h')
plt.xlabel('Number of Launches')
plt.ylabel('Year')
plt.title('Year-on-Year Chart - Organization with the Most Launches')
plt.legend(title='Organization', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
