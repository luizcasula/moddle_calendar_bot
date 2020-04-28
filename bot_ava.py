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

    def getFile(self):
        file_in_path = self.getFileInPath()
        if(file_in_path  == False):
            self.downloadFile()
            file_name = self.renameFile()
            self.readIcsFile('{}.ics'.format(file_name))
            
        elif(self.calculateDeltaTime(file_in_path)):
            self.readIcsFile(file_in_path)
        else:
            self.deleteFile(file_in_path)
            self.getFile()

    def downloadFile(self):
        try:
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
            print('download file sucessful')
        except:
            print('download file error')
        
    def getFileInPath(self):
        path = DATA_PATH
        for p, _, files in os.walk(os.path.abspath(path)):
            if (len(files) == 0):
                return False
            else:
                for file in files:
                    print(os.path.join(file))
                    if(len(files) == 1):
                        return os.path.join(file)
                    #else:
                        #delete older file
                        #return newest file
                    
    
    def readIcsFile(self, file_name):
        try:
            file = open('data/{}'.format(file_name),'rb')
            calendar = Calendar.from_ical(file.read())
            print('file {} opened'.format(file_name))
            for component in calendar.walk():
                if component.name == "VEVENT":
                    print(component.get('summary'))
                    print(component.get('categories'))
                    #print(component.get('description'))
            file.close()
            print('file {} closed'.format(file_name))
        except:
            print('read file error')

    

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
        try:
            file_name = self.buildFileName()
            os.rename(r'{}\icalexport.ics'.format(DATA_PATH), r'{}\{}.ics'.format(DATA_PATH, file_name))
            print('rename file sucessful')
            return file_name
        except:
            print('rename file error')

    def deleteFile(self, file_name):
        try:
            os.remove(r'{}\{}'.format(DATA_PATH, file_name))
            print('delete file sucessful')
        except:
            print('delete file error')


    def calculateDeltaTime(self, name):
        print(name)
        #tratar string
        name = name.split('.ics')
        print(name[0])
        date_file = datetime.fromtimestamp(float(name[0]))
        now = datetime.now()
        delta = now - date_file
        print(delta)
        print(delta.total_seconds())

        if(delta.total_seconds() < 20):
            return True
        else:
            return False


bot = Bot(secret.USERNAME, secret.PASSWORD)
bot.getFile()       
