from brownie import Lottery
from scripts.helpful_scripts import get_account


def get_prices():
    lottery = Lottery[-1]                    # compiled contract
    account = get_account()    
    normal_price = lottery.getNormalPrice()
    adjusted_price = lottery.getAdjustedPrice()
    entrance_fee = lottery.getEntranceFee()  # calls function getEntranceFee() from Lottery.sol
    print(f"Normal price: {normal_price}",'\n')
    print(f"Adjusted price: {adjusted_price}",'\n')
    print(f"Entrance fee: {entrance_fee}")      
    return


def main():
    get_prices()
    return