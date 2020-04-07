from selenium import webdriver
from time import sleep

from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC
import os

DOWNLOAD_PATH = r''

class Bot:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getFileName(self):
        path = DOWNLOAD_PATH
        for p, _, files in os.walk(os.path.abspath(path)):
            for file in files:
                print(os.path.join(p, file))

    def getFile(self):
        options = webdriver.ChromeOptions()
        preferences = {'download.default_directory': '{}'.format(DOWNLOAD_PATH), 'safebrowsing.enable': 'false'}
        options.add_experimental_option("prefs", preferences)
        driver = webdriver.Chrome(chrome_options=options)
        driver.get('https://virtual.ifro.edu.br/jiparana/calendar/export.php')
        sleep(2)
        driver.find_element_by_xpath('//*[@id="username"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="loginbtn"]').click()
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_events_exportevents_all"]').click()
        driver.find_element_by_xpath('//*[@id="id_period_timeperiod_recentupcoming"]').click()
        sleep(2)
        driver.find_element_by_xpath('//*[@id="id_export"]').click()
        

    def readIcsFile(self):
        file = open('icalexport.ics','rb')
        calendar = Calendar.from_ical(file.read())
        for component in calendar.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                print(component.get('categories'))
                print(component.get('description'))      
        file.close()
            
bot = Bot('', '')
#bot.getFile()
#bot.readIcsFile()
bot.getFileName()


