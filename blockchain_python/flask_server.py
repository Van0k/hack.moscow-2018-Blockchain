import json
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import Contract, ConciseContract
from web3.middleware import geth_poa_middleware
from governance_handler import GovernanceHandler
from pm_handler import PMHandler
from web3.personal import Personal

PLACEHOLDER_ADDRESS = "0x" + "0"*40
BLOCK_TIME = 5
TYPE_MODIFIERS = [1, 2, 3, 4]
VICTORY_BASE = 100
PARTICIPATION_BASE = 10
NODE_HOST = '127.0.0.1'
NODE_PORT = '8501'
CONFIG_PATH = '../solc/config.json'

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

from flask import Flask, request, jsonify
app = Flask(__name__)

w3 = Web3(HTTPProvider(f'http://{NODE_HOST}:{NODE_PORT}'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

ghandler = GovernanceHandler(w3, config['governance_address'], config['governance_abi'])
phandler = PMHandler(w3, config['pm_address'], config['pm_abi'])

print(ghandler.current_voting_type())
print(phandler.balance_of(w3.eth.accounts[0]))

@app.route('/create_user_address', methods=['POST'])
def create_user_address():
    w3.eth.enable_unaudited_features()
    password = json.loads(request.data)['passphrase']
    new_address = w3.eth.account.create(password).address
    return jsonify({'address': new_address})

@app.route('/governance/victory_base', methods=['GET'])
def victory_base():
    return jsonify({'victory_base': ghandler.victory_base()})

@app.route('/governance/participation_base', methods=['GET'])
def participation_base():
    return jsonify({'participation_base': ghandler.participation_base()})

@app.route('/governance/organizers', methods=['GET'])
def organizers():
    return jsonify({'organizers': ghandler.organizers()})

@app.route('/governance/current_voting_type', methods=['GET'])
def current_voting_type():
    return jsonify({'current_voting_type': ghandler.current_voting_type()})

@app.route('/governance/type_modifier/<type_id>', methods=['GET'])
def type_modifier(type_id):
    return jsonify({'type_modifier': ghandler.type_modifier(int(type_id))})

@app.route('/governance/start_voting_add_organizer', methods=['POST'])
def start_voting_add_organizer():
    data = json.loads(request.data)
    organizer_address = data['address']
    ghandler.start_voting_add_organizer(organizer_address)
    return "Done!"

@app.route('/governance/start_voting_remove_organizer', methods=['POST'])
def start_voting_remove_organizer():
    data = json.loads(request.data)
    organizer_id = data['organizer_id']
    ghandler.start_voting_remove_organizer(organizer_id)
    return "Done!"

@app.route('/governance/start_voting_change_victory_base', methods=['POST'])
def start_voting_change_victory_base():
    data = json.loads(request.data)
    new_value = data['new_value']
    ghandler.start_voting_change_victory_base(new_value)
    return "Done!"

@app.route('/governance/start_voting_change_participation_base', methods=['POST'])
def start_voting_change_participation_base():
    data = json.loads(request.data)
    new_value = data['new_value']
    ghandler.start_voting_change_participation_base(new_value)
    return "Done!"

@app.route('/governance/start_voting_change_type_modifier', methods=['POST'])
def start_voting_change_type_modifier():
    data = json.loads(request.data)
    new_value = data['new_value']
    type_id = data['type_id']
    ghandler.start_voting_change_type_modifier(new_value, type_id)
    return "Done!"

@app.route('/governance/vote', methods=['POST'])
def vote():
    data = json.loads(request.data)
    is_vote_for = data['is_vote_for']
    print(is_vote_for)
    ghandler.vote(is_vote_for)
    return "Done!"

@app.route('/participants/balance_of/<address>', methods=['GET'])
def balance_of(address):
    return jsonify({'balance': phandler.balance_of(address)})

@app.route('/participants/give_tokens/<address>', methods=['POST'])
def give_tokens(address):
    data = json.loads(request.data)
    amount = data['amount']
    phandler.give_tokens(address, amount)
    return "Done!"

@app.route('/participants/slash_tokens/<address>', methods=['POST'])
def slash_tokens(address):
    data = json.loads(request.data)
    amount = data['amount']
    phandler.slash_tokens(address, amount)
    return "Done!"

@app.route('/participants/make_purchase', methods=['POST'])
def make_purchase():
    data = json.loads(request.data)
    address = data['address']
    amount = data['amount']
    phandler.slash_tokens(address, amount)
    return "Done!"

