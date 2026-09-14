import random
import matplotlib.pyplot as plt
import streamlit as st

# Custom Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B1220;
        color: #F8FAFC;
    }
    div[data-testid="stMetricValue"] {
        font-size: 22px;
        font-weight: bold;
        color: #10B981;
    }
    label {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Helper Functions
def pv_deferred_ordinary(R, i, n, k):
    return R * ((1 - (1 + i) ** (-n)) / i) * ((1 + i) ** (-k))

def fv_deferred_ordinary(R, i, n, k):
    return R * (((1 + i) ** n - 1) / i) * ((1 + i) ** k)

def pv_deferred_due(R, i, n, k):
    d = max(0.0, k - 1.0)
    return R * ((1 - (1 + i) ** (-n)) / i) * ((1 + i) ** (-d))

def fv_deferred_due(R, i, n, k):
    d = max(0.0, k - 1.0)
    return R * (((1 + i) ** n - 1) / i) * ((1 + i) ** d)

def randomize_inputs():
    st.session_state["dash_R"] = float(random.choice([1000, 2500, 5000, 10000, 15000, 20000]))
    # Buong numero mula 2% hanggang 12% (walang butal)
    st.session_state["dash_i"] = float(random.randint(2, 12))
    st.session_state["dash_n"] = float(random.randint(3, 15))
    st.session_state["dash_k"] = float(random.randint(1, 5))

# UI Header
st.title("TVM Annuity Studio")
st.caption("Deferred Annuity Calculator")

st.subheader("Inputs")
c1, c2, c3, c4 = st.columns(4)

with c1:
    R = st.number_input("Regular Payment (R)", value=st.session_state.get("dash_R", None), placeholder="e.g. 10000", step=1000.0, format="%g", key="dash_R")
with c2:
    i_in = st.number_input("Interest Rate (i %)", value=st.session_state.get("dash_i", None), placeholder="e.g. 8", step=1.0, format="%g", key="dash_i")
    i = (i_in / 100.0 if i_in >= 1.0 else i_in) if i_in is not None else None
with c3:
    n = st.number_input("Total Payments (n)", value=st.session_state.get("dash_n", None), placeholder="e.g. 5", step=1.0, format="%g", key="dash_n")
with c4:
    k = st.number_input("Full Delay (k)", value=st.session_state.get("dash_k", None), placeholder="e.g. 2", step=1.0, format="%g", key="dash_k")

col_calc, col_rand = st.columns([1, 1])

with col_calc:
    btn_calc = st.button("Calculate All", type="primary", use_container_width=True)

with col_rand:
    st.button("🎲 Randomize Inputs", on_click=randomize_inputs, use_container_width=True)

if btn_calc:
    if None in (R, i, n, k):
        st.warning("Please complete all required fields before calculating.")
    else:
        pv_ord = pv_deferred_ordinary(R, i, n, k)
        fv_ord = fv_deferred_ordinary(R, i, n, k)
        pv_due = pv_deferred_due(R, i, n, k)
        fv_due = fv_deferred_due(R, i, n, k)

        st.subheader("Results")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("PV — Deferred Ord", f"₱{pv_ord:,.2f}")
        m2.metric("PV — Deferred Due", f"₱{pv_due:,.2f}")
        m3.metric("FV — Deferred Ord", f"₱{fv_ord:,.2f}")
        m4.metric("FV — Deferred Due", f"₱{fv_due:,.2f}")

        # Chart Section
        fig, ax = plt.subplots(figsize=(8, 3.5))
        fig.patch.set_facecolor('#0B1220')
        ax.set_facecolor('#141C2E')

        labels = ["PV Def Ord", "PV Def Due", "FV Def Ord", "FV Def Due"]
        values = [pv_ord, pv_due, fv_ord, fv_due]
        colors = ["#10B981", "#059669", "#22D3EE", "#0E7490"]

        bars = ax.bar(labels, values, color=colors)
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#2A3B57')

        st.pyplot(fig)
