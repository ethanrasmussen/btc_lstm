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
        pass

    def quit_driver(self):
        self.driver.quit()
        self.driver = None

    def get_dashboard_stats(self):
        pass #go to dashboard & get the stats on challenge acc snapshot

    def open_options_simulator(self):
        pass #open sim page & nav to BTC options

    def purchase_option(self):
        pass #buy or sell 1 single option

    def flatten_all_positions(self):
        pass #flatten all active/working positions

    def get_current_condor_value(self):
        pass #do math to get value of all open positions

    def build_iron_condor(self):
        pass #buy normal iron condor (stay in range)

    def build_reverse_condor(self):
        pass #buy reverse IC (exit range)

    def build_straddle(self):
        pass #make straddle (exit range/strike range)