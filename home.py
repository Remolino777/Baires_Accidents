import streamlit as st 



#____________________ Page configuration


st.set_page_config(
    layout='wide',
    initial_sidebar_state='auto'
)
#____________________ Variables

img_path = "BAM_logo.png"

    
#____________________Loading Data





#____________________ Functions


cl1, cl2, cl3, = st.columns([1,4,1])

#____________________ Body

st.divider()
st.divider()
st.divider()

st.image(img_path, use_column_width=True)

st.divider()
st.divider()
st.divider()

#_____________________ Side bar

with st.sidebar:
    st.divider()
    st.divider()
    
    "---"
    "---"
    "---"
    "---"
    "---"
    

    image = 'BAM_logo.png'
    st.image(img_path, use_column_width=True)

    st.caption(':grey[Observatorio de la Mobilidad de la ciudad de Buenos Aires. Area de Siniestros -- Baires 2024 --]')
   
