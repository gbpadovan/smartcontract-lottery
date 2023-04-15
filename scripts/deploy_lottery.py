from brownie import network, config, Lottery
from scripts.helpful_scripts import get_account, get_contract, fund_with_link


def deploy_lottery():
    """Deploys contract Lottery.sol into a blockchain.

    The Lottery.sol contract has 5 constructor parameters:
    ----------------------------------------------------
        address _priceFeedAddress, 
        address _vrfCoordinator, 
        address _link,
        uint256 _fee,
        bytes32 _keyHash   
    ----------------------------------------------------
    """
    #account = get_account(id='g-account')
    account = get_account() 
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,           # _priceFeedAddress,
        get_contract("vrf_coordinator").address,              # _vrfCoordinator,
        get_contract("link_token").address,                   # _link,
        config["networks"][network.show_active()]["fee"],     # _fee,
        config["networks"][network.show_active()]["keyHash"], # _keyHash,        
        {'from':account}, 
        publish_source=config['networks'][network.show_active()].get('verify', False)
    )
    print(f"Contract deployed at: {lottery.address}")
    return lottery
    
def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({'from':account})
    starting_tx.wait(1)
    print("The lottery is started!")
    return

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    entrance_fee = lottery.getEntranceFee() + 100000000  # view function
    enter_tx = lottery.enter({'from':account, 'value':entrance_fee})
    enter_tx.wait(1)
    print("You entered the Lottery!")
    return

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    fund_with_link()
    end_tx = lottery.endLottery({'from':account})
    end_tx_tx.wait(1)
    print("Finished the Lottery!")
    return


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    return
