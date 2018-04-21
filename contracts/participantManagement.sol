pragma solidity ^0.4.21;

//import "./OrganizerGovernance.sol";

library SafeMath {

  function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {
    if (a == 0) {
      return 0;
    }
    c = a * b;
    assert(c / a == b);
    return c;
  }

  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    return a / b;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
    c = a + b;
    assert(c >= a);
    return c;
  }
}

interface IOrganizerGovernance {
    function isOrganizer(address to_check) constant external returns(bool);
}

contract participantManagement {
  using SafeMath for uint256;
  mapping(uint => address) participantByDatabaseId;
  mapping(address => uint256) hackatokenBalance;
  
  IOrganizerGovernance governanceContract;
  
  modifier onlyOrganizer() {
        require(governanceContract.isOrganizer(msg.sender), "Only an organizer can do that.");
        _;
    }
    
  constructor(address _governanceContract) public {
        governanceContract = IOrganizerGovernance(_governanceContract);
    }
    
  function balanceOf(address holder) constant public returns(uint) {
      return hackatokenBalance[holder];
  }
  
  function giveTokens(address receiver, uint amount) onlyOrganizer public {
      hackatokenBalance[receiver] = hackatokenBalance[receiver].add(amount);
  }
  
  function slashTokens(address receiver, uint amount) onlyOrganizer public {
      hackatokenBalance[receiver] = hackatokenBalance[receiver].sub(amount);
  }
  
  function makePurchase(uint amount) public {
      hackatokenBalance[msg.sender] = hackatokenBalance[msg.sender].sub(amount);
  }
      
}