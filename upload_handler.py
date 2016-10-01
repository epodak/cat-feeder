import boto3
import base64
import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import json
import datetime
from timed_state_checker import send_email

def check_label(label):
    if label == "fish" or label == "milk" or label == "bread":
        return True
    else:
        return False

def check_response(response):
    for annotation in response["responses"][0]["labelAnnotations"]:
        if float(annotation["score"]) > 0.5 and check_label(annotation["description"]):
            return True
    return False

def handle(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_name = event["Records"][0]["s3"]["object"]["key"]
    s3 = boto3.resource("s3")
    last_index_of_slash = file_name.rfind("/")
    if last_index_of_slash > -1:
        normalized_file_name = "/tmp/" + file_name[last_index_of_slash + 1:]
    else:
        normalized_file_name = "/tmp/" + file_name
    s3.Object(bucket_name, file_name).download_file(normalized_file_name)
    with open(normalized_file_name, "r+") as image:
        image_content = base64.b64encode(image.read())
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dy-catfeeder-a9dcf9458543.json"
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build("vision", "v1", credentials=credentials)
        service_request = service.images().annotate(body={
            "requests": [{
                "image": {
                    "content": image_content.decode("UTF-8")
                },
                "features": [{
                    "type": "LABEL_DETECTION",
                    "maxResults": 5
                }]
            }]
        })
        response = service_request.execute()
        if check_response(response):
            s3.Object(bucket_name, "state.json").download_file("/tmp/old_state.json")
            file = open("/tmp/old_state.json", "r+")
            contents = file.read()
            contents_as_object = json.loads(contents)
            current_time = datetime.datetime.now()
            current_time_as_string = str(current_time)
            contents_as_object["timestamp"] = current_time_as_string
            if contents_as_object["last_email_state"] == "cat_hungry":
                contents_as_object["last_email_state"] = "cat_fed"
                send_email("The cat is full and happy!")
            file.close()
            file = open("/tmp/new_state.json", "w+")
            file.write(json.dumps(contents_as_object))
            file.close()
            s3.Object(bucket_name, "state.json").upload_file("/tmp/new_state.json")
            print("The cat is fed!")
        else:
            print("The cat remains hungry!")
