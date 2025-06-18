import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load model and data
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
car = pd.read_csv('Cleaned_Car_data.csv')

# Page setup
st.set_page_config(page_title="Car Price Estimator", page_icon="🚗", layout="centered")

# --- CSS Styling (background removed) ---
st.markdown("""
    <style>
    /* Removed background-image */
    .main-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem 3rem;
        border-radius: 16px;
        box-shadow: 0 0 25px rgba(0,0,0,0.15);
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #1f77b4;
    }

    .stButton > button {
        background-color: #1f77b4;
        color: white;
        padding: 0.5rem 2rem;
        font-size: 16px;
        border: none;
        border-radius: 6px;
    }

    .stButton > button:hover {
        background-color: #125a92;
        transition: 0.3s ease;
    }

    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.title("🚗 Used Car Price Estimator")
st.markdown("Get an instant resale value estimate based on your car's details.")

# Dropdown values
companies = sorted(car['company'].unique())
years = sorted(car['year'].unique(), reverse=True)
fuel_types = car['fuel_type'].unique()

# Input fields
col1, col2 = st.columns(2)

with col1:
    company = st.selectbox("🏢 Select Company", ['Select Company'] + companies)

    if company != 'Select Company':
        models = sorted(car[car['company'] == company]['name'].unique())
    else:
        models = []

    model_name = st.selectbox("🚘 Select Model", ['Select Model'] + models)
    year = st.selectbox("📅 Year of Purchase", years)

with col2:
    fuel_type = st.selectbox("⛽ Fuel Type", fuel_types)
    kms_driven = st.number_input("🧭 Kilometers Driven", min_value=0, step=1000, value=10000)

# Predict button
if st.button("🔍 Predict Price"):
    if company == 'Select Company' or model_name == 'Select Model':
        st.warning("⚠️ Please select a valid car company and model.")
    else:
        input_df = pd.DataFrame(
            [[model_name, company, year, kms_driven, fuel_type]],
            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']
        )

        prediction = model.predict(input_df)[0]
        price_lakhs = np.round(prediction / 100000, 2)

        st.success(f"💰 **Estimated Resale Price: ₹ {price_lakhs} Lakh**")

st.markdown("</div>", unsafe_allow_html=True)
