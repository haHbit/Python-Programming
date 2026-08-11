import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Production_car_speed_record"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')   

cars = []  #create a list to append information

for row in soup.find('table', {'class': 'wikitable'}).find_all('tr')[1:]:
    columns = row.find_all('td')
    if len(columns) > 1:
        year = columns[0].text.strip()
        make_model = columns[1].text.strip()
        top_speed = columns[2].text.strip()
        engine = columns[3].text.strip()
        number_built = columns[4].text.strip()

    cars.append({
        'Make and Model': make_model,
        'Top Speed': top_speed,
        'Year': year,
        'Engine': engine,
        'Number built': number_built
    })


df = pd.DataFrame(cars)
df.to_csv('Record breaking Cars.csv', index=False)
print("Data has been successfully extracted and saved to Record breaking Cars.csv")
