import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# function to scrape fight odds using Selenium
def scrape_fight_odds(url):
    driver = webdriver.Chrome() 
    driver.get(url)
    
    # wait for the page to fully load
    time.sleep(5)
    
    # get the page source after it's fully rendered
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    odds_list = []
    span_id_prefix = 'oID'
    span_id_number = 0
    
    # loop through and find the odds
    while True:
        span_id = f'{span_id_prefix}{span_id_number}'
        odds_span = soup.find('span', id=span_id)
        
        if odds_span:
            odds = odds_span.get_text(strip=True)
            odds_list.append(odds)
            span_id_number += 6  # move to the next span (increment by 6)
        else:
            break 
    
    driver.quit() 
    return odds_list

# function to scrape win/loss data from Wikipedia
def scrape_wikipedia_results(url):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results_list = []
    
    # extract win/loss data from the Wikipedia table
    for row in soup.find_all('tr'):
        result = row.find('td', class_='table-yes2')  # Win case
        if result:
            results_list.append('Win')
        else:
            result = row.find('td', class_='table-no2')  # Loss case
            if result:
                results_list.append('Loss')
    
    return results_list

# function to fetch Max Holloway data from the API
def fetch_max_holloway_data():
    api_key = 'REPLACE WITH KEY LATER'
    url = 'https://api.sportsdata.io/v3/mma/scores/json/Fighters'
    headers = {
        'Ocp-Apim-Subscription-Key': api_key
    }

    response = requests.get(url, headers=headers)

    # check if the request was successful
    if response.status_code == 200:
        fighters_data = response.json()

        # search for Max Holloway by comparing FirstName and LastName
        max_holloway_data = next((fighter for fighter in fighters_data if fighter['FirstName'].lower() == 'max' and fighter['LastName'].lower() == 'holloway'), None)

        if max_holloway_data:
            return max_holloway_data
        else:
            print("Max Holloway not found.")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# URLs I used for scraping
odds_url = "https://www.bestfightodds.com/fighters/Max-Holloway-3090"
wiki_url = "https://en.wikipedia.org/wiki/Max_Holloway"

fight_odds = scrape_fight_odds(odds_url)
fight_results = scrape_wikipedia_results(wiki_url)
max_holloway_data = fetch_max_holloway_data()

#combine the fight odds, win/loss results, and fighter profile into a DataFrame
df = pd.DataFrame({
    'Fight Odds': fight_odds,
    'Result': fight_results[:len(fight_odds)],
})

if max_holloway_data:
    df['Height'] = max_holloway_data.get('Height', 'N/A')
    df['Weight'] = max_holloway_data.get('Weight', 'N/A')
    df['Reach'] = max_holloway_data.get('Reach', 'N/A')
    df['Wins'] = max_holloway_data.get('Wins', 'N/A')
    df['Losses'] = max_holloway_data.get('Losses', 'N/A')

print(df)
