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

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

name = "model/budget_optimizer_model_mmm_bolivar_6.nc"
mmm = DelayedSaturatedMMM.load(name)

#st.header('Contribución acumulada')
get_mean_contributions_over_time_df = mmm.compute_mean_contributions_over_time(
    original_scale=True
)

contrib_grouped = get_mean_contributions_over_time_df.copy()
contrib_grouped['Baseline'] = contrib_grouped['dif_vol_lag3']+contrib_grouped['intercept']
contrib_grouped['IPC'] =  contrib_grouped['ipc_lima_var_12meses']+contrib_grouped['ipc_lima_var_mes']
contrib_grouped['Inversión en medios'] = contrib_grouped['inv_META']+contrib_grouped['inv_TIK TOK']+contrib_grouped['inv_TV']+contrib_grouped['inv_YOUTUBE']+contrib_grouped['inv_RADIO_TOTAL']
contrib_grouped['PBI'] = contrib_grouped['pbi_real_base_2007']
contrib_grouped['Tasa de desempleo'] = contrib_grouped['tasa_desempleo_lima_prom3meses_movil']
contrib_grouped['Cantidad de días festivos'] = contrib_grouped['num_dias_festivos']
contrib_grouped['Cantidad de días feriados'] = contrib_grouped['num_dias_feriados']
contrib_grouped['Precio de venta sugerido'] = contrib_grouped['pvpkilos_var_per_20_semanas']+contrib_grouped['pvpkilos_var_per_4_semanas']
contrib_grouped['Precio por kilo (Canal tradicional)'] = contrib_grouped['tradicional_var_per_ppk_OTROS']+contrib_grouped['tradicional_var_abs_ppk_INDUSTRIAS DEL ESPINO_var_per_12_semanas']+contrib_grouped['tradicional_var_abs_ppk_INDUSTRIAS DEL ESPINO_var_per_24_semanas']+contrib_grouped['tradicional_var_abs_ppk_INDUSTRIAS DEL ESPINO_var_per_8_semanas']+contrib_grouped['tradicional_var_per_ppk_OTROS_var_per_4_semanas']+contrib_grouped['tradicional_var_abs_ppk_INDUSTRIAS DEL ESPINO_var_per_4_semanas']+contrib_grouped['tradicional_var_abs_ppk_OTROS_var_per_16_semanas']
contrib_grouped['Precio por kilo (Canal moderno)'] = contrib_grouped['moderno_var_abs_ppk_OTROS_var_per_16_semanas']+contrib_grouped['moderno_var_abs_ppk_GRUPO_CALA']+contrib_grouped['moderno_var_abs_ppk_OTROS_var_per_8_semanas']+contrib_grouped['moderno_var_abs_ppk_GRUPO_CALA_var_per_8_semanas']
contrib_grouped['Crecimiento de marca (Canal tradicional)'] = contrib_grouped['tradicional_perc_ventas_alicorp_compe_soles_var_per_8_semanas']+contrib_grouped['tradicional_perc_ventas_alicorp_compe_soles_var_per_24_semanas']+contrib_grouped['tradicional_perc_ventas_alicorp_compe_soles_var_per_16_semanas']+contrib_grouped['tradicional_perc_ventas_alicorp_compe_soles_var_per_12_semanas']+contrib_grouped['tradicional_perc_ventas_alicorp_compe_kilos_var_per_4_semanas']
contrib_grouped['Crecimiento de marca (Canal moderno)'] = contrib_grouped['moderno_perc_ventas_alicorp_compe_kilos_var_per_4_semanas']
contrib_grouped['Inversión en promociones al consumidor final'] = contrib_grouped['inv_promociones_consumidor_moderno']+contrib_grouped['inv_promociones_consumidor_tradicional']
contrib_grouped.drop(get_mean_contributions_over_time_df.columns.to_list(), axis=1, inplace=True)


contrib_grouped_trn = pd.DataFrame(contrib_grouped.sum()).reset_index()
contrib_grouped_trn.columns = ['variable','contribucion_acum']

total_ventas = contrib_grouped_trn['contribucion_acum'].sum()

colors = ['green' if x >= 0 else 'orange' for x in contrib_grouped_trn['contribucion_acum']]
colors.append('gray')

fig, ax = plt.subplots(figsize=(16, 14))

ax.bar(contrib_grouped_trn['variable'].iloc[0], contrib_grouped_trn['contribucion_acum'].iloc[0], color=colors[0])

for i in range(1, len(contrib_grouped_trn)):
    start_value = contrib_grouped_trn['contribucion_acum'].cumsum().iloc[i-1]
    ax.bar(contrib_grouped_trn['variable'].iloc[i], contrib_grouped_trn['contribucion_acum'].iloc[i], bottom=start_value, color=colors[i])

ax.bar('Total', total_ventas, color='gray')

for i in range(len(contrib_grouped_trn)):
    y = contrib_grouped_trn['contribucion_acum'].cumsum().iloc[i]
    porcentaje = contrib_grouped_trn['contribucion_acum'].iloc[i] / total_ventas * 100
    ax.text(i, y, f'{porcentaje:.1f}%', ha='center', va='bottom' if contrib_grouped_trn['contribucion_acum'].iloc[i] >= 0 else 'top')

ax.text(len(contrib_grouped_trn), total_ventas, f'100%', ha='center', va='bottom')

#ax.set_title('Contribución acumulada por variable')
ax.set_xlabel('variable')
ax.set_ylabel('contribucion Acumulada')
plt.xticks(rotation=90)

st.pyplot(fig)



#fig_2 = st.pyplot(mmm.plot_waterfall_components_decomposition(figsize=(8, 5)))

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")