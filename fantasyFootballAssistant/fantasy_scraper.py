#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://betiq.teamrankings.com/fantasy-football/rankings/ppr/?size=10'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

rows = soup.find_all('tr')

data = []

for row in rows[1:]:
    cols = row.find_all('td')
    if len(cols) >= 13:
        data.append([
            cols[0].get_text(strip=True),
            cols[1].get_text(strip=True),
            cols[2].get_text(strip=True),
            cols[3].get_text(strip=True),
            cols[4].get_text(strip=True),
            cols[5].get_text(strip=True),
            cols[6].get_text(strip=True),
            cols[7].get_text(strip=True),
            cols[8].get_text(strip=True),
            cols[9].get_text(strip=True),
            cols[10].get_text(strip=True),
            cols[11].get_text(strip=True),
            cols[12].get_text(strip=True)
        ])

columns = [
    'projected_draft_position', 'player_name', 'position', 'team', 'bye_week',
    'passing_data', 'rushing_data', 'receiving_data', 'total_yards',
    'projected_points', 'rushing_yards', 'receiving_yards', 'value'
]

df = pd.DataFrame(data, columns=columns)

df.to_csv('player_data_ordered.csv', index=False)

print("Data scraped and saved to player_data_ordered.csv")

