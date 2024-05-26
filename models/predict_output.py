from joblib import load
from nltk.corpus import stopwords
import re

from models.model import Model

stop_words = stopwords.words('english')
model = Model()

def prepareTestRawData(emailBody):
    emailBody = re.sub(r'[^\w\s]', '', emailBody).replace('_', '').lower()
    emailBody = ' '.join([word for word in emailBody.split() if word not in stop_words and not word.isdigit()])
    return emailBody

def predictOutput(emailBody):
    # convert_feature = load('models/data/tfidf_vectorizer.joblib')
    # model = load('models/data/ComplementNB.joblib')

    print(f'\nTest data: {emailBody}')

    new_processed_data = [prepareTestRawData(emailBody)]
    print(f'Processed test data: {new_processed_data[0]}\n')

    transformed_data = model.getConvertFeatureTransform(new_processed_data)
        
    pred = model.predict(transformed_data)

    if pred[0] == -1:
        print(f'Predicted: Phishing text')
        return -1
    else:
        print(f'Predicted: Safe text')
        return 0