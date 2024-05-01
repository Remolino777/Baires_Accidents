import pandas as pd
import geopandas as gpd
import streamlit as st 
import plotly.express as px
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import MarkerCluster
import math
#____________________ Page configuration

image = "BAM_logo.png"

st.set_page_config(
    layout='wide',
    initial_sidebar_state='auto'
)


#_____________________ Source dataset reading.
data_1 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\ETL\siniestros_por_comuna.parquet"  ### Siniestros por comuna
data_2 =  r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\ETL\siniestros.parquet"  ### Siniestros por tipo
data_3 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\comunas.geojson"  ### Geodata
data_4 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\Parquet\comisarias.parquet"
a_down = "Arrow_down.png"
a_up = "Arrow_up.png"
equal = "Equal.png"

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



df1 = load_data(data_1)
df2 = load_data(data_2)
df3 = load_geoData(data_3)
df4 = load_data(data_4)    #Comisarias


#__________________________________________ Global varibles  #########

# data_choro = df1.set_index('COMUNA')['Total victimas 2021'].to_dict()
# current_page = st.session_state.get('current_page', 'Map')
imag = 'BAM_logo.png'
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
            

        
        st.image(image, use_column_width=True)

        st.caption(':grey[Observatorio de la Movilidad de la ciudad de Buenos Aires. Area de Siniestros -- Baires 2024 --]')
    


#____________________________________________________________Tasas



#_____________Muertes x 100000 habitantes
dfc = df1[df1['COMUNA']==select_comuna]

 #m2021 = muertes por en moto por cada 100000 habitantes.
m2021 = ((dfc['Total victimas 2021'].sum())/(dfc['Poblacion 2021'].sum()))*100000
 #m2020 = muertes por en moto por cada 100000 habitantes.
m2020 = ((dfc['Total victimas 2020'].sum())/(dfc['Poblacion 2020'].sum()))*100000

m100 = m2021-m2020

if m100 >= 0:
    m100 = math.ceil(m100) #Redondeo a entero superior
else:
    m100 = math.floor(m100)   #Redondeo a entero inferior



#____________Tasa anual de accidentes mortales de motosicletas
#((accidentes_mortales_moto_anio_anterior - accidentes_mortales_moto_anio_actual)/ accidentes_mortales_moto_anio_anterior) * 100)
df_filtered_21 = df2[(df2['AAAA'] == 2021) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'MOTO')]
total_victimas_moto_2021 = df_filtered_21['N_VICTIMAS'].sum()

df_filtered_20 = df2[(df2['AAAA'] == 2020) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'MOTO')]
total_victimas_moto_2020 = df_filtered_20['N_VICTIMAS'].sum()

if total_victimas_moto_2020 == 0:
    tasa_moto = total_victimas_moto_2021*100
else:    
    #Manejar valor de cero
    tv_moto = (total_victimas_moto_2020 - total_victimas_moto_2021)

    if tv_moto == 0:
        tasa_moto = 0
    else:
        tasa_moto = round(((tv_moto/total_victimas_moto_2020)*100), 0)

#____________Tasa anual de accidentes mortales de PEATON
#((accidentes_mortales_moto_anio_anterior - accidentes_mortales_moto_anio_actual)/ accidentes_mortales_moto_anio_anterior) * 100)
df_filtered_21p = df2[(df2['AAAA'] == 2021) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'PEATON')]
total_victimas_pea_2021 = df_filtered_21p['N_VICTIMAS'].sum()

df_filtered_20p = df2[(df2['AAAA'] == 2020) & (df2['COMUNA'] == select_comuna) & (df2['VICTIMA'] == 'PEATON')]
total_victimas_pea_2020 = df_filtered_20p['N_VICTIMAS'].sum()

#Manejar valor de cero
if total_victimas_pea_2020 == 0:
    tasa_pea = total_victimas_pea_2021*100
else:    
    #Manejar valor de cero
    tv_pea = (total_victimas_pea_2020 - total_victimas_pea_2021)

    if tv_pea == 0:
        tasa_pea = 0
    else:
        tasa_pea = round(((tv_pea/total_victimas_pea_2020)*100), 0)


#_____________Comisarias x 100000 habitantes
df4_filtrado = df4[df4['COMUNA']== select_comuna]

 #m2021 = muertes por en moto por cada 100000 habitantes.
com100 = round((((df4_filtrado['nombre'].count())/(dfc['Poblacion 2021'].sum()))*100000), 2)




#____________________________________________________________Graficos
n1, n2, n3, n4= st.columns(4,gap='large')

with n1:
    st.write('Tasa Anual de Accidentes Mortales de Motosicletas')
    u1, u2= st.columns(2,gap='small')
    with u1:
        st.subheader(f"{tasa_moto}%") 
    with u2:        
        if tasa_moto > 0:        
            st.image(a_up, use_column_width=True)
        elif tasa_moto == 0:        
            st.image(equal, use_column_width=True)
        else:
            st.image(a_down, use_column_width=True)
with n2:
    st.write('Tasa Anual de Accidentes Mortales de Peatones')
    u3, u4= st.columns(2,gap='small')
    with u3:
        st.subheader(f"{tasa_pea}%")  
    with u4:        
        if tasa_pea > 0:        
            st.image(a_up, use_column_width=True)
        elif tasa_pea == 0:        
            st.image(equal, use_column_width=True)
        else:
            st.image(a_down, use_column_width=True)
with n3:
    st.write(f'Muertes anuales X 100,000 habitantes comuna:{select_comuna}')
    u5, u6= st.columns(2,gap='small')
    with u5:
        st.subheader(m100)         
    with u6:
        if m100 >= 0:        
            st.image(a_up, use_column_width=True)
        else:
            st.image(a_down, use_column_width=True)
with n4:
    st.write('Comisarias X 100000 habitantes')
    u7, u8= st.columns(2,gap='small')
    with u7:
        st.subheader(com100) 
    with u8:        
        st.image(equal, use_column_width=True)
        
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
    
    
    marker_cluster_1 = MarkerCluster().add_to(m)
    marker_cluster_2 = MarkerCluster().add_to(m)
    
    
    
    
    df_filtered1 = df2[df2['COMUNA']==select_comuna]            ##### ACCIDENTES
    
    dff2 = df_filtered1['N_VICTIMAS'][df2['AAAA'] == 2021]
    
    for i in dff2.index:
                lat = df_filtered1.loc[i, 'Latitud']
                long = df_filtered1.loc[i, 'Longitud']
                nombre = df_filtered1.loc[i, 'VICTIMA']
                folium.Marker(location=(lat, long),
                    popup=nombre,
                    icon=folium.Icon(color='red'),
                    tooltip=nombre
                    ).add_to(marker_cluster_1)
                
                                                                     ##### COMISARIAS
    df_filtered_comisarias = df4[df4['COMUNA'] == select_comuna]
    
    
    for i, row in df_filtered_comisarias.iterrows():
        lat = row['Latitud']
        long = row['Longitud']
        nombre = row['nombre']
        folium.Marker(location=(lat, long),
                    popup=nombre,
                    tooltip=nombre,                    
                    icon=folium.Icon(color='blue')
                    ).add_to(marker_cluster_2)
    
    
    
    
    
    
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

        







