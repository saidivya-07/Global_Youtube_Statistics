import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt

# Function to load data
@st.cache_data
def load_data():
    data = pd.read_csv('M_Global_YouTube_Statistics.csv')
    return data

# Load the data
df = load_data()

# Streamlit app title
st.title('Global YouTube Channel Analytics')

# Sidebar for filters
st.sidebar.title('Filters and Insights')
selected_category = st.sidebar.selectbox('Select a Category', options=np.insert(df['category'].unique(), 0, 'All'))
selected_countries = st.sidebar.multiselect('Select Countries', options=df['Country'].unique(), default=df['Country'].unique())

# Filter data based on the selected category and countries
if selected_category != 'All':
    df = df[df['category'] == selected_category]
df = df[df['Country'].isin(selected_countries)]

# Sidebar - Top 3 YouTubers
st.sidebar.subheader('Top 3 YouTubers')
top_youtubers = df.sort_values(by='subscribers', ascending=False).head(3)
for index, row in top_youtubers.iterrows():
    st.sidebar.write(f"{row['Youtuber']} - {row['subscribers']} subscribers")

# Create tabs for navigation
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Detailed Statistics", "Distribution of Channels by Country", "Top 5 Youtubers"])

with tab1:
    st.markdown("## **Home**")
    st.image('https://images.ctfassets.net/00i767ygo3tc/1hxo0WiNGieEQMs3pgb8zm/95487ae5d66ecd7d608ab0d89abbec84/images-more-subscribers-youtube.png?w=900&fm=webp', caption='Youtube Statistics')
    st.markdown("**Welcome to YouTube Insights**, Discover trends, analyze channel growth, and gain insights into YouTube's vast landscape right here.")

with tab2:
    st.header("**Detailed Statistics**")

    # Category-wise Analysis
    st.header('Category-wise Analysis')
    category_chart = alt.Chart(df).mark_bar().encode(
        x='category',
        y='average(subscribers)',
        color='Country',
        tooltip=['category', 'average(subscribers)', 'Country']
    )
    st.altair_chart(category_chart, use_container_width=True)

    # Time Series Analysis
    st.header('YouTube Channel Growth Over Time')
    if 'created_year' in df.columns:
        time_series_data = df.groupby(['created_year', 'Country']).size().reset_index(name='New Channels')
        time_series_chart = alt.Chart(time_series_data).mark_line().encode(
            x=alt.X('created_year:O', axis=alt.Axis(title='Year')),
            y=alt.Y('New Channels:Q', axis=alt.Axis(title='Number of New Channels')),
            color='Country:N',
            tooltip=['created_year', 'Country', 'New Channels']
        )
        st.altair_chart(time_series_chart, use_container_width=True)
    else:
        st.write("Time-related data not available for time series analysis.")

    # Interactive Bar Chart - Distribution by Country
    st.header('Distribution of Channels by Country')
    country_chart = alt.Chart(df).mark_bar().encode(
        x='Country',
        y='count()',
        color='Country',
        tooltip=['Country', 'count()']
    )
    st.altair_chart(country_chart, use_container_width=True)

    # Aggregate data for the map visualization
    country_agg = df.groupby('Country', as_index=False).agg(
        total_subscribers=pd.NamedAgg(column='subscribers', aggfunc='sum'),
        youtuber_count=pd.NamedAgg(column='Youtuber', aggfunc='nunique')
    )

    # Create the choropleth map visualization
    fig = px.choropleth(
        country_agg,
        locations="Country",
        locationmode="country names",
        color="total_subscribers",
        hover_name="Country",
        hover_data={"total_subscribers": True, "youtuber_count": True},
        title="Total Subscribers by Country",
        color_continuous_scale=px.colors.sequential.Viridis,
        projection="natural earth"
    )

    # Update layout for a better look
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            lakecolor="rgba(0,0,0,0)",
            landcolor="rgba(243,243,243,1)",
            showland=True,
            countrycolor="Black"
        )
    )
    # Display the figure in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

    # Calculate averages
    country_avg_subscribers = df.groupby('Country')['subscribers'].mean()
    country_avg_video_views = df.groupby('Country')['video views'].mean()

    # Displaying the averages
    st.write("Average Number of Subscribers by Country")
    st.dataframe(country_avg_subscribers)

    st.write("Average Number of Video Views by Country")
    st.dataframe(country_avg_video_views)

    

with tab3:
    st.subheader("**Distribution of Channels by Country**")

    # Create the scatter plot map visualization for individual YouTubers
    fig = px.scatter_geo(
        df,
        lat='Latitude',
        lon='Longitude',
        size='subscribers',
        color='rank',
        hover_name='rank',
        hover_data={'subscribers': True, 'rank': True},
        title="Global YouTube Channel Distribution",
        projection="natural earth"
    )

    # Update layout to resemble a real map
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        geo=dict(
            showland=True,
            landcolor="rgb(212, 239, 223)",
            countrycolor="rgb(200, 200, 200)",
            showocean=True,
            oceancolor="rgb(187, 222, 251)",
            lakecolor="rgb(187, 222, 251)"
        ),
        paper_bgcolor="rgba(255, 255, 255, 1)"
    )

    # Display the figure in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)

    # Display the top 5 ranked countries based on rank
    st.subheader("Countries With their Ranking")
    top_countries = df.groupby('Country')['rank'].min().sort_values().head(5)
    for country, rank in top_countries.items():
        st.write(f"{country}: {rank}")

with tab4:
    st.subheader("**Top 5 Youtubers**")
    st.image('https://api.backlinko.com/app/uploads/2021/01/youtube-users-1280x670.webp', caption='Image Caption')
    top5_youtubers = df.nlargest(5, 'subscribers')
    for index, row in top5_youtubers.iterrows():
        wiki_url = f"https://en.wikipedia.org/wiki/{row['Youtuber'].replace(' ', '_')}"
        youtube_url = f"https://www.youtube.com/c/{row['Youtuber'].replace(' ', '')}"
        st.markdown(
            f"**{row['Youtuber']}** - Subscribers: {row['subscribers']:,} "
            f"[Wikipedia]({wiki_url}) | [YouTube]({youtube_url})"
        )
        st.markdown(f"Total Video Views: {row['video views']:,} - Videos Uploaded: {row['uploads']}")
        st.markdown("---")
