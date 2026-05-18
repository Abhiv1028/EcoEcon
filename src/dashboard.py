
"""
EcoEcon Live Dashboard
Biological Early Warning Signals for Economic Crises
Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import sys

# Add project root to path so we can import if needed
sys.path.insert(0, os.path.expanduser('~/ecoecon'))

st.set_page_config(
    page_title="EcoEcon — Economic Early Warning",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 EcoEcon — Biological Early Warning System")
st.caption("Modeling the US economy as an ecosystem. Sectors = species. Supply chains = food webs. Crises = extinction cascades.")

# ---- Load data ----
@st.cache_data
def load_data():
    data_dir = os.path.expanduser('~/ecoecon/data/processed')

    # Monthly master dataset
    monthly = pd.read_csv(os.path.join(data_dir, 'master_monthly.csv'), parse_dates=['date'])

    # Model comparison
    comparison = pd.read_csv(os.path.join(data_dir, 'full_model_comparison.csv'))

    return monthly, comparison

monthly, comparison = load_data()

# ---- Sidebar: Key Metrics ----
st.sidebar.header("Key Metrics (Most Recent Month)")

latest = monthly.iloc[-1]
crisis_status = "🔴 HIGH RISK" if latest['crisis'] == 1 else "🟢 Normal"

st.sidebar.metric("Crisis Status", crisis_status)
st.sidebar.metric("Economic Biodiversity Index", f"{latest['ebi']:.4f}")
st.sidebar.metric("Spectral Gap", f"{latest['spectral_gap']:.4f}")
st.sidebar.metric("Housing Variance (CSD)", f"{latest['housing_var_var']:.0f}")

# If we have GNN predictions
if 'gnn_prob' in monthly.columns:
    gnn_latest = monthly['gnn_prob'].iloc[-1]
    st.sidebar.metric("GNN Crisis Probability", f"{gnn_latest:.3f}",
                      delta=f"{'↑' if gnn_latest > 0.5 else '↓'}")

st.sidebar.divider()
st.sidebar.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.caption("Data: BEA Input-Output + FRED")
st.sidebar.caption("Author: Abhinav Vaddi")

# ---- Main Panel: Tabs ----
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Early Warning Signals", 
    "🤖 GNN Predictions",
    "📋 Model Comparison",
    "📖 Methodology"
])

with tab1:
    st.subheader("Early Warning Signals (2002–2009)")

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    crisis_mask = monthly['crisis'] == 1
    dates = pd.to_datetime(monthly['date'])

    signals = [
        ('ebi', '#1D9E75', 'Economic Biodiversity Index'),
        ('spectral_gap', '#534AB7', 'Spectral Gap'),
        ('housing_var_var', '#D85A30', 'Housing Starts Variance (Critical Slowing Down)')
    ]

    for ax, (col, color, title) in zip(axes, signals):
        values = monthly[col].values
        ax.plot(dates, values, color=color, linewidth=1.5)
        ax.fill_between(dates, values, values.min(),
                        where=crisis_mask.values,
                        alpha=0.20, color='#D85A30', label='2008 Crisis')
        ax.set_title(title, fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(fontsize=8, loc='upper right')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.tight_layout()
    st.pyplot(fig)

    st.caption("The Economic Biodiversity Index and housing variance both peaked in 2005 — 18 months before the crisis began.")

with tab2:
    st.subheader("GNN Crisis Probability Timeline")

    if 'gnn_prob' in monthly.columns:
        fig, ax = plt.subplots(figsize=(12, 4))

        ax.plot(dates, monthly['gnn_prob'], color='#534AB7', linewidth=1.5, label='GNN Crisis Probability')
        ax.fill_between(dates, 0, 1, where=crisis_mask.values,
                        alpha=0.15, color='#D85A30', label='Actual Crisis Period')
        ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=0.8, alpha=0.7, label='Decision Threshold')

        ax.set_ylabel('Crisis Probability')
        ax.legend(fontsize=8, loc='upper left')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.set_ylim(0, 1)

        plt.tight_layout()
        st.pyplot(fig)

        st.caption("GNN trained on 96 monthly observations. AUC = 0.991 on the 2008 crisis test period.")
    else:
        st.warning("GNN predictions not found. Run notebook 04 to generate them.")

    st.subheader("GNN Architecture")
    st.code("""
    class MonthlyGNN(nn.Module):
        def __init__(self):
            self.conv1 = GCNConv(1, 32)     # 1 input per node → 32
            self.conv2 = GCNConv(32, 16)    # 32 → 16
            self.conv3 = GCNConv(16, 8)     # 16 → 8
            self.dropout = nn.Dropout(0.4)
            self.bn1 = nn.BatchNorm1d(32)
            self.bn2 = nn.BatchNorm1d(16)
            self.classifier = nn.Linear(8, 1)

        def forward(self, x, edge_index, batch):
            x = self.conv1(x, edge_index) → BN → ReLU → Dropout
            x = self.conv2(x, edge_index) → BN → ReLU → Dropout
            x = self.conv3(x, edge_index) → ReLU
            x = global_mean_pool(x, batch)
            return sigmoid(self.classifier(x))
    """, language='python')

with tab3:
    st.subheader("Full Model Comparison")
    st.dataframe(comparison.sort_values('AUC', ascending=False), 
                 use_container_width=True, hide_index=True)

    st.subheader("Key Takeaway")
    st.markdown("""
    - **GNN (monthly)** achieves AUC = 0.991 — capturing cross-variable interactions that linear models miss
    - **Housing starts variance alone** achieves AUC = 0.954 — the ecological early warning signal works with zero crisis training data
    - **Annual GNN fails** at AUC = 0.333 — insufficient data (n=8) for deep learning, motivating the monthly expansion
    """)

with tab4:
    st.subheader("Variable Mapping")
    st.markdown("""
    | Ecological Concept | Economic Analog |
    |---|---|
    | Species | Sector (68 BEA industries) |
    | Predator-prey relationship | Supplier-buyer dependency |
    | Biomass flow | Revenue flow between sectors |
    | Keystone species | Systemically important institution |
    | Extinction cascade | Bankruptcy contagion |
    | Ecosystem biodiversity | Sector concentration (EBI) |
    | Critical slowing down | Rising variance + autocorrelation in financial time series |
    | Spectral gap collapse | Network fragmentation before crisis |
    """)

    st.subheader("Data Sources")
    st.markdown("""
    - **BEA Input-Output Tables** (TableID 259, 2002–2009): 68-sector inter-industry monetary flows
    - **FRED Economic Data**: Housing starts (HOUST), bank credit (TOTBKCR), credit spread (BAMLH0A0HYM2), consumer credit (TOTALSL), Fed funds rate (FEDFUNDS)
    - **NBER**: Official recession/crisis dating
    """)

    st.subheader("References")
    st.markdown("""
    1. May, R.M. (1972). Will a large complex system be stable? *Nature*, 238, 413-414.
    2. Scheffer et al. (2009). Early-warning signals for critical transitions. *Nature*, 461, 53-59.
    3. Acemoglu et al. (2015). Systemic risk and stability in financial networks. *American Economic Review*, 105(2), 564-608.
    4. Shannon, C.E. (1948). A mathematical theory of communication. *Bell System Technical Journal*.
    5. Hamilton, W.L. et al. (2017). Inductive representation learning on large graphs. *NeurIPS*.
    """)

st.divider()
st.caption("🌿 EcoEcon — Biological Early Warning Signals for Economic Crises | Abhinav Vaddi")
