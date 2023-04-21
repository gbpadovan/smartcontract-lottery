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

def test_get_entrance_fee():
    # arrange   
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
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
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # Act / assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({'from':get_account(), 'value':lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
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
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
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

def test_can_pick_winner_correctly():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({'from':account}) 
    # act  
    lottery.enter({'from':account, 'value':lottery.getEntranceFee()})               # account[0]
    lottery.enter({'from':get_account(index=1), 'value':lottery.getEntranceFee()})  # account[1]
    lottery.enter({'from':get_account(index=2), 'value':lottery.getEntranceFee()})  # account[2]
    fund_with_link(lottery)
    transaction = lottery.endLottery({'from':account,})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    STATIC_RNG = 777                                                                # 'random' number
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, 
        STATIC_RNG, 
        lottery.address,
        {'from':account}
        )   
    # logic for the winner: random number = 777, participants = 3
    # 777 % 3 = 0
    # the winner is account index=0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery

def main():
    test_get_entrance_fee()