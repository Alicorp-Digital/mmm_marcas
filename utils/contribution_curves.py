import warnings
    
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import seaborn as sns
import streamlit as st
from st_pages import add_page_title, hide_pages
    
from pymc_marketing.mmm.delayed_saturated_mmm import DelayedSaturatedMMM

add_page_title(layout="wide")

st.markdown("#")

warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")
plt.rcParams["figure.figsize"] = [14, 12]
plt.rcParams["figure.dpi"] = 100

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

name = "model/budget_optimizer_model_fin.nc"
mmm = DelayedSaturatedMMM.load(name)

sigmoid_params = mmm.compute_channel_curve_optimization_parameters_original_scale(
    method="michaelis-menten"
)

#st.pyplot(mmm.plot_channel_contributions_grid(start=0, stop=1.5, num=12));
st.header('Inversión Digital')
st.write('Punto de saturación de inversión: 20000')
st.write(f"Contribución óptima: {round(sigmoid_params['inversion_digital'][0], 2)}")
st.pyplot(mmm.plot_direct_contribution_curves(
    show_fit=True, xlim_max=30000, method="michaelis-menten", channels=['inversion_digital']
));

st.header('Inversión Television')
st.write('Punto de saturación de inversión: 25000')
st.write(f"Contribución óptima: {round(sigmoid_params['inversion_tv'][0], 2)} ")
st.pyplot(mmm.plot_direct_contribution_curves(
    show_fit=True, xlim_max=30000, method="michaelis-menten", channels=['inversion_tv']
));

st.header('Inversión Impresa')
st.write('Punto de saturación de inversión: 18000')
st.write(f"Contribución óptima: {round(sigmoid_params['inversion_impresa'][0], 2)} ")
st.pyplot(mmm.plot_direct_contribution_curves(
    show_fit=True, xlim_max=30000, method="michaelis-menten", channels=['inversion_impresa']
));

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")