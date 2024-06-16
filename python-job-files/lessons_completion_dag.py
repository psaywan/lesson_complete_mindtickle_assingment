import os
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import boto3
from botocore.exceptions import NoCredentialsError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook

# Load environment variables
def get_env_var(key):
    """Fetches environment variable securely"""
    return os.getenv(key) or BaseHook.get_connection(key).password

POSTGRES_DB = get_env_var('POSTGRES_DB')
POSTGRES_USER = get_env_var('POSTGRES_USER')
POSTGRES_PASSWORD = get_env_var('POSTGRES_PASSWORD')
POSTGRES_HOST = get_env_var('POSTGRES_HOST')
POSTGRES_PORT = get_env_var('POSTGRES_PORT')

MYSQL_DB = get_env_var('MYSQL_DATABASE')
MYSQL_USER = get_env_var('MYSQL_USER')
MYSQL_PASSWORD = get_env_var('MYSQL_PASSWORD')
MYSQL_HOST = get_env_var('MYSQL_HOST')
MYSQL_PORT = get_env_var('MYSQL_PORT')

AWS_ACCESS_KEY = get_env_var('AWS_ACCESS_KEY')
AWS_SECRET_KEY = get_env_var('AWS_SECRET_KEY')
S3_BUCKET_NAME = get_env_var('S3_BUCKET_NAME')

EMAIL_FROM = get_env_var('EMAIL_FROM')
EMAIL_TO = get_env_var('EMAIL_TO')
SES_SMTP_USER = get_env_var('SES_SMTP_USER')
SES_SMTP_PASSWORD = get_env_var('SES_SMTP_PASSWORD')

def fetch_and_process_data(**kwargs):
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

        # Push the CSV file path to XCom
        kwargs['ti'].xcom_push(key='csv_filename', value=csv_filename)
    except Exception as e:
        print(f"Error fetching and processing data: {e}")
        raise

def upload_to_s3(**kwargs):
    file_path = kwargs['ti'].xcom_pull(task_ids='fetch_and_process_data', key='csv_filename')
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

def send_email(**kwargs):
    file_path = kwargs['ti'].xcom_pull(task_ids='fetch_and_process_data', key='csv_filename')
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = "Daily Lessons Report"

        body = "Please find attached the daily lessons report."
        msg.attach(MIMEText(body, 'plain'))

        with open(file_path, "rb") as attachment:
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

# Define default args for DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    'daily_lessons_report',
    default_args=default_args,
    description='A DAG to create and send a daily lessons report',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Define tasks
t1 = PythonOperator(
    task_id='fetch_and_process_data',
    python_callable=fetch_and_process_data,
    provide_context=True,
    dag=dag,
)

t2 = PythonOperator(
    task_id='upload_to_s3',
    python_callable=upload_to_s3,
    provide_context=True,
    dag=dag,
)

t3 = PythonOperator(
    task_id='send_email',
    python_callable=send_email,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
t1 >> t2 >> t3
