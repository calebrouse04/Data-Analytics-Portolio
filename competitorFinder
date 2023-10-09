import requests
import overpy
import json
import pandas as pd
from datetime import datetime

api = overpy.Overpass()

# Your Google Places API Key
google_api_key = "SECRET"

def get_competitors(address):
    # Geocoding
    print('.')
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_api_key}"
    response = requests.get(geocode_url)
    resp_json = response.json()

    # Handle invalid address
    if resp_json['status'] != 'OK':
        return [{'competitor': 'Invalid address', 'address': None, 'earliest_review': None}]

    location = resp_json['results'][0]['geometry']['location']
    lat = location['lat']
    lon = location['lng']

    # Query string
    query = f"""
        (
        node["amenity"="fuel"](around:3200,{lat},{lon});
        );
        out;
        """
    # Send the query
    result = api.query(query)

    competitors = []
    # Loop through the results
    for node in result.nodes:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={node.lat},{node.lon}&key={google_api_key}"
        response = requests.get(geocode_url)
        resp_json = response.json()

        # Handle no results from reverse geocoding
        if resp_json['status'] != 'OK':
            competitors.append({'competitor': 'No address found', 'address': None, 'earliest_review': None})
            continue

        place_id = resp_json['results'][0]['place_id']
        competitor_address = resp_json['results'][0]['formatted_address']

        # Fetching review data
        google_place_details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,reviews&key={google_api_key}"
        response = requests.get(google_place_details_url)
        resp_json = response.json()

        # Check if 'result' key exists
        if 'result' in resp_json:
            competitor_name = resp_json['result'].get('name', 'Unknown')

            if 'reviews' in resp_json['result']:
                earliest_review = min(resp_json['result']['reviews'], key=lambda x: x['time'])
                earliest_review_date = datetime.fromtimestamp(earliest_review['time']).strftime('%Y-%m-%d')
            else:
                earliest_review_date = None
        else:
            competitor_name = 'Unknown'
            earliest_review_date = None

        competitors.append({'competitor': competitor_name, 'address': competitor_address, 'earliest_review': earliest_review_date})

    return competitors


# Load the Excel file
df = pd.read_excel('store_list.xlsx')  # replace with your actual file path

# Combine City, State, and Street Address into Full Address
df['Full Address'] = df['Street Address'] + ', ' + df['City'] + ', ' + df['State']

# For each full address, get the competitors
df['Competitors'] = df['Full Address'].apply(get_competitors)

# Flatten the competitors data
competitors = df.explode('Competitors')

# Break the dictionary in competitors into separate columns
competitors = pd.concat([competitors.drop(['Competitors'], axis=1), competitors['Competitors'].apply(pd.Series)], axis=1)

# Save the updated dataframe to a new Excel file
competitors.to_excel('store_list_updated.xlsx', index=False)
