import pandas as pd
import geopandas as gpd
import streamlit as st 
import plotly.express as px
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import MarkerCluster
from PIL import Image

#____________________ Page configuration


st.set_page_config(
    layout='wide',
    initial_sidebar_state='auto'
)


#_____________________ Source dataset reading.
data_1 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\ETL\siniestros_por_comuna.parquet"  ### Siniestros por comuna
data_2 =  r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\ETL\siniestros.parquet"  ### Siniestros por tipo
data_3 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\comunas.geojson"  ### Geodata

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

@st.cache_resource
def load_img(image_file):
    # Leer la imagen
    image = Image.open(image_file)    
    return image


df1 = load_data(data_1)
df2 = load_data(data_2)
df3 = load_geoData(data_3)


#__________________________________________ Global varibles  #########

data_choro = df1.set_index('COMUNA')['Total victimas 2021'].to_dict()
current_page = st.session_state.get('current_page', 'Map')
image_path = 'BAM_logo.png'




#____________________________________________________________Tazas
n1, n2, n3, n4= st.columns(4,gap='large')

with n1:
    st.write('Taza Anual de Accidentes Mortales de Motosicleta')
    u1, u2= st.columns(2,gap='small')
    with u1:
        st.subheader("23.07%") 
    with u2:        
        st.image(load_img(a_up), use_column_width=True)
with n2:
    st.write('Taza Anual de Accidentes Mortales de Peatones')
    u3, u4= st.columns(2,gap='small')
    with u3:
        st.subheader("23.07%") 
    with u4:        
        st.image(load_img(a_up), use_column_width=True)
with n3:
    st.write('Variacion anual Muertes X 100,000 habitantes')
    u5, u6= st.columns(2,gap='small')
    with u5:
        st.subheader("23.07%") 
    with u6:        
        st.image(load_img(a_up), use_column_width=True)
with n4:
    st.write('Comisarias X 100000 habitantes')
    u7, u8= st.columns(2,gap='small')
    with u7:
        st.subheader("23.07%") 
    with u8:        
        st.image(load_img(a_up), use_column_width=True)
        
'---'  
#____________________________________________________________Mapa
n3, n4 = st.columns([3,2], gap='large')

with n3:
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
    
    st_data = st_folium(m, width=700, height=650)

with n4:
    
    df_vic= df2[['AAAA','COMUNA','VICTIMA','N_VICTIMAS']]
    df_vic = df_vic[df_vic['AAAA'] == 2021]
    df_vic = df_vic.drop('AAAA', axis=1)

    df_vic = df_vic.groupby(['COMUNA','VICTIMA'])['N_VICTIMAS'].sum().reset_index()

    df_comunas = df_vic[df_vic['COMUNA'] == 1]
    df_grouped = df_comunas.groupby('VICTIMA')['N_VICTIMAS'].sum().reset_index()

    fig = px.bar(df_grouped, x='N_VICTIMAS', y='VICTIMA', color='VICTIMA', 
                 labels={'N_VICTIMAS':'Numero de victimas', 'VICTIMA':'Tipo de victima'}
                 , width=300)

    # Ocultar la leyenda
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig)

        

#____________________  barras





#____________________________________________________________Side bar
with st.sidebar:
        select_comuna = st.selectbox('COMUNA',df1['COMUNA'].unique(), index=None, placeholder='Select...')
        st.divider()
        st.divider()        
        "---"
        "---"
        "---"
        "---"
        "---"
        

        image = 'BAM_logo.png'
        st.image(load_img(image_path), use_column_width=True)

        st.caption(':grey[Observatorio de la Mobilidad de la ciudad de Buenos Aires. Area de Siniestros -- Baires 2024 --]')
    