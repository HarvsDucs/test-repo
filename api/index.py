from flask import Flask, request, jsonify, make_response
from functools import wraps
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import csv
import io
import pandas as pd
import re

load_dotenv()
app = Flask(__name__)

# Supabase configuration -  IMPORTANT: Use environment variables for security in production
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to fetch API key from Supabase
def get_api_key_from_supabase():
    try:
        response = supabase.table("api_keys").select("api_key").execute()
        if response.data and len(response.data) > 0:
            # Assuming you have only one API key in the table or want to use the first one
            # If you have multiple keys, you might need to adjust the query to select based on some criteria
            return response.data[0]["api_key"]
        else:
            print("Warning: No API key found in Supabase table 'api_keys'.") # Log this for debugging
            return None  # Or raise an exception if API key is mandatory
    except Exception as e:
        print(f"Error fetching API key from Supabase: {e}") # Log the error
        return None


# Decorator to check for API key fetched from Supabase
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key_from_request = request.headers.get('X-API-Key')  # Or request.args.get('api_key')

        if not api_key_from_request:
            return jsonify({"message": "Unauthorized. API key is missing."}), 401

        api_key_from_db = get_api_key_from_supabase()

        if api_key_from_db and api_key_from_request == api_key_from_db:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Unauthorized. Invalid API key."}), 401
    return decorated_function

# Example protected endpoint
@app.route('/transform_data', methods=['POST','GET'])
@require_api_key  # Apply the decorator to this endpoint

def transform_data():
    try:
        data = request.get_json() # Assumes the request body is JSON
        df = pd.DataFrame(data)   # Convert to DataFrame

        # ETL: Add the "Email Provider" Column
        def extract_email_provider(email):
            try:
                username, domain = email.split('@')
                return domain
            except:
                return ""  # Handle invalid emails

        df['Email Provider'] = df['Email'].apply(extract_email_provider)

        # Convert the DataFrame back to JSON
        transformed_data = df.to_dict(orient='records') # converts to a list of dicts
        return jsonify(transformed_data), 200

    except Exception as e:
        return jsonify({'error': f'Error processing data: {str(e)}'}), 500

# Example unprotected endpoint (for comparison)
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the API! This is an unprotected endpoint."

if __name__ == '__main__':
    app.run(debug=True)