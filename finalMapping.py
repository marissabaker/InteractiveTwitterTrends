#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 00:22:00 2019

@author: marissabaker and Lilian Gjertsson
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 14:18:04 2019

@author: Marissa Baker and Lilian Gjertsson
"""

import tweepy
import json
import csv
import plotly
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='marissabaker', api_key='o5D2U1bVcVTXucvxWSTw')
import pandas as pd
import plotly.plotly as py

### Getting Data ###

consumer_key = "Y2bbEd3dVrhA9oOB4jKQByiH5"
consumer_secret = "7ExUONf8f8taWhgSmkKjoB3BM7bUBEmGRO1fhHK6PGltFUrhMb"
access_token = "1116319401454731265-kvmyCFvn2phtvopBVWFFMLkaKKmFHK"
access_token_secret = "tFc0r7J089ZmVwkYYHOrUsvXw6q3YTQyyEAsI2aO0sA6n"

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth) 

# -*- coding: utf-8 -*-
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

#Return top 3 trends for a country in dict form
def getTrends(locationID, location):
	trends1 = api.trends_place(locationID, languages=['en'])

	trends = trends1[0]['trends']
	names = []
	names.append(location)
	i = 0
	for trend in trends:
		if trends[i] != None and i < 3:
			if isEnglish(trend["name"]):
				names.append(trend['name'])
				i += 1

	dictNames = {location: names}
	return dictNames


####### FIND COUNTRY CODES ########
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
# print(df)
codes = {}
for i in range(1, len(df)):
	codes.update({df["COUNTRY"][i]: df["CODE"][i]})
	#print (df["CODE"][i], df["COUNTRY"][i])
codes.update({"korea": "KOR"})


####### FIND TRENDS #########
data = {}
#Get woeid for every country Twitter has trends for
trends = api.trends_available()
#Get trends for every country, add to dict
for trend in trends:
	if trend["placeType"]["name"] == "Country":
		data.update(getTrends(trend["woeid"], trend["name"]))


############ PRINT DATA TO CSV #################
with open('trends.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["USERS(MILLIONS)", "CODE", "COUNTRY", "Trends0", "Trends1", "Trends2"])
    for key, value in data.items():
    	length = len(value)
    	if length == 2:
    		writer.writerow([1, codes.get(key), value[0], value[1]])
    	if length == 3:
    		writer.writerow([1, codes.get(key), value[0], value[1], value[2]])
    	if length == 4:
    		writer.writerow([1, codes.get(key), value[0], value[1], value[2], value[3]])


#### CREATING PLOT ###


df = pd.read_csv('trends.csv', encoding='latin-1')

df['text'] = df['COUNTRY'] + '<br>' + \
    'Top Trends: ' + '<br>' + '<br>' + \
    df['Trends0'] + '<br>' + \
    df['Trends1'] + '<br>' + \
    df['Trends2']
    
data = [go.Choropleth(
    locations = df['CODE'],
    z = df['USERS(MILLIONS)'],
    text = df['text'],

     colorscale = [
         [0, "rgb(155, 242, 210)"],
         [0.35, "rgb(155, 242, 210)"],
         [0.5, "rgb(155, 242, 210)"],
         [0.6, "rgb(155, 242, 210)"],
         [0.7, "rgb(155, 242, 210)"],
         [1, "rgb(155, 242, 210)"]
     ],

    
    showscale = False,
    autocolorscale = False,
    reversescale = True,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
# =============================================================================
#     colorbar = go.choropleth.ColorBar(
#         #tickprefix = '$',
#         title = 'NUMBER OF TWITTER USERS'),
# =============================================================================
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Twitter Trends'
    ),
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = True,
        showcountries = True,
        projection = go.layout.geo.Projection(
            type = 'equirectangular'
        )
    ),
# =============================================================================
#     annotations = [go.layout.Annotation(
#         x = 0.55,
#         y = 0.1,
#         xref = 'paper',
#         yref = 'paper',
#         text = 'Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
#             CIA World Factbook</a>',
#         showarrow = False
#     )]
# =============================================================================
)

fig = go.Figure(data = data, layout = layout)
py.plot(fig, filename = 'd3-world-map')