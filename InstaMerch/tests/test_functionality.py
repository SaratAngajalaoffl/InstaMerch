import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django.urls import reverse

class TestProjectListPage(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome('tests/chromedriver.exe')

    def tearDown(self):
        self.browser.quit()
    
    def test_signup_login(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/a[2]").click()
        time.sleep(1)
        self.browser.find_element_by_xpath("/html/body/div[2]/form/p[1]/input").send_keys("test_user")
        self.browser.find_element_by_xpath("/html/body/div[2]/form/p[2]/input").send_keys("test@gmail.com")
        self.browser.find_element_by_xpath("/html/body/div[2]/form/p[3]/input[1]").send_keys("fname")
        self.browser.find_element_by_xpath("/html/body/div[2]/form/p[3]/input[2]").send_keys("lname")
        self.browser.find_element_by_xpath("/html/body/div[2]/form/p[4]/input").send_keys("Password@123")
        self.browser.find_element_by_xpath("/html/body/div[2]/form/p[5]/input").send_keys("Password@123")
        self.browser.find_element_by_xpath("/html/body/div[2]/form/input[2]").click()
        time.sleep(1)
        self.browser.find_element_by_xpath("/html/body/div/a").click()
        time.sleep(1)
        
        assert self.browser.current_url == self.live_server_url+reverse('dashboard')
        
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/a[3]").click()
        time.sleep(1)
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/a[1]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('/html/body/div[2]/form/p[1]/input').send_keys("test_user")
        self.browser.find_element_by_xpath('/html/body/div[2]/form/p[2]/input').send_keys("Password@123")
        self.browser.find_element_by_xpath("/html/body/div[2]/form/p[3]/input").click()
        self.assertEquals(self.browser.current_url,self.live_server_url+"/")    
