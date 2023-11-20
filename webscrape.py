import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_to_csv(url, chamber, output_file='output.csv'):
    # Make the HTTP request and get the response content
    response = requests.get(url)
    if response.ok:
        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(response.text, "html.parser")

        # Read existing data into a set for quick lookup
        existing_data = set()
        if os.path.exists(output_file):
            with open(output_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                existing_data = {tuple(row) for row in reader}

        # Open the CSV file in append mode
        with open(output_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Iterate through each 'tr' tag and collect 'td' elements and 'a' tags
            for tr in soup.find_all('tr'):
                row_data = [td.text.strip() for td in tr.find_all('td')]
                # Find 'a' tags for district and email within the row
                links = tr.find_all('a', href=True)
                district = links[0]['href'].split('/')[-1] if links else ''
                email = links[1]['href'].replace('mailto:', '') if len(links) > 1 else ''
                # Append district and email to row data
                row_data.extend([district, email])
                # Append the chamber information
                row_data.append(chamber)
                # Convert the list to a tuple for the set operation
                row_tuple = tuple(row_data)
                if row_tuple not in existing_data:  # Check for new unique rows
                    writer.writerow(row_data)
                    existing_data.add(row_tuple)  # Add the new row to the set of existing data

        print(f"Data appended to {output_file} successfully.")
    else:
        print("Failed to retrieve content")

# Use the function with the provided URL for the House
scrape_to_csv('https://wapp.capitol.tn.gov/apps/LegislatorInfo/directory.aspx?chamber=H', 'Representative')

# Use the function with the provided URL for the Senate
scrape_to_csv('https://wapp.capitol.tn.gov/apps/LegislatorInfo/directory.aspx?chamber=S', 'Senator')
