import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus/"

corona_content = requests.get(url, "html.parser")
soup = BeautifulSoup(corona_content.content)

table = soup.find("table", id="main_table_countries_today")

data = {
    "Country": [],
    "Total Cases": [],
    "New Cases": [],
    "Total Deaths": [],
    "New Deaths": [],
    "Total Recovered": [],
    "New Recovered": [],
    "Active Cases": [],
    "Serious, Critical": [],
    "Tot Cases/1M pop": [],
    "Deaths/1M pop": [],
    "Total tests": [],
    "Tests/1M pop": [],
    "Population": [],
    "Continent": [],
    "1 Case every X ppl": [],
    "1 Death every X ppl": [],
    "1 Test every X ppl": [],
    "New Cases/1M pop": [],
    "New Deaths/1M pop": [],
    "Active Cases/1M pop": [],
}

data_rows = table.find("tbody").find_all("tr")

for row in data_rows[8:]:
    columns = row.find_all("td")[1:]
    for i, k in zip(columns, data):
        data[k].append(i.text.strip())

# Find the element containing the datetime string
date_elem = soup.find("div", class_="content-inner")

# Find the div element containing the datetime
date = date_elem.find("div", {"style": "font-size:13px; color:#999; margin-top:5px; text-align:center"})
content = date.text.strip()

# Split string so that we have a perfect datetime string
datetime = content[content.find('M'):content.find(', 1')].replace(',', '').replace(' ', '_')
print(datetime)

# Create a Pandas DataFrame from the dictionary
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv(f"{datetime}_corona_data.csv", index=False)

print(type(df))
