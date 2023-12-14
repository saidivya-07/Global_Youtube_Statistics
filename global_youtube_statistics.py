# Import necessary libraries
import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

# Load data
yt_data = pd.read_csv("M_Global_YouTube_Statistics.csv")

# Displaying the DataFrame
st.write("### Data Preview")
st.write(yt_data.head())

# Showing the shape of the DataFrame
st.write("### Data Shape")
st.write(yt_data.shape)

# Missing values
st.write("### Missing Values in Each Column")
st.write(yt_data.isna().sum())

# Visualization 1: Subscribers by Category using Altair with colors
st.write("## Popularity Trends in YouTube Content by Subscribers")
category_group = yt_data.groupby('category').agg({'subscribers': 'sum', 'video views': 'sum'}).reset_index()
category_group_sorted_subscribers = category_group.sort_values('subscribers', ascending=False)

c_subscribers = alt.Chart(category_group_sorted_subscribers).mark_bar(color='teal').encode(
    x=alt.X('subscribers', scale=alt.Scale(type='log')),
    y='category',
    tooltip=['category', 'subscribers']
)
st.altair_chart(c_subscribers, use_container_width=True)

# Visualization 2: Video Views by Category using Altair with colors
st.write("## Video Views by Category")
category_group_sorted_views = category_group.sort_values('video views', ascending=False)

c_views = alt.Chart(category_group_sorted_views).mark_bar(color='coral').encode(
    x=alt.X('video views', scale=alt.Scale(type='log')),
    y='category',
    tooltip=['category', 'video views']
)
st.altair_chart(c_views, use_container_width=True)

# Visualization 3: Relationship Between Subscribers and Average Video Views using Altair with colors
st.write("## Relationship Between Subscribers and Average Video Views")
grouped_data = yt_data.groupby('subscribers')['video views'].mean().reset_index()

c_relationship = alt.Chart(grouped_data).mark_line(color='purple').encode(
    x='subscribers',
    y='video views',
    tooltip=['subscribers', 'video views']
)
st.altair_chart(c_relationship, use_container_width=True)

# Visualization 4: Geographical Influence on YouTube Content by Subscribers using Altair with colors
st.write("## Geographical Influence on YouTube Content by Subscribers")
country_group = yt_data.groupby('Country').agg({'subscribers': 'sum', 'video views': 'sum'}).reset_index()
country_group_sorted_subscribers = country_group.sort_values('subscribers', ascending=False)

c_country_subscribers = alt.Chart(country_group_sorted_subscribers).mark_bar(color='green').encode(
    x=alt.X('subscribers', scale=alt.Scale(type='log')),
    y='Country',
    tooltip=['Country', 'subscribers']
)
st.altair_chart(c_country_subscribers, use_container_width=True)

# Visualization 5: Geographical Influence on YouTube Content by Views using Altair with colors
st.write("## Geographical Influence on YouTube Content by Views")
country_group_sorted_views = country_group.sort_values('video views', ascending=False)

c_country_views = alt.Chart(country_group_sorted_views).mark_bar(color='blue').encode(
    x=alt.X('video views', scale=alt.Scale(type='log')),
    y='Country',
    tooltip=['Country', 'video views']
)
st.altair_chart(c_country_views, use_container_width=True)

# Visualization 6: Age of the Channel with its Success - Subscribers using Altair with colors
st.write("## Age of the Channel with its Success - Subscribers")
year_data = yt_data.groupby('created_year').agg({'subscribers': 'sum', 'video views': 'sum'}).reset_index()
year_data_subscribers_sorted = year_data.sort_values('subscribers', ascending=False)

c_year_subscribers = alt.Chart(year_data_subscribers_sorted).mark_bar(color='orange').encode(
    x=alt.X('subscribers', scale=alt.Scale(type='log')),
    y='created_year:O',
    tooltip=['created_year', 'subscribers']
)
st.altair_chart(c_year_subscribers, use_container_width=True)

# Visualization 7: Age of the Channel with its Success - Video Views using Altair with colors
st.write("## Age of the Channel with its Success - Video Views")
year_data_videoviews_sorted = year_data.sort_values('video views', ascending=False)

c_year_views = alt.Chart(year_data_videoviews_sorted).mark_bar(color='red').encode(
    x=alt.X('video views', scale=alt.Scale(type='log')),
    y=alt.Y('created_year:O', axis=alt.Axis(title='Channel Created Year')),
    tooltip=['created_year', 'video views']
).properties(width=600, height=400)

st.altair_chart(c_year_views, use_container_width=True)
# Interactive plot to see how many subscribers a channel had at different points in time
