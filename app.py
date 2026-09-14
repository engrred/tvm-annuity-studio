import streamlit as st
import matplotlib.pyplot as plt

# --- MATH ENGINE ---
def pv_deferred_ordinary(R, i, n, k):
    d = max(0.0, float(k) - 1.0)
    return R * n if i == 0 else R * ((1 - (1 + i) ** (-n)) / i) * ((1 + i) ** (-d))

def fv_deferred_ordinary(R, i, n, k):
    return R * n if i == 0 else R * (((1 + i) ** n - 1) / i)

def pv_deferred_due(R, i, n, k):
    d = max(0.0, float(k) - 1.0)
    return R * n if i == 0 else R * ((1 - (1 + i) ** (-n)) / i) * (1 + i) * ((1 + i) ** (-d))

def fv_deferred_due(R, i, n, k):
    return R * n if i == 0 else R * (((1 + i) ** n - 1) / i) * (1 + i)

# --- STREAMLIT UI ---
st.set_page_config(page_title="TVM Annuity Studio", page_icon="📈", layout="wide")

st.title("TVM Annuity Studio")
st.caption("Deferred Annuity Calculator")

st.subheader("Inputs")
c1, c2, c3, c4 = st.columns(4)

with c1:
    R = st.number_input("Regular Payment (R)", value=10000.0, step=1000.0, format="%g")
with c2:
    i_in = st.number_input("Interest Rate (i)", value=0.08, step=0.01, format="%g")
    # Auto-convert kung sakaling 8 ang i-type sa halip na 0.08
    i = i_in / 100.0 if i_in >= 1.0 else i_in
with c3:
    n = st.number_input("Total Payments (n)", value=5, step=1)
with c4:
    k = st.number_input("Full Delay (k)", value=2, step=1)

if st.button("Calculate All", type="primary"):
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
        
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'₱{height:,.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', color='white', fontsize=8)
                    
    st.pyplot(fig)
