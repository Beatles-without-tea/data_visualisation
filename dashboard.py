import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
# import time 
def clean_and_convert(string):
    # remove commas and dollar signs
    string = string.replace(',', '').replace('$', '')

    # convert to float
    number = float(string)

    return number

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

               
        footer {visibility: hidden;}

        </style>
        """, unsafe_allow_html=True)

# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>

# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with st.sidebar:
    st.sidebar.title("How much does it cost to rent an Airbnb in Paris?")


 

#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

#     with st.spinner("Loading..."):
#         # time.sleep(5)
#         pass
#     st.success("Done!")

    dropdown_choice = st.selectbox( 'Select an option' ,
    ('Home','Average price by night','Room availability','Bookings','Reviews','View some airbnbs')
    )

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
    elif dropdown_choice == 'View some airbnbs':
         st.sidebar.info("""
         You now know everything there is to know about airbnbs in Paris. 
         How about looking at some places?
         """)

    elif dropdown_choice == 'Average price by night': 
        st.sidebar.info(
            """Made up of 20 arrondissments, some areas far outprice others.
            Average prices for a night range from around 100 euros to over 300.
             Arrondissements that are
             centrally located, like the 1st (Louvre), 4th (Marais), and 8th 
             (Champs-Élysées), generally have higher Airbnb prices. These areas 
             are in high demand due to their proximity to major tourist attractions, 
             restaurants, shopping districts, and excellent public transportation 
             links.
            In contrast, arrondissements on the outskirts of Paris, such as the 19th 
            and 20th, usually have more affordable Airbnb prices""")

    elif dropdown_choice == 'Bookings':
       st.sidebar.info( """
        Traditionally, 
         the highest demand for Airbnb accommodations tends to coincide with the
          peak tourist season in Paris, 
        which spans from late spring through the end of summer.

        Additionally, there's also an increase in Airbnb activity during the winter
         holiday season, specifically around Christmas and New Year's when Paris is
          known for its festive illuminations and seasonal events.

        Conversely, during the off-peak periods, particularly in late autumn and early 
        winter, the demand for Airbnb accommodation in 
        Paris usually declines. This decrease in tourism activity can result in lower
         prices and increased availability for Airbnb listings.
        """)
    elif dropdown_choice == 'Room availability':
        booking_choice = st.selectbox( 'Choose a graph' ,
        ("Bookings per district","Booking availability")
        )
    elif dropdown_choice == 'Reviews':
    
    #     review_location_choice = st.selectbox( 'Choose an area' ,
    #     ('Hôtel-de-Ville', 'Opéra', 'Louvre', 'Popincourt',
    #    'Buttes-Montmartre', 'Luxembourg', 'Gobelins', 'Entrepôt',
    #    'Batignolles-Monceau', 'Temple', 'Buttes-Chaumont', 'Bourse',
    #    'Ménilmontant', 'Observatoire', 'Panthéon', 'Vaugirard', 'Élysée',
    #    'Reuilly', 'Passy', 'Palais-Bourbon'))

        review_type_choice = st.selectbox( 'Choose a review type' ,
        ('Rating','Cleanliness','Check in','Communication','Location','Value')
        )

        if review_type_choice == 'Rating':
            st.sidebar.info("""Depending on what is important to your trip, 
            whether that is cleanliness, location, or communication, different arrondissements
            have different strengths and weakness. Select a review category from the options above
            to learn more""")
            st.sidebar.info("""The map to the right shows the median review for each arrondissement""")

        elif review_type_choice == 'Cleanliness':
             st.sidebar.info("""
            Some arrondissements may have more professional hosts who use 
            cleaning services to ensure their properties are immaculate before every 
            guest's arrival. On the other hand, hosts in other districts may manage 
            the cleaning process themselves.

            The type and age of buildings across arrondissements can also 
            impact cleanliness ratings. Central arrondissements, such as the 1st or 
            4th, are known for their historic and often older buildings. Despite their
             charm and appeal, these older buildings may present more challenges to
              maintain at a high standard of cleanliness due to their age and 
              architectural features. In contrast, newer buildings, which are more
              common in certain outer arrondissements, could be easier to keep clean
               and well-maintained
             """)
        elif ((review_type_choice == 'Location') or (review_type_choice == 'Value')):
            st.sidebar.info(
                """Some arrondissements, such as the 1st (Louvre) or the 4th (Marais), 
                are renowned for their historical significance, plethora of iconic 
                landmarks, and central location. 
                Therefore, these districts often receive high location ratings due to 
                their proximity to tourist attractions and easy accessibility to public 
                transportation.
                On the other hand, peripheral arrondissements like the 19th and 20th
                may not hold the same 
                touristic appeal, hence their lower location ratings. However,
                these districts often 
                offer better value for money. Here, accommodations are usually more 
                affordable and 
                spacious compared to the centrally located districts. Additionally, 
                these peripheral arrondissements provide an authentic experience of everyday
                Parisian
                life, away from the tourist crowds.""")
   

review_mapper = {'Rating':"review_scores_rating",
                'Cleanliness':"review_scores_cleanliness",
                'Check in':"review_scores_checkin",
                'Communication':"review_scores_communication",
                'Location':"review_scores_location",
                'Value':"review_scores_value"}

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
    if booking_choice == "Bookings per district" :
        st.image("images/density_neighbourhood.png")
    elif booking_choice=="Booking availability": 
        st.image("images/availability_neighbourhood.png")

elif dropdown_choice == 'Bookings':
    st.image("images/bookings_over_time.png")
    st.image("images/booking_2017.png")

elif dropdown_choice == 'Reviews':
    df_1 = pd.read_csv('data/listings_ext_first_half.csv')
    df_2 = pd.read_csv('data/listings_ext_second_half.csv')
    ext_listing = pd.concat([df_1, df_2])
    data = ext_listing.groupby('neighbourhood_cleansed')[review_mapper[review_type_choice]].median()
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

elif dropdown_choice == 'View some airbnbs':
    path_to_html = "Paris_Airbnb.html" 
    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()
    ## Show in webpage
    st.components.v1.html(html_data,height=1200)