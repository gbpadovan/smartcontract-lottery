// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;    


    constructor(address _priceFeedAddress) public {
        // in WEI
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function enter() public payable {
        // $50 USD minimum
        //require()
        players.push(msg.sender);
    }

    function getNormalPrice() public view returns(uint256){
        (, int price, , , ) = ethUsdPriceFeed.latestRoundData();        
        uint256 normalPrice =  uint256(price);
        return normalPrice;
    }

    function getAdjustedPrice() public view returns(uint256){
        (, int price, , , ) = ethUsdPriceFeed.latestRoundData();
        // adjusts price to 18 decimal places:
        // price has 8 decimal places, so we multiply it to 10^10
        // to reach 18 decimals.        
        uint256 adjustedPrice = uint256(price) * (10**10);
        return adjustedPrice;
    }    
    
     function getEntranceFee() public view returns (uint256) {
        (, int price, , ,) = ethUsdPriceFeed.latestRoundData();
        // adjusts price to 18 decimal places:
        // price has 8 decimal places, so we multiply it to 10^10
        // to reach 18 decimals.
        uint256 adjustedPrice = uint256(price) * (10**10);

        /*
        As the usdEntryFee and adjustedPrice have both 18 decimal places,
        once you divide one for the other, all decimal places will be canceled out.
        
        Ex:
        
        entrance fee in USD = 50000000000000000000 (50 USD)
        ETH price in USD = 2000000000000000000000
        
        >>> 50000000000000000000 / 2000000000000000000000 = 0.025
        
        The ammount 0.025 is the ETH quantity equivalennt to 50 USD, if 1 ETH = 2000 USD.
        
        In order to match the Units of Measure, which is in WEI, we have to
        convert 0.025 ETH to WEI. We do that by multiplying 0.025 for 10**18.
        
        >>> (0.025) * (10**18) = 25000000000000000 (WEI)
        
        The logic (iun non solidity language) can be:
        
        ethCostToEnter = usdEntryFee / adjustedPrice;
        weiCostToEnter = ethCostToEnter * (10**18)
        return weiCostToEnter
        
        We can achieve the same result by multiplying usdEntryFee by 10**18 
        before dividing by the adjustedPrice, as following:
        
        uint256 costToEnter = (usdEntryFee * 10**18) / (adjustedPrice);
        return costToEnter;
        
        */        
        uint256 costToEnter = (usdEntryFee * 10**18) / (adjustedPrice);
        return costToEnter;
    }

    function startLottery() public {}

    function endLottery() public {}

}