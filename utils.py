import webbrowser
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

def load_driver():
    # # LOCAL SERVER WITH GECKODRIVER
    if DEBUG == True:
        options = Options()
        options.headless = True

        driver = webdriver.Firefox()


    else:
        options = webdriver.FirefoxOptions()
        # enable trace level for debugging 
        options.log.level = "trace"

        options.add_argument("-remote-debugging-port=9224")
        options.add_argument("-headless")
        options.add_argument("-disable-gpu")
        options.add_argument("-no-sandbox")

        binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

        driver = webdriver.Firefox(
            firefox_binary=binary,
            executable_path=os.environ.get('GECKODRIVER_PATH'),
            options=options
        )

    return driver

##############


# # SERVER PROCESSING WITH CHROME DRIVER (HEROKU)
# options = webdriver.ChromeOptions()

# options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-sh-usage")

# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
# wait = WebDriverWait(driver, 10000) # Huge amount of delay response

def pull_tx_info(tx, token:Token):
    "Fetch Data From EtherScan Website Page"
    driver = load_driver()
    wait = WebDriverWait(driver, 100) # Huge amount of delay response

    print("Fetching Transaction Data ...")

    
    tx = tx.hex()
    print(tx)
    driver.get(f"https://etherscan.io/tx/{tx}")


    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="spanTxHash"]'))) # For page to load complete
    # time.sleep(20)

    try:
        entry1 = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[5]/div[2]/ul/li/div/a[1]').text

        entry2 = driver.find_element_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[5]/div[2]/ul/li/div/a[2]').text
    except Exception as e:
        pass
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
    else:
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