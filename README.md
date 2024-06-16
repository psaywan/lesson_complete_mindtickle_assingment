# lesson_complete_mindtickle_assingment

## Here I have made few required changes to the Docker compose as belows

![Screenshot](https://raw.githubusercontent.com/psaywan/lesson_complete_mindtickle_assingment/master/ss/Screenshot%202024-06-16%20at%208.39.30%20PM.png)


## Changes needed into init.pg.sql. as addition of the table named lesson_completed to track all the entries of the completed lesson by the users. I did used sample data for the same.

![Screenshot](https://github.com/psaywan/lesson_complete_mindtickle_assingment/blob/master/ss/Screenshot%202024-06-16%20at%208.39.30%20PM.png)



In .env we have add information as belows:(Please refer to the .env in /setup/)

AWS_ACCESS_KEY="AWS_ACCESS_KEY"
AWS_SECRET_KEY="AWS_SECRET_KEY"
S3_BUCKET_NAME="Bucket name"

EMAIL_FROM="Sender email"
EMAIL_TO="Reciever email"
SES_SMTP_USER="SMTP user name"
SES_SMTP_PASSWORD="SMTP password"

While I have written python as I didn't had any access to airflow I tried reflecting the same steps in dummpy airflow dag script as well which can be fount in setup/ folder
