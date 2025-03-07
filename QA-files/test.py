import pandas as pd
import requests  # Import the requests library
import json

# 1. Load CSV to DataFrame
data = pd.read_csv("C:/Users/Harvey/Downloads/demo/customers-100.csv")

# 2. Convert DataFrame to JSON (list of records)
json_data = data.to_dict(orient='records')

# 3. Define Headers for API-KEY authentication
headers = {'Content-Type': 'application/json'}

# 4. Vercel URL for the external API, this was mine but it depends on your vercel deployment URL
url = "https://test-repo-umber-beta.vercel.app/transform_data"


# 5. Make the API call
try:
    response = requests.post(url, headers=headers, json=json_data)

    # Check for successful request (status code 200)
    if response.status_code == 200:
        transformed_data = response.json()  # Parse the JSON response
        print("API call successful!")

        #8. Convert the JSON data back to a Pandas DataFrame
        transformed_df = pd.DataFrame(transformed_data)

        #9. Save the DataFrame to a local CSV file
        transformed_df.to_csv("C:/Users/Harvey/Downloads/demo/transformed_data.csv", index=False)  # index=False avoids saving the DataFrame index to the CSV
        print("Transformed data saved to transformed_data.csv")


    else:
        print(f"API call failed with status code: {response.status_code}")
        print(response.text) # Print the error message from the API

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
