import pandas as pd
import streamlit as st 
import plotly.graph_objects as go



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




df1 = load_data(data_1)
df2 = load_data(data_2)
dfp = load_data(data_3)
dfc = load_data(data_4) #comisarias
#_______________________________________CALCULOS

#____________Tasa  de accidentes mortales motociclistas 2021.
df2_filtrado_21 = df2[(df2['AAAA'] == 2021) & (df2['VICTIMA'] == 'MOTO')]
df2_filtrado_p = df2[(df2['AAAA'] == 2021) & (df2['VICTIMA'] == 'PEATON')]
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
tv_comuna = df2_filtrado_21.groupby('COMUNA')['N_VICTIMAS'].sum().reset_index()   # Moto
tv2_comuna = df2_filtrado_p.groupby('COMUNA')['N_VICTIMAS'].sum().reset_index()  # Peaton

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


#____________Tasa  Peatones 2021.   ### fig 6

df3_filtrado_21 = df2[(df2['AAAA'] == 2021) & (df2['VICTIMA'] == 'PEATON')]
#total victimas (tv)  semestre(s)
tv2_2021 = df2_filtrado_21['N_VICTIMAS'].sum()

df3_filtrado_20 = df2[(df2['AAAA'] == 2020) & (df2['VICTIMA'] == 'PEATON')]
tv2_2020 = df3_filtrado_20['N_VICTIMAS'].sum()

if tv2_2020 == 0:
    tasa_pea = tv_2021*100
else:    
    #Manejar valor de cero
    tv_pea = (tv2_2021 - tv2_2020)

    if tv_pea == 0:
        tasa_pea = 0
    else:
        tasa_pea = (tv_pea/tv_2020)*100



#______________________________________TABS
tab1, tab2, tab3 = st.tabs(["TA SEMESTRE 2021","TA MOTOCICLISTAS 2021",  "TA PEATONES 2021"])

with tab2:    
    #___________________________________________________Graficas
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = tasa_moto,
        mode = "gauge+number+delta",
        title = {'text': "Tasa de accidentes anuales motocicletas 2021"},
        delta = {'reference': tv_2021},
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
    
    
    fig5 = go.Figure(go.Indicator(                    ######PEATON    ######PEATON
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = tasa_pea,
        mode = "gauge+number+delta",
        title = {'text': "Tasa de accidentes anuales peatones 2021"},
        delta = {'reference': tv2_2021},
        number={'suffix': '%'},
        gauge = {'axis': {'range': [None, tv2_2021]},
                'steps' : [
                    {'range': [0, tv2_2020], 'color': "lightgreen"},
                    {'range': [tv2_2020, tasa_pea], 'color': "lightpink"}],
                'threshold' : {'line': {'color': "red", 'width': 10}, 'thickness': 0.75, 'value': tv2_2020}}))

    #_______________Barras 2
    fig6 = go.Figure([go.Bar(x=tv2_comuna['COMUNA'], y=tv2_comuna['N_VICTIMAS'], marker_color='mediumaquamarine')])

    fig6.update_layout(title='Total de Víctimas Mortales Peaton por Comuna en el Año 2021',
                    xaxis_title='Comuna',
                    yaxis_title='Total de Víctimas',
                    height=300)       
    
    st.plotly_chart(fig5)
    st.plotly_chart(fig6)
   
with st.sidebar:
    st.divider()
    st.divider()
    
    
    
    "---"
    "---"
    "---"
    "---"
    

    image = 'BAM_logo.png'
    st.image(image, use_column_width=True)

    st.caption(':grey[Observatorio de la Mobilidad de la ciudad de Buenos Aires. Area de Siniestros -- Baires 2024 --]')
