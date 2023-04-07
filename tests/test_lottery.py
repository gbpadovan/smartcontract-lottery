from brownie import accounts, config, network, Lottery
from web3 import Web3


# current eth price 1873.40/USD
# ETH qty equivalent to 50 USD = 50 / 1873.40 = 0,026 ETH
# 0.0266894416568805 ETH in WEI = 26000000000000000 WEI

def test_get_entrance_fee():
    account = accounts[0]
    price_feed = config['networks'][network.show_active()]['eth_usd_price_feed']
    lottery = Lottery.deploy(price_feed,{"from":account,})

    assert entrance_fee > Web3.toWei(0.026, "ether")
    assert entrance_fee < Web3.toWei(0.030, "ether")

def main():
    test_get_entrance_fee()