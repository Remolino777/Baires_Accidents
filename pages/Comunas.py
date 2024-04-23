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

#____________________________________________________Cordenadas Comuna

coordenadas_comuna = {
    1: [-34.60523, -58.35754],
    2: [-34.58495, -58.37903],
    3: [-34.61112, -58.39182],
    4: [-34.64023, -58.38288],
    5: [-34.61998, -58.40963],
    6: [-34.61998, -58.42950],
    7: [-34.63183, -58.43877],
    8: [-34.67562, -58.44980],
    9: [-34.65674, -58.48042],
    10: [-34.62835, -58.48864],
    11: [-34.60885, -58.48108],
    12: [-34.56193, -58.47701],
    13: [-34.55628, -58.44229],
    14: [-34.57522, -58.41168],
    15: [-34.59106, -58.44935]
}



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

# data_choro = df1.set_index('COMUNA')['Total victimas 2021'].to_dict()
# current_page = st.session_state.get('current_page', 'Map')
image_path = 'BAM_logo.png'
select_comuna = 0
#____________________________________________________________Side bar
with st.sidebar:
        select_comuna = st.selectbox('COMUNA',df1['COMUNA'].unique(), index=0, placeholder='Select...')
              
        st.divider()
        st.divider()        
        "---"
        "---"
        "---"
        "---"
        "---"        

        image = 'BAM_logo.png'
        st.image(load_img(image_path), use_column_width=True)

        st.caption(':grey[Observatorio de la Movilidad de la ciudad de Buenos Aires. Area de Siniestros -- Baires 2024 --]')
    


#____________________________________________________________Tasas



#_____________Tasa anual muertes x 100000 habitantes
dfc = df1[df1['COMUNA']==select_comuna]

 #m2021 = muertes por en moto por cada 100000 habitantes.
m2021 = ((dfc['Total victimas 2021'].sum())/(df1['Poblacion 2021'].iloc[0]))*100000
 #m2020 = muertes por en moto por cada 100000 habitantes.
m2020 = ((dfc['Total victimas 2020'].sum())/(df1['Poblacion 2020'].iloc[0]))*100000

m100 = round(m2021-m2020, 2)


#____________Tasa anual de accidentes mortales de motosicletas
#((accidentes_mortales_moto_anio_anterior - accidentes_mortales_moto_anio_actual)/ accidentes_mortales_moto_anio_anterior) * 100)
df_filtered_21 = df2[(df2['AAAA'] == 2021) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'MOTO')]
total_victimas_moto_2021 = df_filtered_21['N_VICTIMAS'].sum()

df_filtered_20 = df2[(df2['AAAA'] == 2020) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'MOTO')]
total_victimas_moto_2020 = df_filtered_20['N_VICTIMAS'].sum()

Tasa_moto = int(((total_victimas_moto_2020 - total_victimas_moto_2021)/total_victimas_moto_2020)*100)

#____________Tasa anual de accidentes mortales de PEATON
#((accidentes_mortales_moto_anio_anterior - accidentes_mortales_moto_anio_actual)/ accidentes_mortales_moto_anio_anterior) * 100)
df_filtered_21p = df2[(df2['AAAA'] == 2021) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'PEATON')]
total_victimas_pea_2021 = df_filtered_21p['N_VICTIMAS'].sum()

df_filtered_20p = df2[(df2['AAAA'] == 2020) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'PEATON')]
total_victimas_pea_2020 = df_filtered_20p['N_VICTIMAS'].sum()

Tasa_pea = int(((total_victimas_pea_2020 - total_victimas_pea_2021)/total_victimas_pea_2020)*100)

#____________________________________________________________Graficos
n1, n2, n3, n4= st.columns(4,gap='large')

with n1:
    st.write('Tasa Anual de Accidentes Mortales de Motosicleta')
    u1, u2= st.columns(2,gap='small')
    with u1:
        st.subheader(f"{Tasa_moto}%") 
    with u2:        
        if Tasa_moto >= 0:        
            st.image(load_img(a_up), use_column_width=True)
        else:
            st.image(load_img(a_down), use_column_width=True)
with n2:
    st.write('Tasa Anual de Accidentes Mortales de Peatones')
    u3, u4= st.columns(2,gap='small')
    with u3:
        st.subheader(f"{Tasa_pea}%")  
    with u4:        
        if Tasa_pea >= 0:        
            st.image(load_img(a_up), use_column_width=True)
        else:
            st.image(load_img(a_down), use_column_width=True)
with n3:
    st.write('Tasa anual Muertes X 100,000 habitantes')
    u5, u6= st.columns(2,gap='small')
    with u5:
        st.subheader(f"{m100}%") 
    with u6:
        if m100 >= 0:        
            st.image(load_img(a_up), use_column_width=True)
        else:
            st.image(load_img(a_down), use_column_width=True)
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
    m = folium.Map(location=coordenadas_comuna[select_comuna], 
                tiles='Esri_WorldGrayCanvas', 
                zoom_control=False, 
                zoom_start=13, 
                dragging=False,
                min_zoom=13,
                scrollWheelZoom=False,
                max_bounds=True, # Creation of map's limits.
                # min_lat = min_lat,
                # max_lat=max_lat,
                # min_lon=min_lon,
                # max_lon=max_lon                  
                )
    
    
    choropleth = folium.Choropleth(  # Pinto la comuna
        geo_data=df3[df3['COMUNAS'] == select_comuna],        
        fill_color="LightGreen",
        fill_opacity=0.25,
        line_opacity=0.5,        
        legend_name="Comuna : "
        
    ).add_to(m)
    
    
    marker_cluster = MarkerCluster().add_to(m)
    
    df_filtered1 = df2[df2['COMUNA']==select_comuna]
    
    dff2 = df_filtered1['N_VICTIMAS'][df2['AAAA'] == 2021]
    
    for i in dff2.index:
                lat = df_filtered1.loc[i, 'Latitud']
                long = df_filtered1.loc[i, 'Longitud']
                nombre = df_filtered1.loc[i, 'VICTIMA']
                folium.Marker(location=(lat, long),
                    popup=nombre,
                    tooltip=nombre
                    ).add_to(marker_cluster)
    
    
    
    
    
    
    st_data = st_folium(m, width=700, height=650)



#_____________________________________________________Grafico Barras

with n4:
    st.header(f'Comuna {select_comuna}')
    df_vic= df2[['AAAA','COMUNA','VICTIMA','N_VICTIMAS']]
    df_vic = df_vic[df_vic['AAAA'] == 2021]
    #df_vic = df_vic.drop('AAAA', axis=1)
    
    df_vic = df_vic[df_vic['COMUNA'] == select_comuna]
    df_vic = df_vic.groupby(['VICTIMA'])['N_VICTIMAS'].sum().reset_index()
    
    

    fig = px.bar(df_vic, x='N_VICTIMAS', y='VICTIMA', color='VICTIMA', 
                 labels={'N_VICTIMAS':'Numero de victimas', 'VICTIMA':'Tipo de victima'}
                 , width=300)

    # Ocultar la leyenda
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig)

        







