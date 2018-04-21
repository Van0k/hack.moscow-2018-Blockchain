pragma solidity ^0.4.0;

contract OrganizerGovernance {
    uint public victoryBase;
    uint public participationBase;
    address[] public organizers;
    uint[] public hackathonModifiers;
    mapping(address => bool) public isOrganizer;
    
    struct Voting {
        uint votes_for;
        uint votes_against;
        uint votingType;
        uint valueParam1;
        uint valueParam2;
        address addressParam;
        mapping(address => bool) voted;
        mapping(address => bool) vote;
    }
    
    Voting current_voting;
    bool isVoting = false;
    
    modifier onlyOrganizer {
        require(isOrganizer[msg.sender], "Only an organizer can do that.");
        _;
    }
    
    modifier onlyWhileVoting {
        require(isVoting, "You can only do that while voting is in effect.");
        _;
    }
    
    modifier onlyWhileNotVoting {
        require(!isVoting, "You can only do that while voting isn't in effect.");
        _;
    }
    
    constructor(uint[] modifiers, uint victoryBaseInitial, uint participationBaseInitial) public {
        
        addOrganizer(msg.sender);
        for(uint i; i < modifiers.length; i++) {
            hackathonModifiers.push(modifiers[i]);
        }
        victoryBase = victoryBaseInitial;
        participationBase = participationBaseInitial;
        
    }

    function getOrganizerList() constant public returns(address[])  {
        return organizers;
    }
    
    function getVotingType() constant public returns(uint) {
        if (isVoting) {
            return current_voting.votingType;
        }
        else {
            return 0;
        }
    }
    
    function addOrganizer(address organizer) private {
        organizers.push(organizer);
        isOrganizer[organizer] = true;
    }
    
    function removeOrganizer(uint organizerIdx) private {
        isOrganizer[organizers[organizerIdx]] = false;
        organizers[organizerIdx] = organizers[organizers.length-1];
        organizers.length--;
    }
    
    function changeVictoryBase(uint newValue) private {
        victoryBase = newValue;
    }
    
    function changeParticipationBase(uint newValue) private {
        participationBase = newValue;
    }
    
    function changeTypeModifier(uint newValue, uint typeId) private {
        hackathonModifiers[typeId] = newValue;
    }
    
    function startVoting(uint votingType, address addressParam, uint valueParam1, uint valueParam2) onlyOrganizer onlyWhileNotVoting public {
        
        current_voting = Voting({
            votes_for: 0,
            votes_against: 0,
            votingType: votingType,
            valueParam1: valueParam1,
            valueParam2: valueParam2,
            addressParam: addressParam
        });
        isVoting = true;
    }
    
    function vote(bool isFor) onlyOrganizer onlyWhileVoting public {
        if (current_voting.voted[msg.sender] == true) {
            revert("You have already voted");
        }
        
        if (isFor) {
            current_voting.votes_for++;
        } else {
            current_voting.votes_against++;
        }
        current_voting.voted[msg.sender] = true;
        current_voting.voted[msg.sender] = isFor;
        
        if (current_voting.votes_for > organizers.length/2 || current_voting.votes_against >= organizers.length/2) {
            finishVoting();
        }
    }
    
    function finishVoting() private {
        if (current_voting.votes_for > current_voting.votes_against) {
            uint valueParam1 = current_voting.valueParam1;
            uint valueParam2 = current_voting.valueParam2;
            address addressParam = current_voting.addressParam;
            
            if (current_voting.votingType == 1) {
                addOrganizer(addressParam);
            }
            if (current_voting.votingType == 2) {
                removeOrganizer(valueParam1);
            }
            if (current_voting.votingType == 3) {
                changeVictoryBase(valueParam1);
            }
            if (current_voting.votingType == 4) {
                changeParticipationBase(valueParam1);
            }
            if (current_voting.votingType == 5) {
                changeTypeModifier(valueParam1, valueParam2);
            }
            
            isVoting = false;
            for(uint i; i < organizers.length; i++) {
                current_voting.voted[organizers[i]] = false;
                current_voting.vote[organizers[i]] = false;
            }
        } else {
            isVoting = false;
            for(uint j; j < organizers.length; j++) {
                current_voting.voted[organizers[i]] = false;
                current_voting.vote[organizers[i]] = false;
            }
        }
    }
    
}