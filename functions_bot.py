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

    def get_options(self):
        self.open_options_simulator()
        # each strike contains price & last, with last = [call, put]
        modifiers = [-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10]
        options_list = {
            "strike-10": {
                'price': 0,
                'last': 0
            },
            "strike-9": {
                'price': 0,
                'last': 0
            },
            "strike-8": {
                'price': 0,
                'last': 0
            },
            "strike-7": {
                'price': 0,
                'last': 0
            },
            "strike-6": {
                'price': 0,
                'last': 0
            },
            "strike-5": {
                'price': 0,
                'last': 0
            },
            "strike-4": {
                'price': 0,
                'last': 0
            },
            "strike-3": {
                'price': 0,
                'last': 0
            },
            "strike-2": {
                'price': 0,
                'last': 0
            },
            "strike-1": {
                'price': 0,
                'last': 0
            },
            "strike": {
                'price': 0,
                'last': 0
            },
            "strike+1": {
                'price': 0,
                'last': 0
            },
            "strike+2": {
                'price': 0,
                'last': 0
            },
            "strike+3": {
                'price': 0,
                'last': 0
            },
            "strike+4": {
                'price': 0,
                'last': 0
            },
            "strike+5": {
                'price': 0,
                'last': 0
            },
            "strike+6": {
                'price': 0,
                'last': 0
            },
            "strike+7": {
                'price': 0,
                'last': 0
            },
            "strike+8": {
                'price': 0,
                'last': 0
            },
            "strike+9": {
                'price': 0,
                'last': 0
            },
            "strike+10": {
                'price': 0,
                'last': 0
            }
        }
        time.sleep(2)
        for m in range(len(modifiers)):
            md = modifiers[m]
            ind = m+1
            print(f"{ind}\n{md}")
            if md == 0:
                options_list['strike']['price'] = self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[7]/span').text
                options_list['strike']['last'] = [
                    self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[6]').text,
                    self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[8]').text]
            elif md < 0:
                options_list[f'strike{md}']['price'] = self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[7]/span').text
                options_list[f'strike{md}']['last'] = [
                    self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[6]').text,
                    self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[8]').text]
            elif md > 0:
                options_list[f'strike+{md}']['price'] = self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[7]/span').text
                options_list[f'strike+{md}']['last'] = [
                    self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[6]').text,
                    self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{ind}]/td[8]').text]
        return options_list

    def purchase_option(self, chain_index, buy, qty, call=False, put=False, on_chain=False):
        if call or put:
            if not on_chain:
                # don't reopen the sim if we don't need to
                self.open_options_simulator()
            time.sleep(2)
            self.driver.find_element_by_xpath(f'/html/body/div[3]/div/div/div[3]/div/div[3]/div/div[3]/div/div[2]/table/tbody/tr[{chain_index}]/td[7]/span').click()
            # enter quantity
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div[2]/input').send_keys(qty)
            # switch to MKT order
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div[1]/div/div/button').click()
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div[1]/div/div/ul/li[1]/a').click()
            # press button for call or put
            if call:
                self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[1]/div[4]/div[1]/div[3]/div[2]/div/span/label[2]').click()
            elif put:
                self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[1]/div[4]/div[1]/div[3]/div[2]/div/span/label[1]').click()
            # press button to buy or sell
            if buy:
                self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div[3]/div/span/label[1]').click()
            if not buy:
                self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[1]/div[4]/div[1]/div[1]/div[3]/div/span/label[2]').click()
            # press button to submit order
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div[2]/div[4]/div[2]/input[1]').click()
            # confirm order
            time.sleep(0.5)
            self.driver.find_element_by_xpath('/html/body/div[11]/div/div[2]/div[3]/button[1]').click()
            # close trade log tab
            time.sleep(0.5)
            self.driver.find_element_by_xpath('/html/body/div[11]/div/div[2]/div[2]/div/div[2]/input[1]').click()

    def flatten_all_positions(self):
        self.open_options_simulator()
        try:
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div/div[5]/div/div/div[1]/div/div/button').click()
        except:
            print("Couldn't find FLATTEN button. Possible that all positions are already flattened.")

    def build_iron_condor(self):
        # buy all 4 wings of the condor
        self.purchase_option(chain_index=7, buy=True, put=True, qty=1) #OTM put buy below strike
        self.purchase_option(chain_index=9, buy=False, put=True, on_chain=True, qty=1) #OTM/ATM put sell below strike (closer)
        self.purchase_option(chain_index=13, buy=False, call=True, on_chain=True, qty=1) #OTM/ATM call sell above strike (closer)
        self.purchase_option(chain_index=15, buy=True, call=True, on_chain=True, qty=1) #OTM call buy above strike

    def build_straddle(self):
        # buy 2 legs of straddle (x3!)
        self.purchase_option(chain_index=11, buy=True, call=True, qty=3) #long call at strike
        self.purchase_option(chain_index=11, buy=True, put=True, on_chain=True, qty=3) #long put at strike
        # TODO: due to margin requirements, it may be possible to, 1. decrease qty, and 2. use short straddles instead of ICs

    def choose_strategy(self, price_prediction):
        # do calculations to pick strategy based on price prediction & option chain
        options = self.get_options()
        portfolio_stats = self.get_dashboard_stats()
        # calculate profitable ranges for IC's (+- 5)
        ic_max_loss = (abs((int(options['strike+5']['last'][0]) - int(options['strike-5']['last'][0]))) * 5)
        ic_profitable_range = None
        # TODO
        # calculate profitable range for straddle at strike
        straddle_strike_max_loss = (int(options['strike']['last'][0]) + int(options['strike']['last'][1]) * 3 * 5)
        straddle_loss_range = None
        # TODO
        # pick strategy
        if int(price_prediction) in ic_profitable_range and int(price_prediction) not in [min(ic_profitable_range), max(ic_profitable_range)]:
            # if predicted price is within the IC profitable range, but not on the very edges, then IC strategy is best
            # TODO: expand the min/max ranges to capture a slightly wider field, use some sort of slicing
            strategy = "ironcondor"
        elif int(price_prediction) not in straddle_loss_range:
            # if predicted price not in IC profit range & not in straddle loss range, then straddle strategy makes sense
            # TODO: create a list of ranges slightly outside the loss range, to avoid being too close to the edges
            strategy = "straddle"
        elif int(price_prediction) in ic_profitable_range or int(price_prediction) not in straddle_loss_range:
            # this detects edge cases that fall either on the edges of the IC profit range or barely outside the straddle loss range
            if int(price_prediction) not in straddle_loss_range:
                # prioritize straddle if both cases are true, as straddle has higher profit potential (and simpler flatten/exit)
                strategy = "straddle"
            elif int(price_prediction) in ic_profitable_range:
                # if not straddle-eligible, then it will be IC-eligible
                strategy = "ironcondor"
        else:
            # if the number doesn't fall within any of our preferred ranges, we can simply choose the lowest max loss, provided max loss is less than 5% of portfolio
            max_allowed_loss = 0.05 * int(str(portfolio_stats['balance']).strip().replace('$',''))
            if ic_max_loss < max_allowed_loss and straddle_strike_max_loss < max_allowed_loss:
                # chooses lowest max loss if both below max allowed loss
                if ic_max_loss > straddle_strike_max_loss:
                    strategy = "straddle"
                elif straddle_strike_max_loss > ic_max_loss:
                    strategy = "ironcondor"
            elif min([ic_max_loss, straddle_strike_max_loss]) < max_allowed_loss:
                # if only one max loss below max allowed loss, select that one
                if ic_max_loss < max_allowed_loss:
                    strategy = "ironcondor"
                else:
                    strategy = "straddle"
            else:
                # if all else fails, neither strategy seems clear, and the max losses of both strats exceed max allowed loss, then we do nothing for the day
                strategy = "nothing"
        return strategy