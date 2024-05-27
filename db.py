from flask import Flask
from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{getenv('PGUSER')}:{getenv('PGPASSWORD')}@{getenv('PGHOST')}:{getenv('PGPORT', 5432)}/{getenv('PGDATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True
        
db = SQLAlchemy(app)

class Emails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_field = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    predicted = db.Column(db.String(255), nullable=False)
    actual = db.Column(db.String(255), nullable=False)

def create_email(email_message,body,result):
    subject = email_message['subject'].replace('\n', '').replace('\r', '')
    from_field = email_message['from'].replace('\n', '').replace('\r', '')
    actual = 'NOT SET'

    result_message = 'Phishing' if result == -1 else 'Safe'
    with app.app_context():
        try:
            email = Emails(from_field=from_field, subject=subject, body=body, predicted=result_message, actual=actual)
            db.session.add(email)
            db.session.commit()
            print(f"\n🧮 Email from {from_field} saved in the database.\n")
        except Exception as e:
            print(f"❌ Error saving email in the database: {e}")