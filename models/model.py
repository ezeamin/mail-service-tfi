from sklearn.naive_bayes import ComplementNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk.corpus import stopwords
import re
from joblib import dump, load

stop_words = stopwords.words('english')

def prepareData():
    df = pd.read_csv('models/datasets/Phishing_Email.csv')
    
    # Remove the 'Unnamed: 0' column
    df = df.drop(columns=['Unnamed: 0'])

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove empty or null values
    df = df.dropna()

    # From Email Text element, retrieve only text and ignore any mail structure (html for example, but remove the tags and any special symbol)
    df['Email Text'] = df['Email Text'].astype(str).str.replace(r'<[^>]*>', '').apply(lambda x: re.sub(r'[^\w\s]', '', x)).str.replace('_', '').str.lower()

    # Remove stopwords and numbers
    df['Email Text'] = df['Email Text'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words and not word.isdigit()]))

    # Set EmailType to -1 for Phishing Email and 1 for Safe Email
    df['Email Type'] = df['Email Type'].apply(lambda x: -1 if x == "Phishing Email" else 1)

    # Oversample the dataset to match amount between phishing and non-phishing emails
    phishing_emails = df[df['Email Type'] == -1]
    non_phishing_emails = df[df['Email Type'] == 1]
    
    phishing_emails = phishing_emails.sample(len(non_phishing_emails), replace=True)
    
    df = pd.concat([phishing_emails, non_phishing_emails])

    return df

class Model:
    def __init__(self):
        print("Model initialized")

        self.model = load('models/data/ComplementNB.joblib')
        self.convert_feature = load('models/data/tfidf_vectorizer.joblib')

        print("Model ready")

        # Uncomment this block to retrain the model, you'll need the .csv training file, available at https://drive.google.com/file/d/1N0_thD9FwXUfidJ-3n7cJK6TroJWaDbB/view?usp=sharing
        
        # self.model = ComplementNB()
        
        # # Prepare data
        # loaded_dataset = prepareData()

        # # Convert feature with TF-ID
        # self.convert_feature = TfidfVectorizer()

        # X = self.convert_feature.fit_transform(loaded_dataset['Email Text'])
        # Y = loaded_dataset['Email Type']

        # # Save the convert feature
        # dump(self.convert_feature, 'models/data/tfidf_vectorizer.joblib')

        # # Train and test split
        # self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, Y, test_size=0.8, random_state=42)

        # self.train()

    def train(self):
        print("Training model...")
        
        self.model.fit(self.X_train, self.y_train)
        dump(self.model, 'models/data/ComplementNB.joblib')
        
        print("Model trained")

    def predict(self, input_array):
        return self.model.predict(input_array)

    def getConvertFeatureTransform(self,values):
        return self.convert_feature.transform(values)
