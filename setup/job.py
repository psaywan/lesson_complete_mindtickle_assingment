
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import boto3
from botocore.exceptions import NoCredentialsError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables from .env file
load_dotenv()

# Ensure that all necessary environment variables are set
required_vars = [
    'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT',
    'MYSQL_DATABASE', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_HOST', 'MYSQL_PORT', 'MYSQL_ROOT_PASSWORD',
    'AWS_ACCESS_KEY', 'AWS_SECRET_KEY', 'S3_BUCKET_NAME',
    'EMAIL_FROM', 'EMAIL_TO', 'SES_SMTP_USER', 'SES_SMTP_PASSWORD'
]

for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Environment variable {var} is not set.")

# Environment variables
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5433')  # Use port 5432

MYSQL_DB = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3307')

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
SES_SMTP_USER = os.getenv('SES_SMTP_USER')#'AKIAYW5UGAODN7T3ADCS'
SES_SMTP_PASSWORD = os.getenv('SES_SMTP_PASSWORD')#'BJCuFXogPzHYSWm/4MQxBpO2o2wACzwiN73szdX3RxBc'

def fetch_and_process_data():
    try:
        # Database connections
        postgres_engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
        mysql_engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}')

        # Query to get lessons completed from MySQL
        mysql_query = "SELECT user_id, COUNT(*) as lessons_completed, DATE(completion_date) as date FROM lesson_completion GROUP BY user_id, DATE(completion_date)"
        
        # Query to get users from PostgreSQL
        postgres_query = "SELECT user_id, user_name as name FROM mindtickle_users WHERE active_status = 'active'"

        # Fetch data from MySQL
        mysql_df = pd.read_sql(mysql_query, mysql_engine)

        # Fetch data from PostgreSQL
        postgres_df = pd.read_sql(postgres_query, postgres_engine)

        # Merge dataframes
        report_df = pd.merge(mysql_df, postgres_df, on='user_id')
        report_df.rename(columns={'name': 'Name', 'lessons_completed': 'Number of lessons completed', 'date': 'Date'}, inplace=True)

        # Save to CSV
        csv_filename = '/tmp/daily_lessons_report.csv'
        report_df.to_csv(csv_filename, index=False)
        return csv_filename
    except Exception as e:
        print(f"Error fetching and processing data: {e}")
        raise

def upload_to_s3(file_path):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3.upload_file(file_path, S3_BUCKET_NAME, os.path.basename(file_path))
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False

def send_email(file_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = "Daily Lessons Report"

        body = "Please find attached the daily lessons report."
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(file_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(file_path)}")
        msg.attach(part)

        server = smtplib.SMTP('email-smtp.ap-south-1.amazonaws.com', 587)
        server.starttls()
        server.login(SES_SMTP_USER, SES_SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Fetch and process data
    csv_file = fetch_and_process_data()
    # Upload to S3
    upload_success = upload_to_s3(csv_file)
    # Send email if upload was successful
    if upload_success:
        send_email(csv_file)
