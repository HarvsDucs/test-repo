from flask import Flask, request, jsonify, make_response
import pandas as pd

app = Flask(__name__)

# Example transform endpoint
@app.route('/transform_data', methods=['POST','GET'])

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
