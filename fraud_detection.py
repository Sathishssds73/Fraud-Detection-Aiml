import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Fraud Detection App", layout="centered")

# Load the trained model safely
try:
    model = joblib.load("fraud_detection_model.pkl")
except Exception as e:
    st.error(f"⚠️ Could not load model: {e}")
    st.stop()

st.title("💳 Fraud Detection Prediction App")
st.markdown("Please enter the transaction details below and click **Predict**")

st.divider()

# Inputs
transaction_type = st.selectbox(
    "Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEPOSIT"]
)

amount = st.number_input("Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=9000.0)
oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=0.0)

# Predict button
if st.button("Predict"):
    # Step 1: Create DataFrame
    input_data = pd.DataFrame([{
        "type": transaction_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }])

    # Step 2: Feature Engineering (create missing columns)
    input_data["balanceDiffOrig"] = input_data["oldbalanceOrg"] - input_data["newbalanceOrig"] - input_data["amount"]
    input_data["balanceDiffDest"] = input_data["newbalanceDest"] - input_data["oldbalanceDest"] - input_data["amount"]

    try:
        # Step 3: Predict
        prediction = model.predict(input_data)[0]
        st.subheader(f"Prediction: **{int(prediction)}**")
        if prediction == 1:
            st.error("⚠️ This transaction may be FRAUD!")
        else:
            st.success("✅ This transaction looks SAFE.")
    except Exception as e:
        st.error(f"Prediction error: {e}")
