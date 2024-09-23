# MMA Fighter Stats
This Python script scans the pages of both Wikipedia and BestFightOdds to find the record for each MMA fighter and their betting odds for each respective fight. It then uses the SportsDataIO API to find the stats of the fighter currently including weight, reach, and most importantly their current win/loss record. The data is then cleaned and imported into a CSV file where data analysis can be conducted.

# Purpose
Watching the UFC, Bellator, ONE Chamionship, or any other MMA promotion is a lot of fun. Some of the aspects that make watching MMA fun also lie in the debates friends have with each other or maybe even bets that people partake in. I made this script to help analyze your favorite fighter. It takes in all of the historical fighting data of whatever fighter you choose and provides the betting odds alongside the result of the fights. This data can be used to figure out a multitude of insights such as how reliable a fighter is by comparing how many times they truly win as the favorite or maybe how many times they've been the underdog and still won. Additionally, some other ideas could be creating a  graph of their betting odds which would display their popularity over time, or putting together an ML model to predict what bet someone should take on a fighter's next fight. The possibilities are wide-ranging!

# Features
- Uses BeautifulSoup and Selenium to scrape UFC fighter data from BestFightOdds and Wikipedia.
- Retrieves detailed fighter profiles (height, weight, reach, wins, losses) from the SportsData API.
- Cleans and processes fight results and betting odds data for the specified fighter.
- Combines all scraped data into a Pandas DataFrame.
- Exports the cleaned data into a CSV file for easy access.

# Packages and Libraries used
- BeautifulSoup4: Used for parsing and navigating the HTML content of Wikipedia and BestFightOdds pages.
- Pandas: For creating, cleaning, and manipulating the DataFrame that holds the fighter data.
- Selenium: This is for dynamically loading content from BestFightOdds.
- Requests: To make API calls to the SportsData API and fetch fighter profiles.
- Python built-in libraries: Includes time for pauses during scraping and requests for HTTP requests.

# Instructions:

1. Enter the UFC fighter's first name, last name, and the BestFightOdds URL when prompted.
2. Run the script.
3. The program will automatically retrieve the fighter’s profile from Wikipedia, BestFightOdds, and SportsData API.
4. The cleaned data, including fight odds, win/loss results, and fighter statistics, will be saved to a CSV file.
