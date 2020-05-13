

import unittest
import time
import pytest

from Laucher.LauchBrowser import LauchBrowser
from Pages.LoginPage import LoginPage
'''
Created on may 12, 2020
@author: janmejay.kumar
'''


class RegisterNow(LauchBrowser):
    global  driver

    @pytest.mark.run(order=1)
    def test_login(self):
        driver = self.setUp()
        login = LoginPage(driver)
        login.loginScenario()
    
    @pytest.mark.run(order=2)
    def test_login2(self):
        driver = self.setUp()
        login = LoginPage(driver)
        login.loginScenario()
        
#         


te = RegisterNow()
te.test_login()
# te.test_execute1()
