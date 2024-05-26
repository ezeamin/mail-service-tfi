from imapclient import IMAPClient
import smtplib, ssl
import config 

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
server.login(SMTP_USER, SMTP_PASSWORD)
print('Connected to SMTP server.')

# Initialize IMAP client
client = IMAPClient(IMAP_SERVER)
client.login(IMAP_USER, IMAP_PASSWORD)
client.select_folder('INBOX')
print('Connected to IMAP server.')