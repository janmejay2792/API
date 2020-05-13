'''
Created on may 12, 2020
@author: janmejay.kumar
'''

import json
import os
import time
import pytest
from pathlib import Path
from UtilityPackage.SeleniumDriver import SeleniumDriver
import unittest
 

class LauchBrowser():
    global driver , driverA, chromePath, launchToPlatform

#     @pytest.fixture(param=["test_setUp_Desktop", "test_setUp_Android"])
#     def crossBrowser(self, request):
#         return request.param
#     
#     def test_A(self, crossBrowser):
#         print(crossBrowser)
    
    def setUp(self):
        launchToPlatform = self.readJson("Browser", "LauchToSetUp")
#         launchToPlatform = crossBrowser
        print(launchToPlatform)
        if launchToPlatform == "test_setUp_Android":
            self.test_setUp_Android()
            driverA = self.getDriverA_test()
            return driverA
        elif launchToPlatform == "test_setUp_Desktop":
            self.test_setUp_Desktop()
            driver = self.getDriver_test()
            return driver
    
    def test_setUp_Desktop(self):
        from selenium import webdriver
        self.driver = webdriver.Chrome(executable_path=self.get_project_root("driver", "chromedriver.exe"))
        path = os.path.dirname(os.path.abspath("Browser.json"))
        print(path)
        data = self.readJson("Browser", "URL")
        self.driver.get(data)
        self.driver.maximize_window()
        SeleniumDriver(self.driver).elementClick(self.readJson("Browser", "cookiesHandle"), locatorType="id")
        print("Auto Cookies Clicked")
        self.driver.implicitly_wait(3)
        
    def test_setUp_Android(self):
        from appium import webdriver
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'emulator-5554'
        desired_caps['chromedriverExecutable'] = chromePath
        desired_caps['browserName'] = 'Chrome'
        desired_caps ['chrome.binary'] = self.get_project_root("driver", "chromedriver.exe")
        self.driverA = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        data = self.readJson("Browser", "URL")
        self.driverA.get(data)
        SeleniumDriver(self.driverA).waitForElement(self.readJson("Browser", "cookiesHandle"), locatorType="id")
        SeleniumDriver(self.driverA).elementClick(self.readJson("Browser", "cookiesHandle"), locatorType="id")
        print("Auto Cookies Clicked")
        self.driverA.implicitly_wait(3)
        
    def getDriver_test(self):
        return self.driver

    def getDriverA_test(self):
        return self.driverA

#     
    def readJson(self, fileN, attribute):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(ROOT_DIR, fileN + ".json")
        f = open(CONFIG_PATH ,)  # "D://Python//PythonSeleniumProject//PyDevSelenium//src//Laucher//"
        data1 = json.load(f)
        data = data1[attribute]
        return data
 
    def get_project_root(self, packagenName1, fileName1) -> Path:
        return str(Path(__file__).parent.parent.joinpath(packagenName1).joinpath(fileName1))

