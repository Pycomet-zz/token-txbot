from ast import Raise
from config import *
from service import APISource
from utils import *


# Business logic For Sending Out Blasts Here

def run():
    "Start Everything"

    file = open(f"{cwd}/source.json")
    data = json.load(file)

    # pull channels
    channels = data['channels']

    # pull token in models
    token = data['tokens'][0]
    client = APISource(token['symbol'])

    status = client.fetch_contract(token['address'])

    if status == "Done":

        while True:
            tx_ids = client.fetch_tx()

            if tx_ids in [False, []]:
                print("failed")
                pass

            else:
                for tx in tx_ids:
                    data = client.fetch_tx_info(tx)

                    for group in channels:
                        bot.send_message(
                            group['Group Id'],
                            f"""
                        {client.symbol} {data['trade']} !

                        Spent: {data['spent']}
                        Got: {data['got']}
                        Buyer Position: {data['position']}
                        Price: {data['fee']}
                        MCap: {data['market-cap']}
                        TX | Dex            
                            """
                        )




if __name__ == "__main__":
    run()