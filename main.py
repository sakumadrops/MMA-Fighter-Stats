import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape fight odds using Selenium since BeautifulSoup doesn't work for BestFightOdds
def scrape_fight_odds(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
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
            span_id_number += 6  # move to the next span (increment by 6 according to my findings)
        else:
            break 
    
    driver.quit() 
    return odds_list

# function to scrape win/loss data from Wikipedia
def scrape_wikipedia_results(first_name, last_name):
    wiki_url = f"https://en.wikipedia.org/wiki/{first_name}_{last_name}"
    headers = {'User-Agent': "Mozilla/5.0"}
    response = requests.get(wiki_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results_list = []
    
    # extract win/loss data from the Wikipedia table
    for row in soup.find_all('tr'):
        result = row.find('td', class_='table-yes2')
        if result:
            results_list.append('Win')
        else:
            result = row.find('td', class_='table-no2') 
            if result:
                results_list.append('Loss')
    
    return results_list

# function to collect UFC fighter data from the SportsData API
def fetch_fighter_data(first_name, last_name):
    api_key = 'f26e1da77b4843bd9c340e539f55be4f'
    url = 'https://api.sportsdata.io/v3/mma/scores/json/Fighters'
    headers = {'Ocp-Apim-Subscription-Key': api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        fighters_data = response.json()
        fighter_data = next((fighter for fighter in fighters_data if fighter['FirstName'].lower() == first_name.lower() and fighter['LastName'].lower() == last_name.lower()), None)

        if fighter_data:
            return fighter_data
        else:
            print(f"Fighter {first_name} {last_name} not found.")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# the MAIN function
def collect_fighter_data():
    first_name = input("Enter the fighter's first name: ")
    last_name = input("Enter the fighter's last name: ")
    odds_url = input("Enter the BestFightOdds URL for the fighter: ")

    fight_odds = scrape_fight_odds(odds_url)
    fight_results = scrape_wikipedia_results(first_name, last_name)
    fighter_data = fetch_fighter_data(first_name, last_name)

    # combine the fight odds, win/loss results, and fighter profile into a DataFrame
    df = pd.DataFrame({
        'Fight Odds': fight_odds,
        'Result': fight_results[:len(fight_odds)],
    })

    if fighter_data:
        df['Height'] = fighter_data.get('Height', 'N/A')
        df['Weight'] = fighter_data.get('Weight', 'N/A')
        df['Reach'] = fighter_data.get('Reach', 'N/A')
        df['Wins'] = fighter_data.get('Wins', 'N/A')
        df['Losses'] = fighter_data.get('Losses', 'N/A')

    # clean the data
    df['Wins'] = pd.to_numeric(df['Wins'], errors='coerce').fillna(0).astype(int)
    df['Losses'] = pd.to_numeric(df['Losses'], errors='coerce').fillna(0).astype(int)

    # export the cleaned dataset to a CSV file
    output_file = f'{first_name}_{last_name}_fight_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Data exported to {output_file}")
    print(df)


collect_fighter_data()
