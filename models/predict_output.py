from nltk.corpus import stopwords
import re

from models.model import Model

stop_words = stopwords.words('english')
model = Model()

def prepareTestRawData(emailBody):
    # Remove the forwarded section
    emailBody = re.sub(r'(Resent|Forwarded) message.*\n', '', emailBody)
    emailBody = re.sub(r'(From|De):.*\n', '', emailBody)
    emailBody = re.sub(r'(Sent|Enviado|Date):.*\n', '', emailBody)
    emailBody = re.sub(r'(To|Para):.*\n', '', emailBody)
    emailBody = re.sub(r'(Subject|Asunto):.*\n', '', emailBody)

    # Remove special characters, convert to lowercase, and remove stop words
    emailBody = re.sub(r'[^\w\s]', '', emailBody).replace('_', '').lower()
    emailBody = ' '.join([word for word in emailBody.split() if word not in stop_words and not word.isdigit()])

    return emailBody

def predictOutput(emailBody):
    new_processed_data = [prepareTestRawData(emailBody)]

    transformed_data = model.getConvertFeatureTransform(new_processed_data)
        
    pred = model.predict(transformed_data)

    return pred[0]