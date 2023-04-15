from brownie import (
    accounts, 
    network, 
    config, 
    MockV3Aggregator, 
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface
)


FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache_gui']

DECIMALS = 8
STARTING_PRICE = 200000000000 # in GWEI
LINK_FEE = 100000000000000000 # in LINK, with 18 decimal places

contract_to_mock = {
    "eth_usd_price_feed":MockV3Aggregator,
    "vrf_coordinator":VRFCoordinatorMock,
    "link_token":LinkToken,
}


def get_account(index=None, id=None):
    if index: 
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]    
 
    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    """
    Deploy all mock versions of V3Aggregator, LinkToken & VRFCoordinator

    Returns:
        None
    """
    print(f'The active network is {network.show_active()}\nDeploying Mocks')
    MockV3Aggregator.deploy(
        decimals,                                         # constructor param
        initial_value,                                    # constructor param
        {'from':get_account()},
    )    
    link_token = LinkToken.deploy({'from':get_account()}) # no constructor param
    VRFCoordinatorMock.deploy(
        link_token.address,                               # constructor param     
        {'from':get_account()},
    )
    print(f'( ͡❛ ͜ʖ ͡❛) ( ͡❛ ͜ʖ ͡❛) Mocks Deployed ( ͡❛ ͜ʖ ͡❛) ( ͡❛ ͜ʖ ͡❛)\n')
    return


def get_contract(contract_name):
    """This function will grab the contract address from the brownie config
    if defined, otherwise it will deploy a mock version of that contract, and
    return that contract

        Args:
            contract_name: str

        Returns:
            brownie.network.contract.ProjectContract: the most recently deployed
            version of this contract
    """
    contract_type = contract_to_mock[contract_name]
    
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0: # it means that contract was not yet deployed
            deploy_mocks()
        contract = contract_type[-1] # after deployment, get the contract
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        # address
        # abi
        contract = Contract.from_abi(
            contract_type.__name__, contract_address, contract_type.abi
        )
    return contract


def fund_with_link(contract_address, account=None, link_token=None, ammount=LINK_FEE):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, ammount, {"from":account})
    #link_token_contract = interface.LinkTokenInterface(link_token.address)
    #tx = link_token_contract.transfer(contract_address, ammount, {"from":account})
    tx.wait(1)
    print("Fund Contract!")
    return tx