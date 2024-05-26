from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import email

from email.message import EmailMessage

from models.predict_output import predictOutput
from cleanup_email import extract
from mail import server,client,SMTP_USER
from utils import set_email_content,save_email_in_file

app = Flask(__name__)

# Initialize IMAP client
def check_email():
    print('\nChecking for new emails...')
    
    messages = client.search(['UNSEEN'])
    if not messages:
        print('No new unseen emails.')
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
    print("\nTrying to send a reply...")

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
    print(f'Reply sent to {email_message["from"]}.')

# Schedule the email check
scheduler = BackgroundScheduler()
scheduler.add_job(check_email, 'interval', seconds=30)
scheduler.start()

@app.route('/')
def index():
    return 'Email checker service is running.'

if __name__ == '__main__':
    app.run()
