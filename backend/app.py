

# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize Flask app with a name
superkart_api = Flask("SuperKart")

# Load the trained churn prediction model
model = joblib.load("superkart_sales_forecast_model_v1_0.joblib")

# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to the Super Kart sales forecasting API!"

# Define an endpoint to predict forecast of single product sales at a given store
@superkart_api.post('/v1/forecast')
def forecast_sales():
    # Get JSON data from the request
    data = request.get_json()

    # Extract relevant product features from the input data. The order of the column names matters.
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type': data['Product_Type']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a sale prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})

# Define an endpoint for batch sales prediction (POST request)
@superkart_api.post('/v1/forecastbatch')
def forecast_sales_batch():
    """
    This function handles POST requests to the '/v1/forecastbatch' endpoint.
    It expects a CSV file containing details for multiple products,
    including 'Product_Id' and 'Store_Establishment_Year'.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_df = pd.read_csv(file)

    # Store Product_Id for output mapping
    product_ids = input_df['Product_Id'].tolist()

    # Calculate Store_Age_Years
    input_df['Store_Age_Years'] = 2025 - input_df['Store_Establishment_Year']

    # Define columns needed for prediction, aligning with X_train
    # The preprocessor handles one-hot encoding of categorical features.
    features_for_model = [
        'Product_Weight', 'Product_Sugar_Content', 'Product_Allocated_Area',
        'Product_Type', 'Product_MRP', 'Store_Size',
        'Store_Location_City_Type', 'Store_Type', 'Store_Age_Years'
    ]
    
    # Select and reorder columns for prediction
    input_data_for_prediction = input_df[features_for_model]

    # Make predictions for all products in the DataFrame
    predicted_sales = model.predict(input_data_for_prediction).tolist()

    # Create a dictionary of predictions with product IDs as keys
    output_dict = dict(zip(product_ids, predicted_sales))

    # Return the predictions dictionary as a JSON response
    return jsonify(output_dict)


# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
