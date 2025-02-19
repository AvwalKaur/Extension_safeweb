import smtplib
import os
import logging
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SMTP Server Details
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Use 465 for SSL

# Get credentials from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

# Set up logging with UTF-8 support
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Ensure Unicode support in logging
    ]
)

def send_email_alert(toxic_message):
    """Send an email alert when a toxic message is detected."""
    
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        logging.error("EMAIL_ADDRESS or EMAIL_PASSWORD is not set. Check your .env file.")
        return
    
    # ✅ Fix curly apostrophes and remove non-ASCII characters
    toxic_message = toxic_message.replace("’", "'")  # Convert curly apostrophe
    toxic_message = toxic_message.encode("ascii", "ignore").decode()  # Remove non-ASCII

    subject = "Toxic Speech Alert Detected"
    body = f"Toxic message detected:\n\n'{toxic_message}'\n\nPlease review it."

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = Header(subject, "utf-8")  # Encode subject properly

    # ✅ Explicitly encode the message to UTF-8
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        # Connect to SMTP Server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, msg.as_string())

        logging.info("Email alert sent successfully!")

    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed! Check your email & app password.")
    except smtplib.SMTPException as e:
        logging.error(f"Error sending email: {e}")

# Example Usage
if __name__ == "__main__":
    send_email_alert("This is a test toxic message with a curly apostrophe: ’")
