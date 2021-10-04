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
    options.add_argument('--log-level=3')
    options.add_argument('--headless')

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
    sunset = browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/w-answer/w-answer-desktop/div[1]').text

    # Formats information
    sunrise = '0' + sunrise[:1] + sunrise[2:4]
    str1 = sunset[:1]
    str1 = str(int(str1) + 12)
    sunset = str1 + sunset[1:]
    sunset = sunset[:2] + sunset[3:5]
    return_weather_data = (f'Sunrise: {sunrise}, Sunset: {sunset}\n')

    # Goes to new page
    browser.get('https://www.google.com/search?q=new+london+weather+tomorrow')

    # Same timeout clause
    timeout = 10
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="wob_dts"]')))
    except TimeoutException:
        browser.quit()
        return ("Weather Timed out (make sure you're connected to the internet and try again)\n")

    # Gets information
    high = browser.find_element_by_xpath('//*[@id="wob_dp"]/div[2]/div[3]/div[1]/span[1]').text
    low = browser.find_element_by_xpath('//*[@id="wob_dp"]/div[2]/div[3]/div[2]/span[1]').text
    precip = browser.find_element_by_xpath('//*[@id="wob_pp"]').text
    weather = browser.find_element_by_xpath('//*[@id="wob_dc"]').text

    # Formats information
    return_weather_data += (f'High: {high}, Low: {low}\n')
    return_weather_data += (f'Weather: {weather}\n')
    return_weather_data += (f'Chance of precipitation: {precip}\n')

    # Exits browser and returns
    browser.quit()
    return return_weather_data


# Function to scrape duty information from locally referenced csv
def getDuty():

    fileName = 'dutyScheduleF2021.csv'

    # Sets working directory to script's directory
    os.chdir(os.path.dirname(sys.argv[0]))

    # Can be modified to adjust relative path
    with open('../resources/' + fileName, 'r') as csv_file:

        # Expecting comma delimiter by default
        csv_reader = csv.reader(csv_file)

        # Finds line with matching date
        for line in csv_reader:

            if(line[0] != ''):
                print(line)

                # One day offset so it gets the next day's duty section
                today = datetime.today() + timedelta(days=1)
                
                # This has to match the formatting of the date on the roster
                today = today.strftime("%Y-%m-%d")
                if(today[0] == '0'):
                    today = today[1:]
                print(today)

                if today == line[1]:

                    # The classes are assumed here, if a 2/c stands in for RCDO it'll still say 1/c
                    # Kind of gnarly, the csv list delimitates on commas OR QUOTES, and delimitates the quotes, which is badass.
                    return_duty_data = (f'Duty Section: {line[2]} \n')
                    return_duty_data += (f'RCDO: 1/c {line[3]} \n')
                    return_duty_data += (f'ACDO: 2/c {line[4]} \n')
                    return_duty_data += (f'CIC: 2/c {line[5]} \n')
                    return_duty_data += (f'LHDO: 2/c {line[6]} \n')
                    return_duty_data += (f'JCDO: 3/c {line[7]} and 3/c {line[8]} \n')
                    return_duty_data += (f'LDO: 3/c {line[9]} \n')
                    if line[11].isspace() or not line[11]:
                        return_duty_data += (f'MHDO: 2/c {line[10]} \n')
                    else:
                        return_duty_data += (f'MHDO: 2/c {line[10]} and 2/c {line[11]} \n')

                    # Only a few values were filled, but why not
                    try:
                        if line[12].isspace() or not line[12]:
                            return_duty_data += 'Special Notes: none\n'
                        else:
                            return_daty_data += (f'Special Notes: {line[12]} \n')
                    except IndexError:
                        return_duty_data += 'Special Notes: none\n'
                    return return_duty_data


# Function for the UOD based on weekday
def getUOD():

    # Hard coded to winter uniforms for now, just need the dates we switch for comparison (or we could do a button)
    weekday = (datetime.now() + timedelta(days=1)).strftime('%A')
    if weekday == 'Friday':
        return 'Uniform: Long Sleeve Tropical Blue Uniforms with Garrison Covers\n'
    elif weekday == 'Saturday' or weekday == 'Sunday':
        return 'Uniform: Service Dress Bravos with Combination Covers\n'
    else:
        return 'Uniform: Operational Dress Uniforms with Class Specific Ballcaps\n'



# Uncomment these function calls to run this script from the CLI
# print(getWeather())
# print(getDuty())
# print('CAUTION, DEFAULT UNIFORM FOR WEEKDAY:\t' + getUOD())
