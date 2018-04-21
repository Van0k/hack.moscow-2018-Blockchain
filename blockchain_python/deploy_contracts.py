import json
import web3
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import Contract, ConciseContract
from web3.middleware import geth_poa_middleware

PLACEHOLDER_ADDRESS = "0x" + "0"*40
BLOCK_TIME = 5
TYPE_MODIFIERS = [1, 2, 3, 4]
VICTORY_BASE = 100
PARTICIPATION_BASE = 10
NODE_HOST = '127.0.0.1'
NODE_PORT = '8501'

GOVERNANCE_SOURCE = '../contracts/OrganizerGovernance.sol'
PM_SOURCE = '../contracts/participantManagement.sol'

w3 = Web3(HTTPProvider(f'http://{NODE_HOST}:{NODE_PORT}'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)


def wait_for_receipt(tx_hash):
    print("Mining")
    while not w3.eth.getTransactionReceipt(tx_hash):
        time.sleep(BLOCK_TIME)
    return w3.eth.getTransactionReceipt(tx_hash)

def deploy_governance(type_modifiers, victory_base, participation_base, source):
    with open(source) as f:
        contract_source_code = f.read()

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:OrganizerGovernance']
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.constructor(type_modifiers, victory_base, participation_base).transact(
        transaction={'from': w3.eth.accounts[0], 'gas': 4100000}
    )
    tx_receipt = wait_for_receipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    abi = contract_interface['abi']

    return contract_address, abi

def deploy_participant_management(governance_address, source):
    with open(source) as f:
        contract_source_code = f.read()

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:participantManagement']
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.constructor(governance_address).transact(
        transaction={'from': w3.eth.accounts[0], 'gas': 4100000}
    )
    tx_receipt = wait_for_receipt(tx_hash)
    contract_address = tx_receipt['contractAddress']
    abi = contract_interface['abi']

    return contract_address, abi

governance_address, governance_abi = deploy_governance(TYPE_MODIFIERS, VICTORY_BASE, PARTICIPATION_BASE, GOVERNANCE_SOURCE)
pm_address, pm_abi = deploy_participant_management(governance_address, PM_SOURCE)

config_dict = {}
config_dict['node_host'] = NODE_HOST
config_dict['node_port'] = NODE_PORT
config_dict['governance_address'] = governance_address
config_dict['governance_abi'] = governance_abi
config_dict['pm_address'] = pm_address
config_dict['pm_abi'] = pm_abi

with open('config.json', 'w') as f:
    json.dump(config_dict, f)