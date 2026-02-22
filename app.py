import streamlit as st
import joblib
import numpy as np

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Earth Pressure Prediction",
    layout="wide"
)

# --------------------------------------------------
# Instagram Dark Theme Styling
# --------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #000000;
}

.main {
    background-color: #000000;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3, h4 {
    color: #ffffff;
}

p, label {
    color: #ffffff;
}

.stNumberInput > div > div > input {
    background-color: #121212;
    color: white;
    border-radius: 8px;
    border: 1px solid #262626;
}

.stButton > button {
    background-color: #0095f6;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1877f2;
}

.section-box {
    background-color: #121212;
    padding: 25px;
    border-radius: 12px;
    border: 1px solid #262626;
}

.footer {
    text-align: center;
    font-size: 13px;
    color: #8e8e8e;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Model
# --------------------------------------------------
data = joblib.load("model/pa_prediction_model.pkl")
model = data["model"]

# --------------------------------------------------
# Header Section
# --------------------------------------------------
st.markdown("## Earth Pressure Prediction")
st.markdown("Predict Total Active Earth Pressure (Pa) using Machine Learning.")

st.divider()

# --------------------------------------------------
# Input Section
# --------------------------------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    H_m = st.number_input("Height H (m)", min_value=0.0, value=5.0)
    gamma_kN_m3 = st.number_input("Unit Weight γ (kN/m³)", min_value=0.0, value=18.0)
    c_kPa = st.number_input("Cohesion c (kPa)", min_value=0.0, value=5.0)

with col2:
    phi_deg = st.number_input("Friction Angle φ (deg)", min_value=0.0, value=30.0)
    beta_deg = st.number_input("Backfill Slope β (deg)", min_value=0.0, value=0.0)
    delta_deg = st.number_input("Wall Friction δ (deg)", min_value=0.0, value=0.0)

with col3:
    q_kPa = st.number_input("Surcharge q (kPa)", min_value=0.0, value=10.0)
    Hw_by_H = st.number_input("Water Table Ratio (Hw/H)", min_value=0.0, value=0.0)
    i_deg = st.number_input("Inclination i (deg)", min_value=0.0, value=0.0)

st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# Predict Button
# --------------------------------------------------
predict = st.button("Predict Earth Pressure", use_container_width=True)

if predict:

    input_data = np.array([[
        H_m,
        gamma_kN_m3,
        c_kPa,
        phi_deg,
        beta_deg,
        delta_deg,
        q_kPa,
        Hw_by_H,
        i_deg
    ]])

    prediction = model.predict(input_data)
    pa_value = prediction[0]

    if pa_value < 0:
        st.info("No Active Pressure Developed (Pa = 0 assumed for design).")
        pa_value = 0

    st.markdown(f"### Predicted Pa: {pa_value:.2f} kN/m")

    # Classification
    if pa_value < 100:
        st.success("LOW EARTH PRESSURE — Generally Safe")
    elif 100 <= pa_value < 250:
        st.warning("MODERATE EARTH PRESSURE — Check Structural Design")
    else:
        st.error("HIGH EARTH PRESSURE — Critical Condition")

st.divider()

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("""
<div class="footer">
Developed as part of the project:<br>
Prediction of Earth Pressure on Retaining Wall using Analytical & ML Approaches<br><br>
Random Forest Regression Model<br>
Developed by Solminde
</div>
""", unsafe_allow_html=True)