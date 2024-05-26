from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import email
import datetime

from email.message import EmailMessage

from models.predict_output import predictOutput
from cleanup_email import extract
from mail import getServerConnection,getImapConnection, SMTP_USER
from utils import set_email_content,save_email_in_file,bcolors
import sys
import nltk

app = Flask(__name__)

client = getImapConnection()

# Initialize IMAP client
def check_email():
    # Print day and time
    print(f'\n🕒 {datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}')

    # Search for new emails in INBOX
    client.select_folder('INBOX')
    process_emails("INBOX 📩")
    
    # Search for new emails in SPAM
    client.select_folder('Junk')
    process_emails("SPAM 🗑️")
    
# Check for new emails in the selected folder
def process_emails(type):
    print(f'🔍 Checking for new emails in {type}...')
    messages = client.search(['UNSEEN'])
    if not messages:
        print(f'🫡  No new unseen emails in {type}.\n')
    else:
        print(f'🧐  Found {len(messages)} new unseen email(s) in {type}.')

        for uid, message_data in client.fetch(messages, 'RFC822').items():
            email_message = extract(message_data[b'RFC822'], uid)
            email_message['Message-ID'] = email.message_from_bytes(message_data[b'RFC822']).get('Message-ID')
            email_message['Thread-Index'] = email.message_from_bytes(message_data[b'RFC822']).get('Thread-Index')
            handle_email(email_message)
            client.add_flags(uid, '\\Seen')

# Process the email
def handle_email(email_message):
    # Get the email body either from the text or html
    body = email_message['text'] or email_message['html']

    print(f"\nNew email from: {email_message['from']}")
    print(f"Subject: {email_message['subject']}")

    # Try to predict the output using the model
    result = predictOutput(body)

    # Save the email in a file
    save_email_in_file(email_message, result)

    # Send a reply
    send_reply(email_message, result)

# Send a reply to the email
def send_reply(email_message, result):
    server = getServerConnection()

    print("\n📦 Trying to send a reply...")
    subject = email_message['subject'].replace('\n', '').replace('\r', '')
    message_id = email_message['Message-ID'].replace('\n', '').replace('\r', '')
    from_mail = email_message['from']
    thread_index = email_message['Thread-Index']

    reply = EmailMessage()
    reply['Subject'] = 'Re: ' + subject
    reply['From'] = SMTP_USER
    reply['To'] = from_mail
    reply['In-Reply-To'] = message_id
    reply['References'] = message_id
    reply['Thread-Index'] = thread_index

    plain_text = set_email_content(result)
    html_content = "<html><body>" + plain_text + "</body></html>"

    reply.set_content(html_content)
    reply.add_alternative(html_content, subtype='html')

    server.send_message(reply)
    print(f'✅ Reply sent to {email_message["from"]} with result: {f"{bcolors.WARNING}Phishing{bcolors.ENDC}" if result == -1 else f"{bcolors.OKGREEN}Safe{bcolors.ENDC}"}.\n')
    
    server.quit()

# Schedule the email check
scheduler = BackgroundScheduler()
scheduler.add_job(check_email, 'interval', minutes=1)
scheduler.start()

# Check the email on startup
check_email()

@app.route('/')
def index():
    return 'Email checker service is running.'

if __name__ == '__main__':
    app.run()
