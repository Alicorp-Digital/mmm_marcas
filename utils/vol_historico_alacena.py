import warnings
    
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
from st_pages import add_page_title, hide_pages

add_page_title(layout="wide")

st.markdown("#")

warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

data = pd.read_csv("data/dataset_mmm_modelo_alacena.csv")

fig_vol = go.Figure()

fig_vol.add_trace(go.Scatter(x=data["periodo"], y=data["venta_volumen"], mode='lines', name='Datos'))
fig_vol.update_layout(xaxis_title='semana',
                  yaxis_title='Volumen',
                     title='Volumen de ventas semanal')

st.plotly_chart(fig_vol, use_container_width=True)


fig_medios = go.Figure()

for var in data[['inv_EXTERIORES', 'inv_RADIO', 'inv_META',
             'inv_TIK TOK', 'inv_TV', 'inv_XAXIS',
             'inv_YOUTUBE']].columns[1:]:  # Omitir la primera columna que es la fecha
    fig_medios.add_trace(go.Scatter(
        x=data['periodo'],
        y=data[var],
        mode='lines',
        name=var
    ))

fig_medios.update_layout(
    title='Inversión en medios semanales',
    xaxis_title='semana',
    yaxis_title='Inversion',
    legend_title='Medios'
)

# Mostrar el gráfico en Streamlit
#st.title('Inversión en medios semanales')
st.plotly_chart(fig_medios, use_container_width=True)



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")