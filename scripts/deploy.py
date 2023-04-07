from brownie import network, config, MockV3Aggregator, Lottery
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS, FORKED_LOCAL_ENVIRONMENTS


def deploy_lottery():
    """Deploys contract Lottery.sol into a blockchain.
    The Lottery.sol contract has 1 constructor parameters:

    <_priceFeed> address
    ----------------solidity code----------------------
    constructor(address _priceFeedAddress) public {
        // in WEI
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }
    ----------------------------------------------------
    """
    account = get_account()
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like goerli, use associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        contructor_param =  config['networks'][network.show_active()][
            'eth_usd_price_feed'                                         # _priceFeed
        ]                                                               
    else:
        deploy_mocks()
        contructor_param = MockV3Aggregator[-1].address

    lottery = Lottery.deploy(
        contructor_param,    # add _priceFeed into our FundMe.deploy() function 
        {'from':account}, 
        publish_source=config['networks'][network.show_active()].get('verify')
    )
    print(f"Contract deployed at: {lottery.address}")
    return lottery


def main():
    deploy_lottery()
    return
