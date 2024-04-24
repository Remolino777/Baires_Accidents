import pandas as pd
import streamlit as st 
import plotly.graph_objects as go
from PIL import Image


#____________________ Page configuration

st.set_page_config(
    layout='centered',
    initial_sidebar_state='auto'
)

#_____________________ Source dataset reading.
data_1 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\ETL\siniestros_por_comuna.parquet"  ### Siniestros por comuna
data_2 =  r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\Parquet\victimas_semestre.parquet"  ### Siniestros por tipo Semestre
data_3 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\Parquet\poblacion.parquet"  #Poblacion
data_4 = r"D:\0_Respaldo\0_Proyectos_2024\Henry_Labs\Lab2\Baires_Accidents\Data\Parquet\comisarias.parquet"  #Comisarias
a_down = "Arrow_down.png"
a_up = "Arrow_up.png"
image_path = 'BAM_logo.png'
#____________________ Functions


@st.cache_data   #cache the csv file
def load_data(parquet_file_path):
    df = pd.read_parquet(parquet_file_path)
    return df


@st.cache_resource
def load_img(image_file):
    # Leer la imagen
    image = Image.open(image_file)    
    return image


df1 = load_data(data_1)
df2 = load_data(data_2)
dfp = load_data(data_3)
dfc = load_data(data_4) #comisarias
#_______________________________________CALCULOS

#____________Tasa  de accidentes mortales motociclistas 2021.
df2_filtrado_21 = df2[(df2['AAAA'] == 2021) & (df2['VICTIMA'] == 'MOTO')]
#total victimas (tv)  semestre(s)
tv_2021 = df2_filtrado_21['N_VICTIMAS'].sum()

df2_filtrado_20 = df2[(df2['AAAA'] == 2020) & (df2['VICTIMA'] == 'MOTO')]
tv_2020 = df2_filtrado_20['N_VICTIMAS'].sum()

if tv_2020 == 0:
    tasa_moto = tv_2021*100
else:    
    #Manejar valor de cero
    tv_moto = (tv_2021 - tv_2020)

    if tv_moto == 0:
        tasa_moto = 0
    else:
        tasa_moto = (tv_moto/tv_2020)*100
        
        
#____________Calculo para grafica de barras TAA 2021      ###### fig2
# Total victimas (tv)
tv_comuna = df2_filtrado_21.groupby('COMUNA')['N_VICTIMAS'].sum().reset_index()


#____________Tasa  de accidentes mortales 2021.   ### fig 3

poblacion_2021 = dfp['2021'][0]
poblacion_2020 = dfp['2020'][0]

e2_filtrado_21 = df2[(df2['AAAA'] == 2021) & (df2['MM'] >=7)]
#total victimas (tv)  semestre(s)
tv_pea_2021 = e2_filtrado_21['N_VICTIMAS'].sum()

p_21 =  tv_pea_2021/poblacion_2021*100000


e2_filtrado_20 = df2[(df2['AAAA'] == 2020) & (df2['MM'] < 7)]
tv_pea_2020 = e2_filtrado_20['N_VICTIMAS'].sum()

p_20 =  tv_pea_2020/poblacion_2020*100000

tv_semestre = round((p_21 - p_20),2)


#____________Calculo para grafica de barras TAA 2021      ###### fig4
# Total victimas (tv)
tv_comuna_2 = e2_filtrado_21.groupby('COMUNA')['N_VICTIMAS'].sum().reset_index()


#____________Tasa  COMISARIAS 2021.   ### fig 5

dc_filtrado = dfc['nombre'].count()
#total victimas (tv)  semestre(s)


c_21 =  dc_filtrado/tv_pea_2021
c_20 =  dc_filtrado/tv_pea_2020


t_com = round((c_21 - c_20)/c_20,2)


#____________Calculo comisarias TAA 2021      ###### fig6
# Total victimas (tv)
co_comuna = dfc.groupby('COMUNA')['nombre'].count().reset_index()



#______________________________________TABS
tab1, tab2, tab3 = st.tabs(["TA SEMESTRE 2021","TA MOTOCICLISTAS 2021",  "TA COMISARIAS"])

with tab2:    
    #___________________________________________________Graficas
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = tasa_moto,
        mode = "gauge+number+delta",
        title = {'text': "Tasa de accidentes anuales motocicletas 2021"},
        delta = {'reference': tasa_moto},
        number={'suffix': '%'},
        gauge = {'axis': {'range': [None, tasa_moto]},
                'steps' : [
                    {'range': [0, 7], 'color': "lightgreen"},
                    {'range': [7, tasa_moto], 'color': "lightpink"}],
                'threshold' : {'line': {'color': "red", 'width': 10}, 'thickness': 0.75, 'value': 7}}))

    #________________fig1  ##### Barras    
    
    
    fig1 = go.Figure([go.Bar(x=tv_comuna['COMUNA'], y=tv_comuna['N_VICTIMAS'], marker_color='mediumaquamarine')])

    fig1.update_layout(title='Total de Víctimas Mortales Motocicletas por Comuna en el Año 2021',
                    xaxis_title='Comuna',
                    yaxis_title='Total de Víctimas',
                    height=300)       
    
    st.plotly_chart(fig)
    st.plotly_chart(fig1)
   
 
with tab1:
    
   #___________________________________________________Graficas
    fig3 = go.Figure(go.Indicator(                               ######## 100,000
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = tv_semestre,
        mode = "gauge+number",
        title = {'text': "Siniestros viales por cada 100,000 habitantes segundo semestre del 2021"},
        delta = {'reference': p_21},
        #number={'suffix': '%'},
        gauge = {'axis': {'range': [None, p_20]},
                'steps' : [
                    {'range': [0, p_20], 'color': "lightgreen"},
                    {'range': [p_20, tv_semestre], 'color': "lightpink"}],
                'threshold' : {'line': {'color': "red", 'width': 10}, 'thickness': 0.75, 'value': p_20}}))

    #_______________Barras 2
    fig4 = go.Figure([go.Bar(x=tv_comuna_2['COMUNA'], y=tv_comuna_2['N_VICTIMAS'], marker_color='mediumaquamarine')])

    fig4.update_layout(title='Total de Víctimas Mortales por Comuna del segundo semestre del Año 2021',
                    xaxis_title='Comuna',
                    yaxis_title='Total de Víctimas',
                    height=300) 





    st.plotly_chart(fig3)
    st.plotly_chart(fig4)

with tab3:
    
    
    print(c_20)
    print(c_21)
    print(t_com)
    fig5 = go.Figure(go.Indicator(                    ######COMISARIA
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = t_com,
        mode = "gauge+number+delta",
        title = {'text': "Tasa anual de comisarias por total de siniestros en el 2021"},
        delta = {'reference': c_21},
        #number={'suffix': '%'},
        gauge = {'axis': {'range': [None, c_20]},
                'steps' : [
                    {'range': [0, c_21], 'color': "lightgreen"},
                    {'range': [c_21, t_com], 'color': "lightpink"}],
                'threshold' : {'line': {'color': "red", 'width': 10}, 'thickness': 0.75, 'value': c_20}}))

    #_______________Barras 2
    fig6= go.Figure([go.Bar(x=co_comuna['COMUNA'], y=co_comuna['nombre'], marker_color='mediumaquamarine')])

    fig6.update_layout(title='Total Comisarias por comuna del Año 2021',
                    xaxis_title='Comuna',
                    yaxis_title='Total de Comisarias',
                    height=300) 
    
    st.plotly_chart(fig5)
    st.plotly_chart(fig6)
   
with st.sidebar:
    st.divider()
    st.divider()
    st.divider()
    st.divider()
    
    "---"
    "---"
    "---"
    "---"
    

    image = 'BAM_logo.png'
    st.image(load_img(image_path), use_column_width=True)

    st.caption(':grey[Observatorio de la Mobilidad de la ciudad de Buenos Aires. Area de Siniestros -- Baires 2024 --]')
