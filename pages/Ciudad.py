import pandas as pd
import geopandas as gpd
import streamlit as st 
import folium
from streamlit_folium import st_folium, folium_static
import plotly.express as px


#____________________ Page configuration


st.set_page_config(
    layout='wide',
    initial_sidebar_state='auto'
)

#_____________________ Source dataset reading.
data_1 = "siniestros_por_comuna.parquet"  ### Siniestros por comuna
data_2 =  "siniestros.parquet"  ### Siniestros por tipo
data_3 = "comunas.geojson"  ### Geodata




a_down = "Arrow_down.png"
a_up = "Arrow_up.png"

#____________________ Functions


@st.cache_data   #cache the csv file
def load_data(parquet_file_path):
    df = pd.read_parquet(parquet_file_path)
    return df

@st.cache_data   #cache the csv file
def load_geoData(geo_file_path):
    df = gpd.read_file(geo_file_path)
    return df




df1 = load_data(data_1)
df2 = load_data(data_2)
df3 = load_geoData(data_3)


#__________________________________________ Global varibles  #########

data_choro = df1.set_index('COMUNA')['Total victimas 2021'].to_dict()

image = 'BAM_logo.png'

#____________________________________________Tasa de accidentes anuales
#____________Tasa anual de accidentes mortales 
#((accidentes_mortales_moto_anio_anterior - accidentes_mortales_moto_anio_actual)/ accidentes_mortales_moto_anio_anterior) * 100)
df_filtered_21 = df2[df2['AAAA'] == 2021]
total_victimas_2021 = df_filtered_21['N_VICTIMAS'].sum()

df_filtered_20 = df2[df2['AAAA'] == 2020]
total_victimas_2020 = df_filtered_20['N_VICTIMAS'].sum()


total_v = (total_victimas_2021 - total_victimas_2020)  
   
tasa_total_victimas = round(((total_v/total_victimas_2020)*100), 0)


#_______________________________Muertes x 100000 habitantes  #########

#m2021 = muertes por cada 100000 habitantes.
m2021 = int(((df1['Total victimas 2021'].sum())/(df1['Poblacion 2021'].iloc[0]))*100000)

#m2021 = muertes por cada 100000 habitantes.
m2020 = int(((df1['Total victimas 2020'].sum())/(df1['Poblacion 2020'].iloc[0]))*100000)

#Variacionde mortalidad cada 100000 habitantes  
m100 = m2021-m2020

poblacion_2021 = df1['Poblacion 2021'].sum()







#_______________________ Columns

n1, n2 = st.columns([3,1], gap='small')

with n1:    #_______________________ Map
    st.subheader('Siniestros en la ciudad de Buenos Aires en el año 2021')
    m = folium.Map(location=[-34.60777, -58.43210], 
                tiles='Esri_WorldGrayCanvas', 
                zoom_control=False, 
                zoom_start=12, 
                dragging=False,
                min_zoom=12,
                scrollWheelZoom=False,
                max_bounds=True, # Creation of map's limits.
                # min_lat = min_lat,
                # max_lat=max_lat,
                # min_lon=min_lon,
                # max_lon=max_lon                  
                )


    choropleth = folium.Choropleth(
        geo_data=data_3,
        data=data_choro,
        columns=['COMUNA','Total victimas 2021'],
        key_on='feature.properties.COMUNAS',
        fill_color="YlGn",
        fill_opacity=0.5,
        line_opacity=0.2,
        bins=[0, 3, 6, 9, 12],
        legend_name="Cantidad de muertes por accidente de transito",
        highlight=True
    ).add_to(m)
    
    # Mostrar nombre de comuna
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['COMUNAS'],
                                       aliases=["Comuna :"])
    )
    

    

    st_data = st_folium(m, width=700, height=800)
    
with n2:
    st.title('Datos')
    st.write('Tasa de accidentes anuales')
    col1, col2 = st.columns([1,2], gap='large')
    with col1:
        st.subheader(f'{tasa_total_victimas}%')
    with col2:
        st.image(a_up, use_column_width=True)
    '---'  
    
    st.write('Muertes X 100,000 habitantes')
    st.subheader(m2021)     #m2021 = muertes por cada 100000 habitantes.
    '---'  
    
    st.write('Variacion anual Muertes X 100,000 habitantes')
    col3, col4 = st.columns([1,2], gap='large')    
    with col3:
        st.subheader(m100)      #Variacionde mortalidad cada 100000 habitantes 
    with col4:
        st.image(a_up, use_column_width=True)
    '---'  
    
    st.write('Poblacion Ciudad de Buenos Aires')
    st.subheader(f'{poblacion_2021}  habitantes')     
    
    with st.sidebar:
        st.divider()
        st.divider()
        st.divider()
        st.divider()
        "---"
        "---"
        "---"
        
        

        
        st.image(image, use_column_width=True)

        st.caption(':grey[Observatorio de la Mobilidad de la ciudad de Buenos Aires. Area de Siniestros -- Baires 2024 --]')
    