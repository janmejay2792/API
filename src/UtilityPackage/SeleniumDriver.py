"""
Customized Selenium WebDriver class which contains all the useful methods that can be re used.
These methods help to in the following cases:
To reduce the time required to write automation script.
To take the screenshot in case of test case failure.
To log
To provide waits

"""

import logging
import os
import time
from traceback import print_stack
from pathlib import Path
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import UtilityPackage.CustomLogger as cl
from _ast import If, Try


class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")
            print("### Exception Occurred when taking screenshot")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + 
                          " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_elements(byType, locator) 
            print(len(element))
            self.log.info("Element found with locator: " + locator + 
                          " and  locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator + 
                          " and  locatorType: " + locatorType)
        return element

    def elementClick(self, locator, locatorType="id", index=0):
        try:
            if locatorType == "text":
                # Pass Text as Locator field
                self.waitForElement("//*[text()='{text}']".format(text=locator), locatorType)
                element = self.driver.find_element_by_xpath("//*[text()='{text}']".format(text=locator))
                element.click()
                self.log.info("Element found with Test: " + locator + 
                          " and  locatorType: " + locatorType)
            else:
                self.waitForElement(locator, locatorType)
                element = self.getElement(locator, locatorType)[index]
                element.click()
            self.log.info("Clicked on element with locator: " + locator + 
                          " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + 
                          " locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator, locatorType="id", index=0):
        try:
            self.waitForElement(locator, locatorType)
            element = self.getElement(locator, locatorType)[index]
            element.send_keys(data)
            self.log.info("Sent data on element with locator: " + locator + 
                          " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator + 
                  " locatorType: " + locatorType)
            print_stack()

    def isElementPresent(self, locator, locatorType="id"):
        try:
            self.waitForElement(locator, locatorType)
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element present with locator: " + locator + 
                              " locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not present with locator: " + locator + 
                              " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element present with locator: " + locator + 
                              " locatorType: " + str(byType))
                return True
            else:
                self.log.info("Element not present with locator: " + locator + 
                              " locatorType: " + str(byType))
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType="id",
                               timeout=10, pollFrequency=0.5, data=""):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) + 
                  " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, 15, poll_frequency=2,
                                 ignored_exceptions=[NoSuchElementException, ElementNotInteractableException,
                                                     ElementNotVisibleException, StaleElementReferenceException,
                                                     ElementNotSelectableException])
            if data:
                element = wait.until(EC.visibility_of_element_located(byType,
                                                            locator))
            elif locatorType == "text": 
                element = wait.until(EC.element_to_be_clickable(By.XPATH,
                                                             "//*[text()='{text}']".format(text=locator)))
            else:
                element = wait.until(EC.element_to_be_clickable(byType,
                                                             locator))
#             element = wait.until(EC.element_to_be_clickable((byType,
#                                                              "stopFilter_stops-0")))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
#             print_stack()
        return element
    
    def get_project_root(self, packagenName1, fileName1) -> Path:
        return str(Path(__file__).parent.parent.joinpath(packagenName1).joinpath(fileName1))
