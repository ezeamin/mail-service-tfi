# Phishing Detector Service

This is a web service that detects phishing emails upon resend to a specific inbox. 

The service uses an AI Model based on Complement Naive Bayes Algorithm to classify emails as phishing or not phishing.

This is a project developed for the subject "Proyecto Final Integrador" at Universidad del Norte Santo Tomás de Aquino.

## Dependencies

Dependencies are listed in the `requirements.txt` file. You can install them by running the following command:
```shell
pip install -r requirements.txt
```

After that, you'll need to install the NLTK data. Follow the instructions below to install NLTK and download the necessary data.

1. Install NLTK by running the following command (if not already installed):
    ```shell
    pip install nltk
    ```

2. Initialize NLTK by running the following Python code:
    ```python
    import nltk
    nltk.download('stopwords')
    ```

## Running the Web Service

This is a web service developed in Python with Flask. You can run the web service by following the instructions below.

1. First, be sure to create a `.env` file with the content of the `.env.sample` file. This info will be used to connect to the email server. Be careful with the credentials you use.

2. Then, run the web service by executing the following command:
    ```
    python main.py
    ```

## Usage

Every one minute, the web service will check the inbox for new emails. If a new email is found, the service will check if the email is a phishing email using an AI Model based on Complement Naive Bayes Algorithm. If it is, the email will be marked as a phishing email and the user will be notified with a response email.

New emails will also be saved in SQL database for further analysis.

## License

This project is licensed under the MIT License.

## Authors

- [Ezequiel Amin](https://github.com/ezeamin)
- [Valentina Ormaechea](https://github.com/valeormaechea)
- [Bernardita Peñalba](https://github.com/bernipenalba)