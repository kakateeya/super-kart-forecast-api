
import streamlit as st
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

st.title("SuperKart sales forecasting")
st.subheader("Please enter the following product details to get forecast for the sales.")

# Input fields for product and store data
Product_Weight = st.number_input("Product Weight", min_value=0.0, max_value=30.0, value=15.0)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area", min_value=0.0, max_value=0.3, value=0.1)
Product_MRP = st.number_input("Product_MRP", min_value=0.0, max_value=300.0, value=150.0)
Store_Size = st.selectbox("Store_Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox("Store_Location_City_Type", ["Tier_1", "Tier_2", "Tier_3"])
Store_Type = st.selectbox("Store_Type", ["Departmental Store", "Supermarket Type 1", "Supermarket Type 2", "Food Mart"])
Store_Age_Years = st.number_input("Store_Age_Years", min_value=1, max_value=50, value=20)
Product_Type = st.selectbox("Product_Type", ["Baking goods", "Bread", "Breakfast", "Canned", "Dairy", "Frozen foods",
                                                      "Fruits and vegetables", "Hard drinks", "Health and hygiene",
                                                      "Household", "Meat", "Snack foods", "Soft drinks", "Seafood",
                                                      "Starchy foods", "Others"])

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type": Product_Type
}

if st.button("Forecast", type='primary'):
    response = requests.post(f"{BACKEND_URL}/v1/forecast", json=product_data)
    if response.status_code == 200:
        result = response.json()
        predicted_sales = result["Sales"]
        st.write(f"Predicted Product Store Sales Total: ₹{predicted_sales:.2f}")
    else:
        st.error(f"API error: {response.status_code}")
        st.code(response.text)

# Section for batch prediction
st.subheader("Batch Forecast")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Forecast Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/forecastbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch forecast completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error(f"API error: {response.status_code}")
            st.code(response.text)
