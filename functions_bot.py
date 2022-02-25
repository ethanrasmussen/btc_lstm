from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pathlib


class TradingBot:
    # TODO: get chromedriver

    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(executable_path='chromedriver.exe')

    def login(self):
        # get page
        self.driver.get('https://login.cmegroup.com/sso/accountstatus/showAuth.action')
        # send username
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div/form/ul/li[1]/input').send_keys(self.username)
        # send password
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div/form/ul/li[2]/input').send_keys(self.password)
        # click login button
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div/div[2]/div[1]/div/form/div[2]/button').click()
        # accept cookies
        time.sleep(2)
        # self.driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div[2]/div/div/button[2]').click()
        # # time.sleep(10)
        # # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div[3]/div/div/div[2]/div/div/button[2]')))
        # # self.driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div/div[2]/div/div/button[2]').click()
        # time.sleep(2)
        # self.driver.get('https://www.cmegroup.com/futures_challenge/dashboard')
        # # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/button[2]')))
        # # self.driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/button[2]').click()

    def quit_driver(self):
        self.driver.quit()
        self.driver = None

    def get_dashboard_stats(self):
        #go to dashboard & get the stats on challenge acc snapshot
        self.driver.get('https://www.cmegroup.com/futures_challenge/dashboard')
        # relogin
        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/div/div/nav/div/div/div[1]/div[2]/button/span').click()
        time.sleep(5)
        # access dashboard
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/p[2]/a').click()
        time.sleep(5)
        #
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[8]/a')))
        stats = {'working_orders': self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/span[2]').text,
                 'open_positions': self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/span[2]').text,
                 'balance': self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[4]/span[2]').text,
                 'margin': self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[5]/span[2]').text,
                 'you_control': self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[6]/span[2]').text,
                 'net_pl': self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[7]/span[2]').text}
        return stats

    def open_options_simulator(self):
        #open sim page & nav to BTC options
        self.driver.get('https://www.cmegroup.com/futures_challenge/dashboard')
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[8]/a')))
        self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div[2]/div/div/div[2]/div/div/div/div[8]/a').click()
        # select options
        #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/h1/div/span/span[2]/label[2]/input')))
        time.sleep(10)
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/h1/div/span/span[2]/label[2]').click()
        # select crypto
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div[2]/div/div/ul/li[8]/a').click()
        # select BTC
        #WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[8]/div/div/div/div[3]/div/div[1]/div[2]/div/div/div/div')))
        time.sleep(5)
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[8]/div/div/div/div[3]/div/div[1]/div[2]/div/div/div/div').click()

    def get_BTC_price(self):
        self.open_options_simulator()
        return self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div[2]/div/div/div/div[8]/div/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[2]/div[3]/div[1]').text

    def purchase_option(self):
        pass #buy or sell 1 single option

    def flatten_all_positions(self):
        pass #flatten all active/working positions

    def build_iron_condor(self):
        pass #buy normal iron condor (stay in range)

    def build_reverse_condor(self):
        pass #buy reverse IC (exit range)

    def build_straddle(self):
        pass #make straddle (exit range/strike range)