import time
from web3.contract import ConciseContract

BLOCK_TIME = 5
PLACEHOLDER_ADDRESS = "0x" + "0"*40

class GovernanceHandler():

    def __init__(self, w3, contract_address, contract_abi):
        self.contract = w3.eth.contract(address=contract_address, abi=contract_abi, ContractFactoryClass=ConciseContract)
        self.w3 = w3

    def wait_for_receipt(self, tx_hash):
        print("Mining...")
        while not self.w3.eth.getTransactionReceipt(tx_hash):
            time.sleep(BLOCK_TIME)
        return self.w3.eth.getTransactionReceipt(tx_hash)

    def victory_base(self):
        return self.contract.victoryBase()

    def participation_base(self):
        return self.contract.participationBase()

    def organizers(self):
        return self.contract.getOrganizerList()

    def current_voting_type(self):
        return self.contract.getVotingType()

    def type_modifier(self, type_id):
        return self.contract.hackathonModifiers(type_id)

    def start_voting_add_organizer(self, organizer_address):
        tx_hash = self.contract.startVoting(
            1,
            self.w3.toChecksumAddress(organizer_address),
            0,
            0,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")

    def start_voting_remove_organizer(self, organizer_id):
        tx_hash = self.contract.startVoting(
            2,
            self.w3.toChecksumAddress(PLACEHOLDER_ADDRESS),
            organizer_id,
            0,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")

    def start_voting_change_victory_base(self, new_value):
        tx_hash = self.contract.startVoting(
            3,
            self.w3.toChecksumAddress(PLACEHOLDER_ADDRESS),
            new_value,
            0,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")

    def start_voting_change_participation_base(self, new_value):
        tx_hash = self.contract.startVoting(
            4,
            self.w3.toChecksumAddress(PLACEHOLDER_ADDRESS),
            new_value,
            0,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")

    def start_voting_change_type_modifier(self, new_value, type_id):
        tx_hash = self.contract.startVoting(
            5,
            self.w3.toChecksumAddress(PLACEHOLDER_ADDRESS),
            new_value,
            type_id,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")

    def vote(self, isFor):
        tx_hash = self.contract.vote(
            isFor,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")