import streamlit as st 
from PIL import Image


#____________________ Page configuration


st.set_page_config(
    layout='centered',
    initial_sidebar_state='collapsed'
)
#____________________ Variables


image_path = 'BAM_logo.png'

#____________________ Functions
@st.cache_resource
def load_img(image_file):
    # Leer la imagen
    image = Image.open(image_file)    
    return image


#____________________ Body


st.divider()
st.divider()
st.divider()

st.image(load_img(image_path), use_column_width=True)

st.divider()
st.divider()
st.divider()

#_____________________ Side bar

with st.sidebar:
    st.divider()
    st.divider()
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
   
