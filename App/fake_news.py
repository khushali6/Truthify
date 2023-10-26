import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

csv_file = os.path.join(os.path.dirname(__file__), 'fake_news.csv')
# Load the dataset
try:
    data = pd.read_csv(csv_file, encoding='latin1')
except UnicodeDecodeError:
    try:
        data = pd.read_csv(csv_file, encoding='latin1')
    except UnicodeDecodeError:
        data = pd.read_csv(csv_file, encoding='utf-16')

# Handle missing values
data.fillna('', inplace=True)
print(data.columns)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[['ï»¿URL', 'Headline']], data['Label'], test_size=0.2, random_state=42)

# Preprocess the text data using TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train['Headline'])
X_test_tfidf = vectorizer.transform(X_test['Headline'])

# Train a Random Forest Classifier
classifier = RandomForestClassifier()
classifier.fit(X_train_tfidf, y_train)

# Method to predict the label of a news article
def predict_article(news_headline, news_url):
    # Preprocess the input data
    input_data = pd.DataFrame({'URL': [news_url], 'Headline': [news_headline]})
    input_data.fillna('', inplace=True)
    input_tfidf = vectorizer.transform(input_data['Headline'])
    
    # Predict the label
    prediction = classifier.predict(input_tfidf)
    if prediction[0] == '':
        return 2  # Return label 2 for "indecisive"
    return int(prediction[0])  # Return the predicted label as an integer
