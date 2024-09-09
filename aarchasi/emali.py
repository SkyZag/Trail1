import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
area = "hyd"
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = '22eg110a23@anurag.edu.in'
EMAIL_PASSWORD = '96chikki25'

def send_test_email():
    to_email = 'gk9676473925@gmail.com'
    subject = f'Request for Trash Collection in {area}'
    body = f"""Dear ------,

I hope this email finds you well. I am writing to request the collection of trash in our area, {area}.We have noticed that the trash has not been collected for a few days, and the accumulation is becoming a concern for the residents.

Could you please arrange for a trash collection at the earliest convenience to ensure the cleanliness and hygiene of our neighborhood? If you need any further details or specific instructions, please do not hesitate to let me know.

Thank you for your attention to this matter. We appreciate your prompt response and cooperation."""

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
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Run the test function
send_test_email()
