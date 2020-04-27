from selenium import webdriver
from time import sleep

from icalendar import Calendar, Event
from datetime import datetime
from pytz import UTC
import os
import time
import secret
import platform


DATA_PATH = r'C:\Users\lacft\Documents\Python Projects\AVA bot\moddle_calendar_bot\data'



class Bot:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        

    def getFilesInPath(self):
        path = DATA_PATH
        for p, _, files in os.walk(os.path.abspath(path)):
            for file in files:
                if len(files) == 1:
                    return os.path.join(file)
                else:
                    #delete older file
                    #return new file
                    print(os.path.join(file))

    def getFile(self):
        options = webdriver.ChromeOptions()
        preferences = {'download.default_directory': '{}'.format(DATA_PATH), 'safebrowsing.enable': 'false'}
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
        sleep(5)
        driver.quit()

    def readIcsFile(self, file_name):
        file = open('data/{}.ics'.format(file_name),'rb')
        calendar = Calendar.from_ical(file.read())
        for component in calendar.walk():
            if component.name == "VEVENT":
                print(component.get('summary'))
                print(component.get('categories'))
                print(component.get('description'))      
        file.close()

    def getLink(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()
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
        driver.find_element_by_xpath('//*[@id="id_generateurl"]').click()
        sleep(2)
        link = driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div').text
        driver.quit()
        return link

    def buildFileName(self):
        if platform.system == 'Windows':
            return os.path.getctime(DATA_PATH)
        else:
            stat = os.stat(DATA_PATH)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
                  
    def renameFile(self):
        file_name = self.buildFileName()
        sleep(3)
        os.rename(r'{}\icalexport.ics'.format(DATA_PATH), r'{}\{}.ics'.format(DATA_PATH, file_name))
        return file_name
        
    def deleteFile(self):
        file_name = '1587885349.6933017.ics'
        os.remove(r'{}\{}'.format(DATA_PATH, file_name))

    def convertTime(self, name):
        #name = self.getFileName()
        print(name)
        #print(datetime.fromtimestamp(name).strftime('%Y-%m-%d %H:%M:%S'))
        print(datetime.fromtimestamp(name))

    #def calculateTime(self):
        


bot = Bot(secret.USERNAME, secret.PASSWORD)

#bot.getFile()
#name = bot.getFilesInPath()
#file_name = bot.renameFile()
#bot.getFilesInPath()
#bot.readIcsFile(file_name)

bot.convertTime(1587941903.5602446)
