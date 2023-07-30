# fetch
Fetch Take Home Assesment

Setups Needed to Run this application:
Intall all the requirements below.
1) Python >3.6 download from https://www.python.org/
2)Pip will automaticall be installed else use sudo apt-get install python3-pip 
3) Install docker https://docs.docker.com/get-docker/
4) Install docker compose if it dosent come with docker.
5) Install Psql https://www.postgresql.org/download/
6) Pip will automaticall be installed else use sudo apt-get install python3-pip 
7)Install aws-cli client to test if the docket image is working fine using pip install awscli-local
8) Install boto3 library using python -m pip install boto3.
9) Install psycopg2 library using python -m pip install psycopg2 or python -m pip install psycopg2-binary in few machines.

Steps to run:
Once at the libraries are installed:
1)Docker will automatically pull the images if we navigate to the docker-compose.yml file and execute "docker-compose up" command but its adviced to download first for better functioning of application.
2)Pull the local stack docker image at https://hub.docker.com/r/fetchdocker/data-takehome-localstack using the command from terminal - "docker pull fetchdocker/data-takehome-localstack".
3)Pull the  postgresql docker image at https://hub.docker.com/r/fetchdocker/data-takehome-postgresusing the command from terminal - "docker pull fetchdocker/data-takehome-postgres".
4)Navigate to the directory where docker-compose.yml is present and run the command "docker-compose up". 
5) Do not close the terminal, keep the terminal running and open the new terminal.
6) Inside new terminal navigate to the folder where "app.py" is located and run app.py using "python app.py" command.

***Note1**: For better understanding 20s is the time interval between each message is fetched from the queue.
**Note2**: Deleting the message from the queue throws error because of the ClientTokenId security error, uncomment line number 116 inside process_sqs_and_save_to_db() function where delete_message() is called . 
Result: Data from the Queue is fetched required modifications are being made and stored into the PostgreSQL database.
**Note3**:uncoment the check funciton to check for database once the application is completed runnning

**If issue with docer image check if the service is activted from command line using this command:
"awslocal sqs receive-message--queue-urlhttp://localhost:4566/000000000000/login-queue"
 