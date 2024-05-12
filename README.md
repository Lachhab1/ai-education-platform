# AI Education Platform

The AI Education Platform is a Flask web application that allows users to upload text files and classify their content based on a pre-trained machine learning model. The application also integrates with the Ethereum blockchain for storing education credentials.

## Features

- User authentication with Flask-Login
- Text preprocessing and classification using NLTK and scikit-learn
- File upload and categorization
- Display categorized files based on their predicted categories
- Store predicted categories as education credentials on the Ethereum blockchain

## Prerequisites

- Python 3.x
- Flask
- NLTK
- scikit-learn
- Web3.py
- Solcx
- Ganache (local Ethereum blockchain)

## Installation

1. Clone the repository:

```
git clone https://github.com/Lachhab1/ai-education-platform.git
```

2. Navigate to the project directory:

```
cd ai-education-platform
```

3. Install the required Python packages:

```
pip install flask nltk scikit-learn web3 solcx
```

4. Download the necessary NLTK resources:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

5. Start the Ganache local Ethereum blockchain.

6. Update the `app.py` file with the appropriate mnemonic phrase and Ganache RPC URL.

## Usage

1. Run the Flask application:

```
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Log in with the default credentials (username: `admin`, password: `password`).

4. Upload a text file, and the application will classify its content and store the predicted category as an education credential on the Ethereum blockchain.

5. View the categorized files by navigating to the "View Categories" page.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [NLTK](https://www.nltk.org/)
- [scikit-learn](https://scikit-learn.org/)
- [Web3.py](https://web3py.readthedocs.io/)
- [Solcx](https://github.com/ethereum/solcx)
- [Ganache](https://trufflesuite.com/ganache/)
