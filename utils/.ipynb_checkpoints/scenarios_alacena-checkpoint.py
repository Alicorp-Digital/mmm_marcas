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
    
from pymc_marketing.mmm.delayed_saturated_mmm import DelayedSaturatedMMM
from pymc_marketing.mmm.budget_optimizer import calculate_expected_contribution

add_page_title(layout="wide")

st.markdown("#")

warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

name_bolivar = "model/budget_optimizer_model_mmm_alacena_5.nc"
mmm_bolivar = DelayedSaturatedMMM.load(name_bolivar)

menten_params = mmm_bolivar.compute_channel_curve_optimization_parameters_original_scale(
    method="michaelis-menten"
)

total_budget = st.number_input("Ingrese el presupuesto total en medios:", 
                               min_value=0)

channels = [
    'inv_EXTERIORES', 'inv_RADIO', 'inv_META',
             'inv_TIK TOK', 'inv_TV', 'inv_XAXIS',
             'inv_YOUTUBE'
]

# Ingresar los otros 3 valores
col1, col2, col3, col4 = st.columns(4)
with col1:
    budget_per_meta = st.number_input("Presupuesto Via Publica:", min_value=0, max_value=total_budget, key=None)
with col2:
    budget_per_tiktok = st.number_input("Presupuesto Radio:", min_value=0, max_value=total_budget, key=None)
with col3:
    budget_per_tv = st.number_input("Presupuesto Meta:", min_value=0, max_value=total_budget, key=None)
with col4:
    budget_per_youtube = st.number_input("Presupuesto TikTok:", min_value=0, max_value=total_budget, key=None)

col5, col6, col7 = st.columns(3)
with col5:
    budget_per_radio= st.number_input("Presupuesto Televisión:", min_value=0, max_value=total_budget, key=None)
with col6:
    budget_per_prom_consumidor_moderno = st.number_input("Presupuesto XAXIS:", min_value=0, max_value=total_budget, key=None)
with col7:
    budget_per_prom_consumidor_tradicional = st.number_input("Presupuesto YouTube:", min_value=0, max_value=total_budget, key=None)

suma_valores = budget_per_meta+budget_per_tiktok+budget_per_tv+budget_per_youtube+budget_per_radio+budget_per_prom_consumidor_moderno+budget_per_prom_consumidor_tradicional

initial_budget_dict = {'inv_EXTERIORES':budget_per_meta,
             'inv_RADIO':budget_per_tiktok,
             'inv_META':budget_per_tv,
             'inv_TIK TOK':budget_per_youtube,
             'inv_TV':budget_per_radio,
             'inv_XAXIS':budget_per_prom_consumidor_moderno,
             'inv_YOUTUBE':budget_per_prom_consumidor_tradicional}

initial_contribution = calculate_expected_contribution(
        method="michaelis-menten", parameters= menten_params, budget= initial_budget_dict
    )
    
initial_scenario = {
        "initial_contribution": initial_contribution,
        "initial_budget": initial_budget_dict,
    }

platform_base_optimization = mmm_bolivar.optimize_channel_budget_for_maximum_contribution(
        method="michaelis-menten",
        total_budget=total_budget,
        parameters=menten_params,
        budget_bounds={'inv_EXTERIORES':[0,total_budget],
                     'inv_RADIO':[0,total_budget],
                     'inv_META':[0,total_budget],
                     'inv_TIK TOK':[0,total_budget],
                     'inv_TV':[0,total_budget],
                     'inv_XAXIS':[0,total_budget],
                     'inv_YOUTUBE':[0,total_budget]}
                            )

# Comprobar si la suma supera el valor límite
if suma_valores > total_budget:
    st.error("No puede ingresar valores que superen el valor máximo de presupuesto.")
else:
    st.success("Los valores son válidos y no superan el límite de presupuesto.")
    cols, colt = st.columns(2)
    with cols:
        st.write(f"Tu presupuesto en medios es: {suma_valores} S/")
    with colt:
        st.write(f"Te quedan por agregar: {total_budget-suma_valores} S/")

    st.write("Escenario de contribuciones ajustado a tu presupuesto")
    st.pyplot(mmm_bolivar.plot_budget_scenearios(
        base_data=initial_scenario, method="michaelis-menten", scenarios_data=[platform_base_optimization]
    ));
        
    st.write(f"Recomendación de presupuesto óptimo y contribución esperada según tu presupuesto total")
    platform_base_optimization.columns = ['contribución estimada', 'inversión óptima']
    st.dataframe(platform_base_optimization);  
    
    # cola, colb = st.columns(2)
    # with cola:
    #     fig_opt_con = go.Figure(go.Bar(
    #         x=[round(platform_base_optimization['contribución estimada'][0], 2), 
    #            round(platform_base_optimization['contribución estimada'][1], 2),
    #            round(platform_base_optimization['contribución estimada'][2], 2), 
    #            round(platform_base_optimization['contribución estimada'][3], 2), 
    #            round(platform_base_optimization['contribución estimada'][4], 2),
    #            round(platform_base_optimization['contribución estimada'][5], 2), 
    #            round(platform_base_optimization['contribución estimada'][6], 2)],
    #         y=channels,
    #         orientation='h',
    #         marker=dict(color='#76D7C4'),
    #         text=[round(platform_base_optimization['contribución estimada'][0], 2), 
    #               round(platform_base_optimization['contribución estimada'][1], 2),
    #               round(platform_base_optimization['contribución estimada'][2], 2), 
    #               round(platform_base_optimization['contribución estimada'][3], 2), 
    #               round(platform_base_optimization['contribución estimada'][4], 2),
    #               round(platform_base_optimization['contribución estimada'][5], 2), 
    #               round(platform_base_optimization['contribución estimada'][6], 2)], 
    #         textposition='auto'
    #         ))
            
    #     fig_opt_con.update_layout(
    #             title='Valores óptimos de contribución por semana',
    #             xaxis_title='Contribución',
    #             yaxis_title='Medios',
    #             yaxis=dict(autorange='reversed'),
    #             width=450, 
    #             height=320
    #         )
    #     st.plotly_chart(fig_opt_con)
    
    # with colb:
    fig_opt = go.Figure(go.Bar(
            x=[round(menten_params['inv_EXTERIORES'][0], 2),
               round(menten_params['inv_RADIO'][0], 2), 
               round(menten_params['inv_META'][0], 2), 
               round(menten_params['inv_TIK TOK'][0], 2),
                 round(menten_params['inv_TV'][0], 2), 
               round(menten_params['inv_XAXIS'][0], 2), 
               round(menten_params['inv_YOUTUBE'][0], 2)],
            y=channels,
            orientation='h',
            marker=dict(color='skyblue'),
            text=[round(menten_params['inv_EXTERIORES'][0], 2), 
                  round(menten_params['inv_RADIO'][0], 2), 
               round(menten_params['inv_META'][0], 2),
                 round(menten_params['inv_TIK TOK'][0], 2), 
               round(menten_params['inv_TV'][0], 2), 
               round(menten_params['inv_XAXIS'][0], 2),
                 round(menten_params['inv_YOUTUBE'][0], 2)], 
            textposition='auto'
            ))
        
    fig_opt.update_layout(
            title='Valores óptimos de inversión por semana',
            xaxis_title='Inversión',
            yaxis_title='Medios',
            yaxis=dict(autorange='reversed'),
            width=650, 
            height=320
        )
    
    st.plotly_chart(fig_opt, use_container_width=True)  

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")