import boto3
import psycopg2
import json
import time
import hashlib

#Configuration of Local Stack (Configure according to the example provided,declared as global to maintain ease of modification)
SQS_QUEUE_URL = 'http://localhost:4566/000000000000/login-queue'
AWS_REGION = 'us-east-1' 

#Configuration of PostgreSQL(Configure according to the example provided,declared as global to maintain ease of modification)
PG_HOST = 'localhost'
PG_PORT = 5432
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'
PG_DB = 'postgres'
PG_TABLE = 'user_logins'

#Function to access the SQS and read the data from the queue, i have used JSON and HashMaps as data structures.
def receive_message(queue_url):
    sqs_client = boto3.client('sqs', endpoint_url=queue_url,aws_access_key_id='dummy',aws_secret_access_key='dummy',)
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )
        if 'Messages' in response:
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']
            json_data = json.loads(message['Body'])
            return json_data, receipt_handle
    except Exception as e:
        print("Error receiving message:", e)
    return None, None

# Function to delete the message from the queue so that the same message wont be read multiples times.
#Unable to delete from the Queue because of the Client token id security isssue.
def delete_message(queue_url, receipt_handle):
    sqs_client = boto3.client('sqs')
    try:
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    except Exception as e:
        print("Error deleting message:", e)

# Function to connect to the data base and write data into it.
# I have used cursor object to access the data base
def write_to_postgres(data):
    try:
        connection = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            database=PG_DB
        )

        cursor = connection.cursor()

        #Check if the table exists
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM pg_tables WHERE tablename = '{PG_TABLE}');")
        table_exists = cursor.fetchone()[0]

        #Create the table if it does not exist
        if not table_exists:
            cursor.execute(f"CREATE TABLE {PG_TABLE} (user_id integer, device_type varchar(255), masked_ip varchar(255), masked_device_id varchar(255), locale varchar(255), app_version varchar(255));")

        #Alter the data type of 'app_version' to varchar to support the data being set.
        cursor.execute(f"ALTER TABLE {PG_TABLE} ALTER COLUMN app_version TYPE varchar(255);")

        #Flatten the JSON object
        flattened_data = flatten_json(data)

        #Insert data into Postgres table
        insert_query = f"INSERT INTO {PG_TABLE} (user_id, device_type, masked_ip, masked_device_id, locale, app_version) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_query, (
            flattened_data['user_id'],
            flattened_data['device_type'],
            mask_field(flattened_data['ip']),
            mask_field(flattened_data['device_id']),
            flattened_data['locale'],
            str(flattened_data['app_version']) 
        ))
        print("Successfully Executed")
        connection.commit()
        connection.close()

    except psycopg2.Error as e:
        print("Error writing to Postgres:", e)


#Function to mask the device_id and ip fields using SHA 256 hashing
def mask_field(field_value):
    return hashlib.sha256(field_value.encode('utf-8')).hexdigest()[:16]

#flatten json object
def flatten_json(json_obj):
    flat_data = {}
    for key, value in json_obj.items():
        if isinstance(value, dict):
            flat_data.update(flatten_json(value))
        else:
            flat_data[key] = value
    return flat_data

#Main funciton where the link is done between queue and database
#Commented the delete since its not getting deleted from the message queue
def process_sqs_and_save_to_db(queue_url):
    try:
        while True:
            json_data, receipt_handle = receive_message(queue_url)
            if json_data is not None:
                print(json_data)
                write_to_postgres(json_data)
                #delete_message(queue_url, receipt_handle) 
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")

# Function to Check the tables of a data base and see if the data is proeprly inserted
def check_database():
    try:
        connection = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgres',
            database='postgres'
        )
        if not connection.closed:
            print('Connection established successfully.')
        else:
            print('Connection failed.')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM user_logins;')

        for row in cursor:
            print(row)
        connection.close()

    except Exception as e:
        print(e)

def main():
    process_sqs_and_save_to_db(SQS_QUEUE_URL)
    #check_database()



if __name__ == "__main__":
    main()
