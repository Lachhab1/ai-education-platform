import os
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit
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
    
    # Join the filtered tokens back into a string
    preprocessed_text = ' '.join(filtered_tokens)
    return preprocessed_text

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
                    processed_text = preprocess_text(text)
                    data.append(processed_text)
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

# Create a pipeline with TfidfVectorizer and SVC
text_clf = Pipeline([('tfidf', TfidfVectorizer()), ('clf', SVC())])

# Split into train and test sets using stratified split
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in sss.split(data, labels):
    X_train, X_test = [data[i] for i in train_index], [data[i] for i in test_index]
    y_train, y_test = [labels[i] for i in train_index], [labels[i] for i in test_index]

# Train the model
text_clf.fit(X_train, y_train)

# Save the trained model
model_path = os.path.join(os.getcwd(), 'model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(text_clf, f)
print(f"Model saved to: {model_path}")

# Make predictions on test data
y_pred = text_clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Print classification report
print(classification_report(y_test, y_pred))