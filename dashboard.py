import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import time 

# col1, col2 = st.columns(2)

# col1.header("Airbnb prices in Paris")
# col1.info(
#         "something abt paris"
#         "idk words")

# dropdown_choice = col1.selectbox( 'Select an option' ,('Average price by night','other'))

# col2.header("Grayscale")

st.set_page_config(layout="wide")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 0rem;
                    padding-right: 0rem;
                }
            
      
        </style>
        """, unsafe_allow_html=True)

with st.sidebar:
    st.sidebar.title("How much does it cost to rent an Airbnb in Paris?")


 

#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

#     with st.spinner("Loading..."):
#         # time.sleep(5)
#         pass
#     st.success("Done!")

    dropdown_choice = st.selectbox( 'Select an option' ,('Home','Average price by night','Room availability','other'))

    if dropdown_choice == 'Home':
       st.sidebar.info(
       """Paris is one of the most visited cities in the world, 
                    known for its rich history, stunning architecture, and 
                    romantic atmosphere. However, with its popularity comes a 
                    high price tag, making it one of Europe's most expensive destinations. 
                    For budget-conscious travelers, finding affordable accommodation is key. 
                    In this data analysis, we explore the most affordable areas to rent an Airbnb 
                    in the city, providing insights into where travelers can save money without 
                    sacrificing the Parisian experience""")

    elif dropdown_choice == 'Average price by night': 
        st.sidebar.info(
            """Made up on 21 arrondissments, some areas far outprice others""")

# dropdown_choice = 'word'
if dropdown_choice == 'Average price by night':
    # Load the data into a Pandas DataFrame
    data = pd.read_csv('data/neighbourhood_price.csv')
    # Create a map centered on Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12, width='100%', height='100%')
    # Add a choropleth layer to the map to show price by neighborhood
    folium.Choropleth(
        geo_data='data/neighbourhoods.geojson',
        name='choropleth',
        data=data,
        columns=['neighbourhood', 'price'],
        key_on='feature.properties.neighbourhood',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Average price by night',
        tooltip = folium.GeoJsonTooltip(fields=['neighbourhood', 'price'], sticky=True, labels=True, toLocaleString=True)

    ).add_to(m)

    # Add a layer control to the map
    folium.LayerControl().add_to(m)

    # Display the map
    folium_static(m, width=1200, height=800)

elif dropdown_choice == 'Home':
       st.image("images/paris-airbnb.jpeg")

elif dropdown_choice == 'Room availability':
    st.image("images/availability.png")
    st.image("images/place_per_neighbourhood.png")
