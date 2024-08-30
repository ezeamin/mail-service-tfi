from imapclient import IMAPClient
import smtplib, ssl
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Email account credentials
IMAP_SERVER = getenv('IMAP_SERVER')
IMAP_USER = getenv('IMAP_USER')
IMAP_PASSWORD = getenv('IMAP_PASSWORD')
SMTP_SERVER = getenv('SMTP_SERVER')
SMTP_USER = getenv('SMTP_USER')
SMTP_PASSWORD = getenv('SMTP_PASSWORD')

# Initialize SMTP client for replies
def getServerConnection():
    context = ssl.create_default_context()
    server = smtplib.SMTP(SMTP_SERVER,port=587)
    server.ehlo()
    server.starttls(context=context)
    server.login(SMTP_USER, SMTP_PASSWORD)
    print('Connected to SMTP server.')
    return server

# Initialize IMAP client
def getImapConnection():
    client = IMAPClient(IMAP_SERVER,993)
    client.login(IMAP_USER, IMAP_PASSWORD)
    print('Connected to IMAP server.')
    return client