## Imports
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import streamlit as st
import requests
# from data import Map_data_table_creation as ck

# st.title('This is a title')

def nexrad_map():
    st.markdown("# NexRad Map")
    st.sidebar.markdown("# NexRad Map")
    ### Call the function to pull Map data : 
    # conn, cursor = ck.map_data_tbl()

    # df = pd.read_sql_query("SELECT * from Mapdata", conn) 
    # data = pd.read_fwf('https://www.ncei.noaa.gov/access/homr/file/nexrad-stations.txt')

    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    # data = data.drop(index = 0,axis = 0)
    # st.subheader("Req data :")
    # df = data 
    # st.write(df)
    token = st.session_state["authentication_status"]
    headers = {'Authorization': f'Bearer {token}'}
    # payload = {'stationId':str(station),'day': day_nexrad,'year':year_nexrad,'month':month_nexrad}
    result = requests.get("http://ec2-3-223-141-28.compute-1.amazonaws.com:8000/nexrad/map-data", headers=headers).json()
    df = pd.DataFrame(data = result)
    # print(df)
    st.write(df)
    st.subheader("Graph")
    fig = go.Figure(data=go.Scattergeo(
            locationmode = 'USA-states',
            lon = df['lon'],
            lat = df['lat'],
            text = df['name']+ ',' + df['county'],
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = 'square',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = 'Blues',
                cmin = 0,
                color = df['elev'].astype(int),
                cmax = df['elev'].astype(int).max(),
                colorbar_title="Elevation"
            )))

    fig.update_layout(
            title = 'NexRad Location Across USA',
            geo = dict(
                scope='usa',
                projection_type='albers usa',
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
        )
    # Plot!
    st.plotly_chart(fig, use_container_width=False)
if "authentication_status" not in st.session_state:
   st.session_state["authentication_status"] = False
if st.session_state["authentication_status"] == False:
      st.subheader("Please Login before use")
else:
      nexrad_map()

