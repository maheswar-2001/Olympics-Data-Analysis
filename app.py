import streamlit as sl
import pandas as pd
import preprocess,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')

df = preprocess.process(df,df_region)

sl.sidebar.title("Olympics Analysis")
sl.sidebar.image('olympics.png')
option = sl.sidebar.radio(
    'Select an Option',
    ("Medal Tally","Overall Analysis","Country-Wise Analysis","Athlete wise Analysis")
)

#sl.dataframe(df)


if option == 'Medal Tally':
    sl.sidebar.title("Medal Tally")
    years,country = helper.country_wise(df)

    selected_year = sl.sidebar.selectbox("Select Year",years)
    selected_country = sl.sidebar.selectbox("Select Country", country)

    medal = helper.fetch_data(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_year == 'Overall':
        sl.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        sl.title("Medal Tally in "+str(selected_year)+" Olympics" )
    if selected_year == 'Overall' and selected_country != 'Overall':
        sl.title(selected_country+ " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        sl.title(selected_country + " performance in "+ str(selected_year)+" Olympics")

    sl.table(medal)

elif option == 'Overall Analysis':
    # How many times Olympics is being played
    editions = df['Year'].unique().shape[0]-1

    # In how many cities is Olypics is being played
    cities = df['City'].unique().shape[0]

    # Number of Different sports being played in the olympics
    sports = df['Sport'].unique().shape[0]

    # Number of event happened in the olypics
    events = df['Event'].unique().shape[0]

    # Number of atheletes participated in olympics
    players = df['Name'].unique().shape[0]

    #Number of nations participating
    countries = df['region'].unique().shape[0]

    sl.title("Top Statistics")
    col1,col2,col3 = sl.columns(3)
    with col1:
        sl.header("Editions")
        sl.title(editions)
    with col2:
        sl.header("Cities")
        sl.title(cities)
    with col3:
        sl.header("Sports")
        sl.title(sports)

    col4, col5, col6 = sl.columns(3)
    with col4:
        sl.header("Events")
        sl.title(events)
    with col5:
        sl.header("Athletes")
        sl.title(players)
    with col6:
        sl.header("Countries")
        sl.title(countries)

    sl.title("Participating Nations over years")
    nations = helper.data_time(df,'region')
    fig = px.line(nations, x='Edition', y='region')
    sl.plotly_chart(fig)

    sl.title("Events over the years")
    events = helper.data_time(df,'Event')
    fig = px.line(events, x='Edition', y='Event')
    sl.plotly_chart(fig)

    sl.title("Athelets of the years")
    athlete = helper.data_time(df, 'Name')
    fig = px.line(athlete, x='Edition', y='Name')
    sl.plotly_chart(fig)

    sl.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    sl.pyplot(fig)

    sl.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = sl.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    sl.table(x)

elif option == 'Country-Wise Analysis':

    sl.sidebar.title('Country-Wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = sl.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    sl.title(selected_country + " Medal Tally over the years")
    sl.plotly_chart(fig)

    sl.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(15, 15))
    ax = sns.heatmap(pt, annot=True)
    sl.pyplot(fig)

    sl.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    sl.table(top10_df)

elif option == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    sl.title("Distribution of Age")
    sl.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    sl.title("Distribution of Age wrt Sports(Gold Medalist)")
    sl.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

#     sl.title('Height Vs Weight')
#     selected_sport = sl.selectbox('Select a Sport', sport_list)
#     temp_df = helper.weight_v_height(df,selected_sport)
#     fig,ax = plt.subplots()
#     ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'])
#     sl.pyplot(fig)

    sl.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=700, height=600)
    sl.plotly_chart(fig)
