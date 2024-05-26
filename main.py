from flask import Flask
from imapclient import IMAPClient
import smtplib, ssl
from email.message import EmailMessage
from email.header import decode_header
from apscheduler.schedulers.background import BackgroundScheduler
import email
import config 
from models.predict_output import predictOutput
from cleanup_email import extract

app = Flask(__name__)

# Email account credentials
IMAP_SERVER = config.IMAP_SERVER
IMAP_USER = config.IMAP_USER
IMAP_PASSWORD = config.IMAP_PASSWORD
SMTP_SERVER = config.SMTP_SERVER
SMTP_USER = config.SMTP_USER
SMTP_PASSWORD = config.SMTP_PASSWORD

# Initialize SMTP client for replies
context = ssl.create_default_context()
server = smtplib.SMTP(SMTP_SERVER,port=587)
server.ehlo()
server.starttls(context=context)
print('Connected to SMTP server.')
server.login(SMTP_USER, SMTP_PASSWORD)
print('Logged in to SMTP server.')

# Initialize IMAP client
client = IMAPClient(IMAP_SERVER)
print('Connected to IMAP server.')
client.login(IMAP_USER, IMAP_PASSWORD)
print('Logged in to IMAP server.')
client.select_folder('INBOX')

def decode_mime_words(s):
    decoded_words = decode_header(s)
    return ''.join(word.decode(encoding or 'utf8') if isinstance(word, bytes) else word for word, encoding in decoded_words)

# Initialize IMAP client
def check_email():
    print('\nChecking for new emails...')
    
    messages = client.search(['UNSEEN'])
    if not messages:
        print('No new unseen emails.')
        return
    else:
        print(f'Found {len(messages)} new unseen email(s).')

    for uid, message_data in client.fetch(messages, 'RFC822').items():
        email_message = extract(message_data[b'RFC822'], uid)
        email_message['Message-ID'] = email.message_from_bytes(message_data[b'RFC822']).get('Message-ID')
        email_message['Thread-Index'] = email.message_from_bytes(message_data[b'RFC822']).get('Thread-Index')
        handle_email(email_message)
        client.add_flags(uid, '\\Seen')

# Process the email
def handle_email(email_message):
    body = email_message['text'] or email_message['html']

    print(f"\nNew email from: {email_message['from']}")
    print(f"Subject: {email_message['subject']}")

    # Try to predict the output
    result = predictOutput(body)

    # Append email to .csv file (if it doesn't exist, create one called "mails.csv")
    # Columns are: From, Subject, Body, Result (Phishing or Safe)
    result_message = 'Phishing' if result == -1 else 'Safe'
    with open('mails.csv', 'a', encoding='utf-8') as f:
        f.write(f"\"{email_message['from']}\", \"{decode_mime_words(email_message['subject'])}\", \"{body}\", {result_message}\n")

    # Send a reply
    send_reply(email_message, result)

# Send a reply to the email
def send_reply(email_message, result):
    print("\nTrying to send a reply...")

    message_id = email_message['Message-ID'].replace('\n', '').replace('\r', '')

    reply = EmailMessage()
    reply['Subject'] = 'Re: ' + email_message['subject'].replace('\n', '').replace('\r', '')
    reply['From'] = SMTP_USER
    reply['To'] = email_message['from']
    reply['In-Reply-To'] = message_id
    reply['References'] = message_id
    reply['Thread-Index'] = email_message['Thread-Index']

    if result == -1:
        reply.set_content('Este correo es sospechoso, y podría tratarse de un correo de phishing (fraudulento). Por favor, tenga cuidado y no entre a ningún enlace.\n\nGracias por usar nuestro servicio!')
    else:
        reply.set_content('Este correo parece ser seguro. Sin embargo, siempre tenga cuidado al operar y abrir enlaces en la web.\n\nGracias por usar nuestro servicio!')
    
    server.send_message(reply)
    print(f'Reply sent to {email_message["from"]}.')

# Schedule the email check
scheduler = BackgroundScheduler()
scheduler.add_job(check_email, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def index():
    return 'Email checker service is running.'

if __name__ == '__main__':
    app.run(debug=True)
