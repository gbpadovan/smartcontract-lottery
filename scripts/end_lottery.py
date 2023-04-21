from brownie import Lottery
from scripts.helpful_scripts import get_account, fund_with_link
import time
from tqdm import tqdm

assert Lottery

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    link_tx = fund_with_link(contract_address = lottery.address)
    ending_tx = lottery.endLottery({'from':account})
    ending_tx.wait(1)
    # As we have to receive a callback, the Chainlink node may take some seconds to 
    # answer. Then we wait a couple seconds.
    for i in tqdm(range(60), ascii=True, desc="Waiting for callback"): 
        time.sleep(1)
    print(f"{lottery.recentWinner()} is the recent winner!\n")
    print("Finished the Lottery!")
    return


def main():    
    end_lottery()
    return