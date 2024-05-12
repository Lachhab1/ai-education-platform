import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

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
