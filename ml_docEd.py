import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Function to preprocess text data
def preprocess_text(text):
    # Convert to lowercase and tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and perform stemming
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('french'))
    filtered_tokens = [stemmer.stem(token) for token in tokens if token not in stop_words and token.isalnum()]
    
    return filtered_tokens

# Function to load and preprocess data
def load_data(data_dir):
    data = []
    labels = []

    def traverse_dir(dir_path, category):
        for entry in os.listdir(dir_path):
            entry_path = os.path.join(dir_path, entry)
            if os.path.isdir(entry_path):
                traverse_dir(entry_path, category)
            elif os.path.isfile(entry_path) and not entry.startswith('.'):
                print(f"Processing file: {entry_path}")
                with open(entry_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    data.append(" ".join(preprocess_text(text)))
                    labels.append(category)

    print(f"Processing directory: {data_dir}")
    for category in os.listdir(data_dir):
        category_dir = os.path.join(data_dir, category)
        if os.path.isdir(category_dir):
            print(f"Found category: {category}")
            traverse_dir(category_dir, category)
        else:
            print(f"Skipping non-directory entry: {category}")

    return data, labels

# Load data
data_dir = './data'
data, labels = load_data(data_dir)

# Create a pipeline with TfidfVectorizer and SVM
text_clf = Pipeline([('tfidf', TfidfVectorizer()), ('clf', SVC())])

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Train the model
text_clf.fit(X_train, y_train)

# Make predictions on test data
y_pred = text_clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Print classification report
print(classification_report(y_test, y_pred))