from config import *
from models import Token
from typing import KeysView
from selenium import webdriver
import random
import time
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# # LOCAL SERVER WITH GECKODRIVER
# options = Options()
# options.headless = True

# driver = webdriver.Firefox()
# wait = WebDriverWait(driver, 10000) # Huge amount of delay response

##############


# # SERVER PROCESSING WITH CHROME DRIVER (HEROKU)
options = webdriver.ChromeOptions()

options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-sh-usage")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
wait = WebDriverWait(driver, 10000) # Huge amount of delay response

def pull_tx_info(tx:str, token:Token):
    "Fetch Data From EtherScan Website Page"

    print("Fetching Transaction Data ...")

    driver.get(f"https://etherscan.io/tx/{tx}")

    # import pdb; pdb.set_trace()

    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[5]/div[2]/ul/li/div/a[1]"))) # For page to load complete

    entry1 = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[5]/div[2]/ul/li/div/a[1]').text
    entry2 = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[5]/div[2]/ul/li/div/a[2]').text

    tx1_coin = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[8]/div[2]/ul/li[1]/div/span[6]/span').text
    
    dummy_text = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[8]/div[2]/ul/li[1]/div').text
    tx1_usd = dummy_text.split('(')[1].split(')')[0]
    tx1_symbol = dummy_text.split('(')[2].split(')')[0]

    tx2_coin = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[8]/div[2]/ul/li[2]/div/span[6]/span').text
    dummy_text = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[8]/div[2]/ul/li[2]/div').text
    tx2_usd = dummy_text.split('(')[1].split(')')[0]
    tx2_symbol = dummy_text.split('(')[2].split(')')[0]

    if entry1 == token.symbol:
        trade = "SELL"
    elif entry2 == token.symbol:
        trade = "BUY"

    if tx1_symbol == entry1:

        spent = f"{tx1_coin} {tx1_symbol} ({tx1_usd})"
        got = f"{tx2_coin} {tx2_symbol}"

    else:
        spent = f"{tx2_coin} {tx2_symbol} ({tx2_usd})"
        got = f"{tx1_coin} {tx1_symbol}"

    fee = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[10]/div/div[2]/span/span').text


    # TRADE / SPENT / GOT / POSITION / FEE / MCAP

    response = {
        "trade": trade,
        "spent": spent,
        "got": got,
        "fee": fee,
        "position": "New",
        "market-cap": ""
    }
    print(response)

    return response