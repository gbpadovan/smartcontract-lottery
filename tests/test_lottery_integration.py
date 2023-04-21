import time
from tqdm import tqdm
from brownie import accounts, config, network, Lottery, exceptions
from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS
)

from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest

"""
def test_get_entrance_fee():
    # arrange   
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()    
    lottery = deploy_lottery()
    # act
    # in development environtemnt:
        # 1 ETH = 2000 USD
        # usdEntryFee = 50 USD
        # usdEntryFee = 0.025 ETH (as 2000/1 == 50/x == 0.025 )
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # assert
    assert entrance_fee == expected_entrance_fee


def test_cant_enter_unless_started():
    # arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({'from':get_account(), 'value':lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account}) 
    # act  
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    # assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account}) 
    # act  
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({'from':account,})
    # assert
    # LOTTERY_STATE public lottery_state
    assert lottery.lottery_state() == 2 # lottery_state.CALCULATING_WINNER
"""
def test_can_pick_winner_correctly():
    # arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account}) 
    # act  
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})
    fund_with_link(lottery)

    transaction = lottery.endLottery({'from':account,})
    transaction.wait(1)
    # As we have to receive a callback, the Chainlink node may take some seconds to 
    # answer. Then we wait a couple seconds.
    for i in tqdm(range(60), ascii=True, desc="Waiting for callback"): 
        time.sleep(1)
    
    # assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

def main():
    test_can_pick_winner_correctly()