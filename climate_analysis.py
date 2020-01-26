#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[4]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[5]:


engine = create_engine("sqlite:///hawaii.sqlite")


# In[6]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[7]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[8]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[9]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Climate Analysis

# In[26]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
#Starting from the last data point in the database. 
prev_year = dt.date(2017, 7, 30) - dt.timedelta(days=30)
# Calculate the date one year from the last date in data set.

# Perform a query to retrieve the data and precipitation scores
results = session.query(Measurement.date, Measurement.prcp)
#print(results.all())
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year)
results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame(results, columns=['date','precipitation'])
df.set_index(df['date'], inplace=True)

# Sort the dataframe by date
#print(df)
#rint(df.to_string(index=False))

#greater than the start date and smaller than the end date
mask = (df['date'] > '2017-07-01') & (df['date'] <= '2017-07-30')

JulyDF = df.loc[mask]

print(JulyDF)

# Use Pandas Plotting with Matplotlib to plot the data
#df.plot()


# In[27]:


# Use Pandas to calcualte the summary statistics for the precipitation data
JulyDF.describe()


# In[ ]:


# How many stations are available in this dataset?
session.query(func.count(Station.station)).all()


# In[ ]:


# What are the most active stations?
# List the stations and the counts in descending order.
session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()


# In[ ]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station == 'USC00519281').all()


# In[ ]:


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
print(results)

df = pd.DataFrame(results, columns=['tobs'])
df.plot.hist(bins=12)
plt.tight_layout()


# In[ ]:


# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates


# # Challenge

# In[ ]:




