import time
from web3.contract import ConciseContract

BLOCK_TIME = 5
PLACEHOLDER_ADDRESS = "0x" + "0" * 40


class PMHandler():
    def __init__(self, w3, contract_address, contract_abi):
        self.contract = w3.eth.contract(address=contract_address, abi=contract_abi,
                                        ContractFactoryClass=ConciseContract)
        self.w3 = w3

    def wait_for_receipt(self, tx_hash):
        print("Mining...")
        while not self.w3.eth.getTransactionReceipt(tx_hash):
            time.sleep(BLOCK_TIME)
        return self.w3.eth.getTransactionReceipt(tx_hash)

    def balance_of(self, address):
        return self.contract.balanceOf(self.w3.toChecksumAddress(address))

    def give_tokens(self, receiver_address, amount):
        tx_hash = self.contract.giveTokens(
            self.w3.toChecksumAddress(receiver_address),
            amount,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")

    def slash_tokens(self, receiver_address, amount):
        tx_hash = self.contract.slashTokens(
            self.w3.toChecksumAddress(receiver_address),
            amount,
            transact={'from': self.w3.eth.accounts[0], 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")

    def make_purchase(self, spender_address, amount):
        tx_hash = self.contract.makePurchase(
            amount,
            transact={'from': self.w3.toChecksumAddress(spender_address), 'gas': 4100000}
        )
        self.wait_for_receipt(tx_hash)
        print("Done!")
