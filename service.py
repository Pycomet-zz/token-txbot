from audioop import add
from bdb import set_trace
import requests
import json
import time
from config import *
from models import Token
from utils import *

class APISource:

    def __init__(self, symbol) -> None:
        self.api_key = WEB3_API_KEY
        self.address = ""
        self.symbol = symbol

    def get_abi(self):
        "Fetch Token ABI from EtherScan API"

        result = requests.get(
            f"https://api.etherscan.io/api?module=contract&action=getabi&address={self.address}&apikey={self.api_key}",
        ).json()
        return result['result']


    def fetch_contract(self, address:str):
        "Fetch the contract details (ABI)"
        self.address = Web3.toChecksumAddress(address)
        self.abi = json.loads(self.get_abi())
        return "Done"
    

    def fetch_tx(self):
        "Initialize Web3 Connection"
        # import pdb; pdb.set_trace()
        self.web3 = Web3(Web3.HTTPProvider(NODE_PROVIDER))

        if self.web3.isConnected() == True:

            #fetch addr transaction
            # addr = Web3.toChecksumAddress('0x2b591e99afe9f32eaa6214f7b7629768c40eeb39')
            addr = Web3.toChecksumAddress(self.address)

            self.token_contract = self.web3.eth.contract(address=addr, abi=self.abi) 
            
            while True:
                filter = self.token_contract.events.Transfer().createFilter(fromBlock='latest')

                txs = filter.get_new_entries()
                # import pdb; pdb.set_trace()
                if len(txs) > 0:
                    return [txs[i]['transactionHash'] for i in range(len(txs))]
                else:
                    print(txs)
                    time.sleep(120)
                    continue


        else:
            return False

    def get_token(self, address:str):
        "Fetch Token ABI and symbol"
        # addr = Web3.isChecksumAddress(address)
        # abi = json.loads(self.get_abi())

        # contract = self.web3.eth.contract(address=address, abi=abi)
        # symbol = contract.functions.symbol().call()

        result = requests.get(
            f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{address}",
        ).json()
        price_eth = result['market_data']['current_price']['eth']
        symbol = result['symbol']

        return price_eth, symbol.upper()


    def fetch_data(self, tx:str):
        "Fetches the Data Information From The Page"
        # token = Token(self.symbol, self.address)

        #Pull Token TX
        # data = pull_tx_info(tx, token)

        tx_data =  self.web3.eth.get_transaction_receipt(tx)
        tx_logs = self.token_contract.events.Transfer().processReceipt(tx_data)

        input_log = {}
        output_log = {}

        try:
            # Get Input And Output Logs
            for log in tx_logs:
                # index = tx_logs.index(log) + 1
                if tx_data['from'] == log['args']['from']:
                    input_log = log

                elif tx_data['from'] == log['args']['to']:
                    output_log = log
                else:
                    pass
        except Exception as e:
            print(e)
            return None

        print(input_log)
        print(output_log)

        if output_log == {} and input_log != {}:
            output_log['address'] = self.address
            output_log['args'] = {}
            output_log['args']['tokens'] = input_log['args']['tokens']

        elif output_log != {} and input_log == {}:
            input_log['address'] = self.address
            input_log['args'] = {}
            input_log['args']['tokens'] = output_log['args']['tokens']
         

        elif output_log == {} or input_log == {}:
            return None

        else:

            # Inptu value and Token
            price_per_eth, input_symbol = self.get_token(
                address=input_log['address']
            )
            spent_val =  float(input_log['args']['tokens']) / float(price_per_eth)
            spent = f"{spent_val} {input_symbol}"

            if input_symbol == self.symbol:
                trade = "SELL"
            else:
                trade = "BUY"


            price_per_unit, output_symbol = self.get_token(output_log['address'])
            got_value = float(output_log['args']['tokens']) / float(price_per_unit)
            got = f"{got_value} {output_symbol}"

            fee_wei = tx_data['gasUsed'] * tx_data['effectiveGasPrice']
            fee = self.web3.fromWei(fee_wei, 'ether')

            data = {
                "trade": trade,
                "spent": spent,
                "got": got,
                "fee": f"{fee} Eth",
                "position": "New",
                "market-cap": ""   
            }
            return data


    
        

    def write_channel_to_json(self, name:str, id:str):
        "Write New Channel to Database"
        file = open(f'{cwd}/sources.json')
        data = json.load(file)

        # new channel
        data['channels'].append({
            'Group Name': name,
            'Group Id': id
        })
        with open(f'{cwd}/sources.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.close()



