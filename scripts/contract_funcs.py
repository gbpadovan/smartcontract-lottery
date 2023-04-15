from brownie import Lottery
from scripts.helpful_scripts import get_account
from scripts.deploy_lottery import deploy_lottery


def get_acc():
    account = get_account(id='g-account')
    return 'ok'


def get_prices():
    account = get_account() 
    if not Lottery:        
        lottery = deploy_lottery()
    else:
        lottery = Lottery[-1]                       # compiled contract
       
    normal_price = lottery.getNormalPrice()
    adjusted_price = lottery.getAdjustedPrice()
    entrance_fee = lottery.getEntranceFee()         # calls function getEntranceFee() from Lottery.sol
    print(f"Normal price: {normal_price}",'\n')
    print(f"Adjusted price: {adjusted_price}",'\n')
    print(f"Entrance fee: {entrance_fee}")      
    return


def main():
    #get_prices()
    get_acc()
    return