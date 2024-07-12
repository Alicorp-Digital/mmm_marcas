if __name__ == '__main__':

    
    import warnings
    
    import arviz as az
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import pymc as pm
    import seaborn as sns
    import streamlit as st
    from st_pages import Page, Section, show_pages, add_page_title, hide_pages
    
    from pymc_marketing.mmm.delayed_saturated_mmm import DelayedSaturatedMMM
    from pymc_marketing.mmm.transformers import geometric_adstock, logistic_saturation
    from pymc_marketing.mmm.budget_optimizer import calculate_expected_contribution

    st.set_page_config(
        page_title="MMM ALICORP", page_icon=":chart_with_upwards_trend:"
    )

    warnings.filterwarnings("ignore")

    az.style.use("arviz-darkgrid")
    plt.rcParams["figure.figsize"] = [12, 5]
    plt.rcParams["figure.dpi"] = 100
    
    add_page_title()

    show_pages(
        [   
            Page("st_mmm.py", "Marketing Mix Modeling - ALICORP"),

            Section("JABONES DE LAVAR BOLIVAR"),
            Page("utils/scenarios.py", "Escenarios de presupuesto y contribución", "1️⃣", in_section=True),
            Page("utils/components.py", "Contribución por componentes", "2️⃣", in_section=True),
            Page("utils/vol_historico.py", "Información histórica", "3️⃣", in_section=True),

            Section("SALSAS ALACENA"),
            Page("utils/scenarios_alacena.py", "Escenarios de presupuesto y contribución", "1️⃣", in_section=True),
            Page("utils/components_alacena.py", "Contribución por componentes", "2️⃣", in_section=True),
            Page("utils/vol_historico_alacena.py", "Información histórica", "3️⃣", in_section=True)
        ]
    )

    st.image("images/mmm_principal.jpg", use_column_width=True)


