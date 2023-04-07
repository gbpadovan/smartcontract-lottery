from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3


FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache_gui']

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(force_deploy=False):
    """
    This function deploys MockV3Aggregator.sol to simulate 
    pricefeed.

    Observation:
    ------------
    The MockV3Aggregator contract has 2 constructor parameters:

    <_decimals> uint8
    <_initialAnswer> int256

       ----------------solidity code--------------------
                constructor(
                    uint8 _decimals,
                    int256 _initialAnswer
                ) public {
                    decimals = _decimals;
                    updateAnswer(_initialAnswer);
                }
     ----------------------------------------------------   
    Returns:
        None
    """
    print(f'The active network is {network.show_active()}')
    print(f'Deploying Mocks')
    
    if len(MockV3Aggregator) <=0 or force_deploy:
        _decimals = DECIMALS 
        #_initialAnswer = Web3.toWei(int(STARTING_PRICE),"ether") # 2000 x 10^18 = 2000000000000000000000
        _initialAnswer = STARTING_PRICE 
        # deploy:
        MockV3Aggregator.deploy(
            _decimals,        # constructor param
            _initialAnswer,   # constructor param
            {'from':get_account()},
        )
        print(f'( ͡❛ ͜ʖ ͡❛) ( ͡❛ ͜ʖ ͡❛) Mocks Deployed ( ͡❛ ͜ʖ ͡❛) ( ͡❛ ͜ʖ ͡❛)\n')        
    else:
        print(f'MockV3Aggregator is already deployed\n')
    return