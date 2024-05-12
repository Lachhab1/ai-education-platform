from web3 import Web3
import solcx

# Enable unaudited HD Wallet features
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

# Set the desired Solidity compiler version
solcx.set_solc_version('v0.8.0')

# Connect to the local Ethereum node
rpc_url = 'http://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(rpc_url))
# Install the Solidity compiler if not already installed
solcx.install_solc('v0.8.0')

# Define the smart contract code
contract_source_code = '''
pragma solidity ^0.8.0;

contract EducationCredentials {
    mapping(address => string[]) public credentials;

    function addCredential(string memory credential) public {
        credentials[msg.sender].push(credential);
    }

    function getCredentials() public view returns (string[] memory) {
        return credentials[msg.sender];
    }
}
'''

# Compile the contract
compiled_sol = solcx.compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:EducationCredentials']

# Generate an account from a mnemonic phrase
mnemonic = "shift burger margin oak vapor arrest bracket differ bring wine draw pupil"  # Replace with your actual mnemonic phrase
account = w3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")

# Set the default account for transactions
w3.eth.default_account = account.address

# Deploy the contract
contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

# Interact with the contract
contract_instance = w3.eth.contract(address=contract_address, abi=contract_interface['abi'])
