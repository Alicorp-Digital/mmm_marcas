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
from pymc_marketing.mmm.budget_optimizer import calculate_expected_contribution

add_page_title(layout="wide")

st.markdown("#")

warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

name = "model/budget_optimizer_model_fin.nc"
mmm = DelayedSaturatedMMM.load(name)

data = pd.read_csv("data/data.csv")

st.header('Inversión total en medios')
fig1, ax = plt.subplots(figsize=(10, 5))
bars = data[["inversion_digital", "inversion_tv", "inversion_impresa"]].sum().plot(kind="barh", color=["C0", "C1", "C2"], ax=ax)

for bar in bars.patches:
    ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', 
            ha='left', va='center')

ax.set(title="Inversión total en medios", xlabel="Canal de medios", ylabel="Inversion (miles)");

st.pyplot(fig1);

channel_contribution_original_scale = mmm.compute_channel_contribution_original_scale()

roas_samples = (
    channel_contribution_original_scale.stack(sample=("chain", "draw")).sum("date")
    / data[["inversion_digital", "inversion_tv", "inversion_impresa"]].sum().to_numpy()[..., None]
)

fig, ax = plt.subplots(figsize=(14, 8))
sns.histplot(
    roas_samples.sel(channel="inversion_digital").to_numpy(),  color="C0", kde=True, ax=ax
)
sns.histplot(
    roas_samples.sel(channel="inversion_tv").to_numpy(), color="C1", kde=True, ax=ax
)
sns.histplot(
    roas_samples.sel(channel="inversion_impresa").to_numpy(), color="C2", kde=True, ax=ax
)

ax.axvline(x=roas_samples[0].median(), color="C0", linestyle="--", label=r"ROI estimado Canal Digital")
ax.axvline(x=roas_samples[1].median(), color="C1", linestyle="--", label=r"ROI estimado Canal TV")
ax.axvline(x=roas_samples[2].median(), color="C2", linestyle="--", label=r"ROI estimado Canal Impresa")
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
ax.set(title="Distribución ROI óptimo estimado", xlabel="ROI");

st.header('Distribución ROI óptimo estimado')
st.pyplot(fig);

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")