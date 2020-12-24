__POD Web Scraper__
==================

By: _Jstith_

## Overview

### How to use _(TLDR)_

- Run the `PODscraper.py` script
- Click the `Scrape POD Info` button __once__
- Wait for text to appear
- If something goes wrong, try the button again

### What is it?

The POD Web Scraper is a python based tool that lets users quickly and easily grab relevant information for creating the next day's POD. Built for windows and Linux with an easy to use GUI. Non-technical people can use this program too, it is literally click button, get information!

### What gets read?

All of the necessary weather information gets read from the following:

- https://www.google.com/search?q=new+london+sunrise+sunset+tomorrow
- https://www.google.com/search?q=new+london+weather+tomorrow

The duty information is scraped from a locally downloaded CVS file (the google sheet cannot be edited without disabling JavaScript, which seems like more trouble than it's worth since this sheet only changes once or twice per semester).

- `resources/dutyScheduleF2020.cvs`

**Please Note**: This is not the actually duty schedule, all of the names have been replaced with my hero for privacy.

The UOD is determined by checking what day of the week it is. Nothing fancy there.

## Python Stuff

### Dependencies

- Python3
- PIP:
  - `pip install selenium`
  - `pip install webdriver-manager`
  - `pip install DateTime`
  - `pip install os-sys`
  - `csv - included by default`
  - `tkinter - included by default`

### Selenium

I used selenium as my web scraper. As such, I needed a driver and used chromedriver. Originally, I downloaded the driver and tried to reference it locally, but the selenium is a nightmare when it comes to local referencing. Instead, I have the program download a new chromedriver to use. If you run the program more than once, it'll get cashed in your pycache, and the program should find it automatically. If you're particularly moved to get a local copy instead, you can install the correct chromedriver from https://chromedriver.chromium.org/.

#### Timeout errors

Sometimes selenium (or more aptly the chromedriver) times out when trying to connect to a website. I wrote in a 10 second timeout limit for each of the two connections. If you have slow internet and it keeps timing out, you can go into the `seleniumScraper.py` file and change the `timeout = 10` lines (two of them) to a longer time (such as 20).

### Scripts

The script that runs the GUI is `run/PODscraper.py`. The other file in the directory(`run/seleniumScraper.py`) can be used instead if you don't want the GUI. To do so, simply go in and uncomment the function calls at the bottom of the script.

```Python
print(getWeather())
print(getDuty())
print('CAUTION, DEFAULT UNIFORM FOR WEEKDAY:\t' + getUOD())
```

### Working Directory

The working directory gets set by the python script to the `Pod-Scraper/run` directory. If you want to change that or the relative path to the csv file for any reason, simply modify this code in `seleniumScraper.py`


```python
# Sets working directory to script's directory
os.chdir(os.path.dirname(sys.argv[0]))

# Can be modified to adjust relative path
with open('../resources/dutyScheduleF2020.csv', 'r') as csv_file:
```

## Future Goals

- Automate adding and removing announcements from their respective documents
- Scrape CHDO (requires .edu network access)
- Deploy to executable format or to web server
