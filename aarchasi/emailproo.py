import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = '22eg110a23@anurag.edu.in'  # Your email address
EMAIL_PASSWORD = '96chikki25'  # Your app password

# Define the CSV file to read results
results_file = "trash_classification_results.csv"

# Define the in-charge people mapping
incharge_mapping = {
    'Recyclable': {'email': 'gk9676473925@gmail.com'},
    'Decomposable': {'email': 'gk9676473925@gmail.com'},
    'Disposable': {'email': 'gk9676473925@gmail.com'}
}

# Function to send an email
def send_email(to_email, subject, body):
    try:
        # Create a MIME object
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Set up the server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email sent to {to_email} successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP authentication error: {e}")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Function to segregate data and notify in-charge people
def notify_incharge():
    if not os.path.exists(results_file):
        print("No results file found.")
        return

    # Read the CSV file
    try:
        df = pd.read_csv(results_file)
        print(f"CSV file read successfully. Data:\n{df}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Segregate and notify
    for classification, group in df.groupby('Classification'):
        if classification in incharge_mapping:
            incharge_info = incharge_mapping[classification]
            email_address = incharge_info['email']

            # Create a summary message
            message_body = f"Trash Classification Summary for {classification}:\n\n"
            for _, row in group.iterrows():
                message_body += f"Trash Type: {row['Trash Type']}\n"
                message_body += f"Instructions: {row['Instructions']}\n"
                message_body += f"Timestamp: {row['Timestamp']}\n"
                message_body += "-" * 40 + "\n"

            print(f"Preparing to send email to {email_address}")
            # Send an email to the in-charge person
            send_email(email_address, f"Trash Classification Notification: {classification}", message_body)

# Run the notification function
notify_incharge()
