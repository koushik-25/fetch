# fetch
Fetch Take Home Assesment

## Setups Needed to Run this application:

1. Install Python >3.6 from https://www.python.org/
2. Install Pip (if not already installed)
3. Install Docker https://docs.docker.com/get-docker/
4. Install Docker Compose if it does not come with Docker
5. Install Psql https://www.postgresql.org/download/
6. Install aws-cli client to test if the docker image is working fine using `pip install awscli-local`
7. Install boto3 library using `python -m pip install boto3`.
8. Install psycopg2 library using `python -m pip install psycopg2` or `python -m pip install psycopg2-binary` in few machines.

## Steps to run:

1. Run `aws configure` and set these values:

  AWS Access Key ID [None]: dummy
  
  AWS Secret Access Key [None]: dummy
  
  Default region name [None]: us-east-1
  
  Default output format [None]: json

2. Navigate to the directory where docker-compose.yml is present and run the command `docker-compose up`.
3. Do not close the terminal, keep the terminal running and open a new terminal.
4. Inside the new terminal, navigate to the folder where `app.py` is located and run `app.py` using the command `python app.py`.

**Note1**: For better understanding, 20s is the time interval between each message is fetched from the queue.

**Note2**: Deleting the message from the queue throws error because of the ClientTokenId security error, uncomment line number 116 inside `process_sqs_and_save_to_db()` function where `delete_message()` is called.

**Note3**: Uncomment the `check()` function to check for database once the application is completed running.
Result: Data from the Queue is fetched, required modifications are being made and stored into the PostgreSQL database.

**If issue with docker image, check if the service is activated from command line using this command:**

`awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue`
