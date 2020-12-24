# Imports all necessary functions from selenium, and DateTime
# Fully imports csv, it's a tiny library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import csv
import os
import sys

# Function for web scraping weather information
def getWeather():

    # Tells chromedriver to STFU, with varying success
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--headless")

    # Opens browser
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get('https://www.google.com/search?q=new+london+sunrise+sunset+tomorrow')

    # Waits for page to fully load, timeout value can be changed if you have a slow connection.
    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rso"]/div[1]/div/div[1]/w-answer[1]/w-answer-desktop/div[1]')))
    except TimeoutException:
        browser.quit()
        return ("Weather Timed out (make sure you're connected to the internet and try again)\n")

    # Gets information
    sunrise = browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/w-answer[1]/w-answer-desktop/div[1]').text
    sunrise = '0' + sunrise[:1] + sunrise[2:4]
    data = browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/w-answer/w-answer-desktop/div[1]')

    # Formats information
    title = data.text
    str1 = title[:1]
    str1 = str(int(str1) + 12)
    title = str1 + title[1:]
    title = title[:2] + title[3:5]
    return_weather_data = (f'Sunrise: {sunrise}, Sunset: {title}\n')

    # Goes to new page
    browser.get('https://www.google.com/search?q=new+london+weather+tomorrow')

    # Same timeout clause
    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wob_dts"]')))
    except TimeoutException:
        browser.quit()
        return ("Weather Timed out (make sure you're connected to the internet and try again)\n")

    # Gets info and formats return string as it goes
    high = browser.find_element_by_xpath('//*[@id="wob_dp"]/div[2]/div[3]/div[1]/span[1]').text
    low = browser.find_element_by_xpath('//*[@id="wob_dp"]/div[2]/div[3]/div[2]/span[1]').text
    return_weather_data += (f'High: {high}, Low: {low}') + '\n'
    return_weather_data += (browser.find_element_by_xpath('//*[@id="wob_dc"]').text) + '\n'
    precip = browser.find_element_by_xpath('//*[@id="wob_pp"]').text
    return_weather_data += (f'Chance of precipitation: {precip}') + '\n'

    # Exits browser and returns
    browser.quit()
    return return_weather_data


# Function to scrape duty information from locally referenced csv
def getDuty():

    # Sets working directory to script's directory
    os.chdir(os.path.dirname(sys.argv[0]))

    # Can be modified to adjust relative path
    with open('../resources/dutyScheduleF2020.csv', 'r') as csv_file:
        
        # Expecting comma delimiter by default
        csv_reader = csv.reader(csv_file)

        # Finds line with matching date
        for line in csv_reader:

            # Hard coding a 60 day offset so we can use the preexisting data
            today = datetime.today() - timedelta(days=60)
            today = today.strftime("%m/%d/%Y")
            if today == line[1]:

                # Kind of gnarly, the csv list delimitates on commas OR QUOTES, and delimitates the quotes, which is badass.
                return_duty_data = 'Duty Schedule: ' + line[2] + '\n'
                return_duty_data += 'RCDO: ' + line[3] + '\n'
                return_duty_data += 'ACDO: ' + line[4] + '\n'
                return_duty_data += 'CIC: ' + line[5] + '\n'
                return_duty_data += 'LHDO: ' + line[6] + '\n'
                return_duty_data += 'JCDO: ' + line[7] + ' and ' + line[8] + '\n'
                return_duty_data += 'LDO: ' + line[9] + '\n'
                return_duty_data += 'MHDO: ' + line[10] + ' and ' + line[11] + '\n'

                # Only a few values were filled, but why not
                try:
                    return_duty_data += 'Special Notes: ' + line[12] + '\n'
                except IndexError:
                    return_duty_data += 'Special Notes: none\n'
                return return_duty_data


# Function for the UOD based on weekday
def getUOD():

    # Hard coded to winter uniforms for now, just need the dates we switch for comparison (or we could do a button)
    weekday = (datetime.now() + timedelta(days=1)).strftime('%A')
    if weekday == 'Friday':
        return "Uniform: Long Sleeve Tropical Blue Uniforms with Garrison Covers\n"
    elif weekday == 'Saturday' or weekday == 'Sunday':
        return "Uniform: Service Dress Bravos with Combination Covers\n"
    else:
        return "Uniform: Operational Dress Uniforms with Class Specific Ballcaps\n"



# Uncomment these function calls to run this script from the CLI

# print(getWeather())
# print(getDuty())
# print('CAUTION, DEFAULT UNIFORM FOR WEEKDAY:\t' + getUOD())