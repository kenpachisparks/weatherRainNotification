from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as soupCleanUp

import subprocess, sys, time

safariDriver = webdriver.Safari(port=0, executable_path="/usr/bin/safaridriver", quiet=False)

# Round Rock
# safariDriver.get("https://weather.com/weather/today/l/2c8d802ebb0d8711dbc9422d22ca32037e06cb6560f2e2c52ddb0ad2af21f90e")
weatherCity = input("Please enter the zip code or city name only then press return: ")

safariDriver.get("https://weather.com/")
WebDriverWait(safariDriver, 10).until(
    EC.element_to_be_clickable((By.ID, "LocationSearch_input")))
searchWebsiteItem = safariDriver.find_element_by_id("LocationSearch_input")
searchWebsiteItem.send_keys(weatherCity)
WebDriverWait(safariDriver, 10).until(
    EC.element_to_be_clickable((By.ID, "LocationSearch_listbox")))
searchWebsiteItem.click()
searchWebsiteItem.send_keys(Keys.RETURN)
searchWebsiteItem.send_keys(Keys.RETURN)
while True:
    WebDriverWait(safariDriver, 10).until(
        EC.element_to_be_clickable((By.ID, "WxuDailyWeatherCard-main-bb1a17e7-dc20-421a-b1b8-c117308c6626")))

    htmlWebScrap = safariDriver.page_source
    htmlWebScrap = soupCleanUp(htmlWebScrap, "lxml")


    def rainCheck(dateNum, dayWeatherArray, weatherSorted):

        dayOfTheWeek = dateNum[weatherSorted]
        lowTemp = dateNum[weatherSorted + 2]
        highTemp = dateNum[weatherSorted + 1]
        rainChance = dateNum[weatherSorted + 3]
        if int(rainChance[:-1]) > 11:
            dayWeatherArray.append(('\n' + str(rainChance) + ' chance of rain on ' + str(
                dayOfTheWeek) + ' and high temperature of ' + str(highTemp) + ' and a low temperature of ' + str(
                lowTemp) + '\n'))
        return dayWeatherArray


    dailyWeatherCard = htmlWebScrap.find_all('div', {'class': 'DailyWeatherCard--TableWrapper--12r1N'})
    dailyWeatherCardSplit = dailyWeatherCard[0].find_all('ul', {'class': 'WeatherTable--columns--3q5Nx'})
    dailyWeatherCardString = str(dailyWeatherCardSplit[0])
    soupUpWeather = soupCleanUp(dailyWeatherCardString, "html.parser")
    htmp = ([dailyWeatherCardString for dailyWeatherCardString in soupUpWeather.strings])

    todayWeather = []  # 0-4
    tonightWeather = []  # 5-9
    twoDaysFromNowWeather = []  # 10-14
    twoDaysFromNowNightWeather = []  # 15-19
    threeDaysFromNowWeather = []

    rainCollector = (
        rainCheck(htmp, todayWeather, 0) + rainCheck(htmp, tonightWeather, 4) + rainCheck(htmp, twoDaysFromNowWeather,
                                                                                               8) + rainCheck(htmp,
                                                                                                               twoDaysFromNowNightWeather,
                                                                                                               12),
        rainCheck(htmp, threeDaysFromNowWeather, 16))

    rainCollector = list(rainCollector)
    clearRainCollector = len(rainCollector) - 1
    rainCollectorResults = rainCollector[clearRainCollector]
    if not rainCollectorResults:
        del rainCollector[clearRainCollector]

    print(rainCollector)
    if not rainCollector:
        time.sleep(10)
        safariDriver.refresh()
    else:
        removeCharactersFromRainCollector = ['[', '\'', ']', ',']
        final = ''.join(i for i in str(rainCollector) if not i in removeCharactersFromRainCollector)

        appleScript = '''tell application "Messages"
    set theBuddy to buddy "noreply@github.com" of service id "84631HF5-84F1-A497-N168-135G468e79WP"
    send "''''Rain Alert:\n\n' + final + '''" to theBuddy
end tell
'''
        stageAppleScript = [item for rainCollectorResults in [("-e", splitUpRainCollector.strip()) for splitUpRainCollector in appleScript.split('\n') if splitUpRainCollector.strip() != ''] for item in rainCollectorResults]
        prepareAppleScript = subprocess.Popen(["osascript"] + stageAppleScript, stdout=subprocess.PIPE)
        finalAppleScript = prepareAppleScript.stdout.read().strip()
        sys.stdout.write(str(finalAppleScript))
        break
