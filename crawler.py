import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv
import json


# Fetch HTML content from the URL
url = "https://nofluffjobs.com/pl/praca-zdalna?page=1" #make the paggination for the number of pages 
response = requests.get(url)
html_page = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_page, 'html.parser')

# Initialize a list to store the parsed job data
job_data_list = []

# Find all the job containers
job_containers = soup.find_all('a', class_='posting-list-item')

# Loop through each job container and extract the desired information
for job_container in job_containers:
    # Extract the data from the job container
    title = job_container.find('h3', class_='posting-title__position').text.strip()
    description = ''  # Add code to extract description if present in the HTML
    town = job_container.find('span', class_='tw-text-ellipsis').text.strip()
    type_of_work = job_container.find('span', class_='text-truncate').text.strip()
    salary = job_container.find('span', class_='salary').text.strip()

    # Append the extracted data to the job_data_list as a dictionary
    job_data_list.append({
        'title': title,
        'description': description,
        'town': town,
        'type_of_work': type_of_work,
        'salary': salary,
    })

# Convert the job_data_list to JSON format
output_json = json.dumps(job_data_list, ensure_ascii=False, indent=2)

# Print the JSON data (or save it to a file)
print(output_json)

with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile: # CSV don't work with some symbols
    fieldnames = ['title', 'description', 'town', 'type_of_work', 'salary']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for job_data in job_data_list:
        writer.writerow(job_data)

# Convert the job_data_list to JSON format and save to a file
with open('jobs.json', 'w', encoding='utf-8') as json_file:
    json.dump(job_data_list, json_file, ensure_ascii=False, indent=2)