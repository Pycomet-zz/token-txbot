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
        web3 = Web3(Web3.HTTPProvider(NODE_PROVIDER))
        if web3.isConnected() == True:

            #fetch addr transaction
            # addr = Web3.toChecksumAddress('0x2b591e99afe9f32eaa6214f7b7629768c40eeb39')
            addr = Web3.toChecksumAddress(self.address)

            token_contract = web3.eth.contract(address=addr, abi=self.abi) 
            
            while True:
                filter = token_contract.events.Transfer.createFilter(fromBlock='latest')

                txs = filter.get_new_entries()
                if len(txs) > 0:
                    return [txs[i]['transactionHash'] for i in len(txs)]
                else:
                    print(txs)
                    time.sleep(10)
                    continue


        else:
            return False



    def fetch_tx_info(self, tx:str):
        "Fetches the Data Information From The Page"
        token = Token(self.symbol, self.address)

        #Pull Token TX
        data = pull_tx_info(tx, token)
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



