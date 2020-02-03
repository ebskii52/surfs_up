# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

# %%
import numpy as np
import pandas as pd

# %%
import datetime as dt

# %%
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Table

# %%
engine = create_engine("sqlite:///hawaii.sqlite")

# %%
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# %%
# We can view all of the classes that automap found
Base.classes.keys()


# %%
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# %%
# Create our session (link) from Python to the DB
session = Session(engine)

# %% [markdown]
# # Exploratory Climate Analysis

# %%
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
# print(df)
# print(df.to_string(index=False))

#greater than the start date and smaller than the end date
Julymask = (df['date'] > '2017-07-01') & (df['date'] <= '2017-07-30')

Decmask = (df['date'] > '2017-12-01') & (df['date'] <= '2017-12-31')


JulyDF = df.loc[Julymask]
DecDF = df.loc[Decmask]


print(JulyDF)

# %%
# Use Pandas to calcualte the summary statistics for the precipitation data
JulyDF.describe()


# %%
# How many stations are available in this dataset?
session.query(func.count(Station.station)).all()


# %%
# What are the most active stations?
# List the stations and the counts in descending order.
session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()


# %%
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?
session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).all()


# %%
# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
print(results)

df = pd.DataFrame(results, columns=['tobs'])
df.plot.hist(bins=12)
plt.tight_layout()


# %%
# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    #print jsonify(temps)
    return(temps)
    

JulyTemp = calc_temps('2017-06-01', '2017-06-30')
JulyDF   = pd.DataFrame(JulyTemp, columns=['tobs'])

JulyDF

# %% 
####################################
########## Challenge ###############
####################################

# %%
def WeatherData(start=None, end=None):
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp, Measurement.tobs).all()
    # Save the query results as a Pandas DataFrame and set the index to the date column
    df = pd.DataFrame(results, columns=['date','precipitation', 'temperature'])
    df.set_index(df['date'], inplace=True)
    df.index = pd.to_datetime(df.index)
    df.drop("date",axis=1,inplace=True)
    df = df[(df.index.month.isin([f'{start}',f'{end}']))]
    return(df)

# %%
## Identify count, max, min, mean, standard deviation, and percentiles in June 
# across all of the stations and years using the describe() function, with no errors. 
JuneDf = WeatherData('06','06')
JuneDf.describe()


# %%
## Identify count, max, min, mean, standard deviation, and percentiles in December 
# across all of the stations and years using the describe() function, with no errors. 
DecTemp = WeatherData('12', '12')
DecTemp.describe()


# %%
# Comparing June and December Temperature and Percipitation.

# Analysis
# July seems to has favorable temperature with 83F Max and 71F Min, however, December has lower rainfall with lower temperature. 
# For Ice-cream surf July seems to better month to have long hour of operation.

# Recommendation for futher Analysis
# 1) Wynn needs to sample more data on the foot traffic of the beach during the year to know the traffic season.
# 2) Get the data on the average age of people visiting to help in understanding the group of people, as kids are important driving factor for Icecream sales.
