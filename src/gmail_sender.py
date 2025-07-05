from src.custom_exception import CustomException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from src.logger import auto_logger
import os
import sys
import io
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
logger = auto_logger(__name__)


class Emailreply():

    def __init__(self):
        try:
            logger.info("Authenticating Email Creds")

            self.email = os.getenv("emailid")
            self.password = os.getenv("password")

            logger.info("Email Creds authenticated sucessfully")
        except Exception as e:
            logger.error("Failed to authenticate email creds")
            raise CustomException(e)

    def email_sender(self,to_email,subject,body):
        try:
            logger.info("Sending Ticket registration confirmation mail to patient")

            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain')) 



            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(0)  # Set to 1 to enable full SMTP debug
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

            logger.info("Email sent sucessfully")

        except Exception as e:
            logger.error("Failed to send email")
            raise CustomException(e)