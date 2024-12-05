# net_migration-net_population-dashboard
This Repo contain the code of Data Extraction from API and datasets of Dashboard 
Fetching Data from the WBData API 🌍📊
This guide explains how to fetch data from the WBData API using Python. The World Bank Data API provides access to a wealth of international economic, social, and environmental data.

Prerequisites 🚀
Before you begin, make sure you have the following:

Python installed on your machine
The wbdata library (install via pip if you haven't already)
bash

pip install wbdata
Steps to Fetch Data 📥
Import Libraries 📚 Start by importing the necessary libraries:
python


import wbdata
import pandas as pd
Set Up Your Query 🔍 Define the indicators and countries you want to analyze. For example, to get data for GDP (indicator: 'NY.GDP.MKTP.CD') for the United States ('USA'):
python


indicators = {'NY.GDP.MKTP.CD': 'GDP'}
countries = ['USA']
Fetch the Data 🌐 Use the get_dataframe function to fetch and convert the data into a Pandas DataFrame:



data = wbdata.get_dataframe(indicators, country=countries)
Explore the Data 🔍 Check the first few rows of the DataFrame to understand its structure:
python


print(data.head())
Visualize the Data 📈 You can visualize the fetched data using libraries like Matplotlib or Plotly. For example, using Matplotlib:

import matplotlib.pyplot as plt

data.plot()
plt.title('GDP of USA Over Time')
plt.ylabel('GDP in USD')
plt.show()


Conclusion 🎉
Fetching data from the WBData API is straightforward with Python. You can easily manipulate and visualize this data to gain insights into global economic trends. Happy coding! 👩‍💻👨‍💻
