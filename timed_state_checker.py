import boto3
import datetime
import json

bucket_name = "asaf-dy-feedcats"
file_name = "state.json"

def send_email(message_body):
    ses = boto3.client("ses")
    ses.send_email(
    Source="asafchel@post.bgu.ac.il",
    Destination={
        "ToAddresses": [
            "asaf@chelouche.net"
        ]
    },
    Message={
        "Subject": {
            "Data": "The cat's state has changed!",
            "Charset": "utf-8"
        },
        "Body": {
            "Text": {
                "Data": message_body,
                "Charset": "utf-8"
            }
        }
    },
    ReplyToAddresses=[
        "asafchel@post.bgu.ac.il",
    ],
    ReturnPath="asafchel@post.bgu.ac.il",
    SourceArn="arn:aws:ses:us-east-1:781085178525:identity/asafchel@post.bgu.ac.il",
    ReturnPathArn="arn:aws:ses:us-east-1:781085178525:identity/asafchel@post.bgu.ac.il"
)

def check_state(event, context):
    current_time = datetime.datetime.now()
    current_time_as_string = str(current_time)
    s3 = boto3.resource("s3")
    s3.Object(bucket_name, file_name).download_file("/tmp/old_state.json")
    file = open("/tmp/old_state.json", "r")
    contents = file.read()
    file.close()
    contents_as_object = json.loads(contents)
    timestamp = contents_as_object["timestamp"]
    last_email_state = contents_as_object["last_email_state"]
    if last_email_state == "cat_fed":
        timestamp_as_object = datetime.datetime.strptime(timestamp, "%Y-%m-%d %X.%f")
        diff = current_time - timestamp_as_object
        if diff.seconds / 60 >= 15:
            new_state = {"timestamp": current_time_as_string, "last_email_state": "cat_hungry"}
            file = open("/tmp/new_state.json", "w+")
            file.write(json.dumps(new_state))
            file.close()
            s3.Object(bucket_name, file_name).upload_file("/tmp/new_state.json")
            send_email("The cat is hungry! Feed him!")
            print("The cat just turned hungry, an email alert was sent.")
        else:
            print("Less then 15 minutes passed since the cat last ate. Actual time difference is {0} minutes.".format(diff.seconds / 60))
    else:
        print("The cat is hungry! FEED HIM!")
