from UtilityPackage.SeleniumDriver import SeleniumDriver
from Laucher.LauchBrowser import LauchBrowser
import xml.dom.minidom
from pathlib import Path
'''
Created on may 12, 2020
@author: janmejay.kumar
'''


class LoginPage(SeleniumDriver):
    
    def __init__(self, driver):
        self.driver = driver
        
    _login_registerNow = "//*[contains(text(),'Register Now')]"
#     _logInToYourAccount = "//*[text()='Log in to Your Account']"
    _logInToYourAccount = "Log in to Your Account"
    _cancelGeneralError = "Cancel"
    _loginUserNAme = "Username"
    _loginPassword = "Password"
    _signIn = "Sign in"
    _signUpNow = "Sign up now"
    _userName = "logonIdentifier"
    _password = "newPassword"
    _confirmPassword = "reenterPassword"
    _email = "email"
    _firstName = "//*[text()='First Name']"
    _lastName = "//*[text()='Last Name"']'
    _checkTos = "tosCheck"
    _createBtn = "continueSignUp"
    
    def firstName(self, data):
        self.sendKeys(data, self._firstName, locatorType="xpath")

    def lastName(self, data):
        self.sendKeys(data, self._lastName, locatorType="xpath")

    def checkTos(self):
        self.elementClick(self._checkTos, locatorType="name")

    def createBtn(self):
        self.elementClick(self._createBtn, locatorType="id")
    
    def loginUserNAme(self, data):
        self.sendKeys(data, self._loginUserNAme, locatorType="name")

    def loginPassword(self, data):
        self.sendKeys(data, self._loginPassword , locatorType="name")

    def login_registerNow(self):
        self.elementClick(self._login_registerNow, locatorType="xpath")

    def sinInnBtn(self):
        self.elementClick(self._signIn, locatorType="text")

    def userName(self, data):
        self.sendKeys(data, self._userName, locatorType="id")

    def password(self, data):
        self.sendKeys(data, self._password, locatorType="id")

    def confirmPassword(self, data):
        self.sendKeys(data, self._confirmPassword, locatorType="id")

    def cancelGeneralError(self):
        self.elementClick(self._cancelGeneralError, locatorType="name")

    def email(self, data):
        self.sendKeys(data, self._email, locatorType="id")

    def logInToYourAccount(self):
        self.elementClick(self._logInToYourAccount, locatorType="text")

    def signUpNow(self):
        self.elementClick(self._signUpNow, locatorType="text")
        
    def loginScenario(self):
        self.driver.execute_script("window.scrollTo(0,300)")  # document.body.scrollHeight
        self.login_registerNow()
        self.logInToYourAccount()
        lau = LauchBrowser()
        launchToPlatform = lau.readJson("Browser", "LauchToSetUp")
        if launchToPlatform == "test_setUp_Desktop":
            self.cancelGeneralError()
            self.logInToYourAccount()
            self.loginUserNAme(self.readXML("UserName"))
        else:
            self.loginUserNAme(self.readXML("FirstName"))
        self.loginPassword(self.readXML("Password"))
        self.sinInnBtn()
        self.signUpNow()
        self.userName(self.readXML("UserName"))
        self.password(self.readXML("Password"))
        self.confirmPassword(self.readXML("Password"))
        self.email(self.readXML("Email"))
        self.firstName(self.readXML("FirstName"))
        self.lastName(self.readXML("LastName"))
        self.checkTos()
        self.createBtn()

    def readXML(self, attributeName):
        xmlpath = (self.get_project_root("PageObjectData", "LoginPageData.xml"))
        doc = xml.dom.minidom.parse(xmlpath)
        name = doc.getElementsByTagName(attributeName)[0]
        print(name.firstChild.data)
        return name.firstChild.data
  
