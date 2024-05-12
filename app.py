from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from web3 import Web3
import solcx
from eth_account import Account
from werkzeug.utils import secure_filename
import json
import os

with open('categories.json', 'r') as f:
    categories = json.load(f)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.static_folder = 'uploads'
app.secret_key = 'enset2024'
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app)
Account.enable_unaudited_hdwallet_features()
# Connect to the local Ethereum node
rpc_url = 'http://127.0.0.1:7545'
w3 = Web3(Web3.HTTPProvider(rpc_url))

# Set the desired Solidity compiler version
solcx.set_solc_version('v0.8.0')

# User model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Load user from database (replace with your own logic)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Implement your own authentication logic here
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid (replace with your own logic)
        if username == 'admin' and password == 'password':
            user = User(1)  # Replace with actual user object
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# Load the model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Convert to lowercase and tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and perform stemming
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('french'))
    filtered_tokens = [stemmer.stem(token) for token in tokens if token not in stop_words and token.isalnum()]
    
    return filtered_tokens

# Add a route to display the index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
@login_required
def classify_text(file_path):
    # Read the file contents
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Preprocess the input text
    processed_text = preprocess_text(text)
    processed_text_str = ' '.join(processed_text)

    # Make a prediction using the loaded model
    prediction = model.predict([processed_text_str])[0]

    # Store the predicted category on the blockchain
    store_credential_on_blockchain(prediction)

    return jsonify({'category': prediction})






@app.route('/view_categories')
@login_required
def view_categories():
    return render_template('categoty.html' , categories=categories)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_name = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)

    response = classify_text(file_path)

    if response.status_code == 200:
        data = response.get_json()
        category = data['category']
        file_info = {'name': file_name, 'path': file_path}

        # Find the category in your categories list and add the file
        for cat in categories:
            if cat['name'] == category:
                cat['files'].append(file_info)
                break

        # Save the updated categories to the JSON file
        with open('categories.json', 'w') as f:
            json.dump(categories, f, indent=2)

        return jsonify({'message': 'File uploaded and categorized successfully'})
    else:
        return response

# Function to store credential on blockchain
def store_credential_on_blockchain(credential):
    # Generate an account from a mnemonic phrase
    mnemonic = "sense ship float liar whisper candy color awful vast detect wear modify"  # Replace with your actual mnemonic phrase
    account = w3.eth.account.from_mnemonic(mnemonic, account_path="m/44'/60'/0'/0/0")

    # Set the default account for transactions
    w3.eth.default_account = account.address

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

    # Deploy the contract
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress

    # Interact with the contract
    contract_instance = w3.eth.contract(address=contract_address, abi=contract_interface['abi'])

    # Store credential on blockchain
    tx_hash = contract_instance.functions.addCredential(credential).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)

if __name__ == '__main__':
    app.run(debug=True)
