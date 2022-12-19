import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = "Distribution of BioMedical Studies in Iran"
APP_SUB_TITLE = "different committees are merged here based on their province"


#df[(df.date.map(lambda x:x.year) == 2020) & (df.state == 'Tehran') & 
# (df.type == 'Thesis')]['number of studies'].sum()

def display_map(df, year):
    df = df[df.date.map(lambda x:x.year) == year]

    map = folium.Map(location = [32.65, 54] , zoom_start = 5 , scrollWheelZoom = False , 
    tiles = 'CartoDB positron')
    
    choropleth = folium.Choropleth(
        geo_data = 'ir_states_boundaries_coordinates.geojson',
        data = df,
        columns = ('state', 'number of studies'),
        key_on = 'feature.properties.name:en',
        line_opacity = 0.8,
        highlight = True
    )
    choropleth.geojson.add_to(map)
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name:en']
        feature['properties']['studies'] = 'number of recorded studies: ' + str(df[(df.state == state_name)]['number of studies'].sum())
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name:en' , 'studies'] , labels = False)
    )

    
    st_map = st_folium(map , width = 700, height = 450)

    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['name:en']
        return state_name

def display_time_type(df):
    year_list = list(df.date.map(lambda x:x.year).unique())
    year_list.sort()
    year = st.sidebar.selectbox('Year' , year_list, len(year_list)-1)
    type = st.sidebar.selectbox('Type', ['Thesis', 'Proposal' ])
    st.header(f'{type} records of {year} ')
    return year, type


def display_facts1(df, year, state, type):

    df = df[(df.date.map(lambda x:x.year) == year) & (df.state == state) & (df.type == type)]
    num_committee = df.committee.unique()
    total = df['number of studies'].sum()

    st.metric(label = " of {type} studies"  ,value = '{:,}'.format(total) )


def display_facts2(df, state):
    
    df = df[df.state == state]
    num_committee = df.committee.unique()

    st.metric(label = "committees"  ,value = '{:,}'.format(len(num_committee)) )


def display_facts3(df, year, state, type):
    
    df = df[(df.date.map(lambda x:x.year) == year) & (df.state == state) & (df.type == type)]
    num_committee = df.committee.unique()
    mean = df['number of studies'].sum()/len(num_committee)

    st.metric(label = 'studies per committee'  ,value = '{:,}'.format(mean) )



def main():

    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    # load data
    df = pd.read_csv("GroupBy.csv")
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')

    # display_facts(df, year, state, type)

    # display filters and map 
    year, type = display_time_type(df)
    state_name = display_map(df, year)


    

    # Display Metrices
    st.subheader(f'{type} records of {state_name}')
    col1, col2, col3 = st.columns(3)
    with col1:
        display_facts1(df, year, state_name, type)
    with col2:
        display_facts2(df, state_name)
    with col3: 
        display_facts3(df, year, state_name, type)

    


if __name__ == "__main__" :
    main()



    # challenge both types 
