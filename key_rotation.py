import boto3, os, time, datetime, sys, json
from datetime import date
from botocore.exceptions import ClientError

iam = boto3.client("iam")


def lambda_handler(event, context):
    email_70_list = []
    email_80_employee = []
    email_80_machine = []
    email_90_employee = []
    email_90_machine = []

    # print("All IAM user emails that have AccessKeys 30 days or older")
    unique_user_list = (iam.list_users()["Users"])
    for userlist in unique_user_list:
        userKeys = iam.list_access_keys(UserName=userlist["UserName"])
        for keyValue in userKeys["AccessKeyMetadata"]:
            UserAccessKeyID = keyValue["AccessKeyId"]
            IAMUserName = keyValue["UserName"]
            # print(f"IAMUserName IAM Users:{len(IAMUserName)}: {IAMUserName}")
            if (keyValue["Status"] == "Active" or keyValue["Status"] == "Inactive"):
                currentdate = date.today()
                active_days = currentdate - keyValue["CreateDate"].date()
                # print ("The active days details are: ", active_days)
                # print ("datetime details are: ", datetime.timedelta(days=15))

                # if Access key age is greater then or equal to 70 days, send warning
                if active_days == datetime.timedelta(days=int(os.environ["days_70"])):
                    userTags = iam.list_user_tags(UserName=keyValue["UserName"])
                    email_tag = list(
                        filter(lambda tag: tag["Key"] == "Email", userTags["Tags"])
                    )
                    if len(email_tag) == 1:
                        email = email_tag[0]["Value"]
                        email_70_list.append(email)
                        print(
                            "This User: ",
                            IAMUserName,
                            ", with the email: ",
                            email,
                            ", is having access key age is 70 days",
                        )

                        email_unique = list(set(email_70_list))
                        print("Email list: ", email_unique)
                        RECIPIENTS = email_unique
                        SENDER = os.environ["sender_email"]
                        AWS_REGION = os.environ["region"]
                        SUBJECT = os.environ["SUBJECT"]
                        BODY_TEXT_70 = os.environ["BODY_TEXT_70"]
                        BODY_HTML_70 = os.environ["BODY_HTML_70"]
                        CHARSET = "UTF-8"
                        client = boto3.client("ses", region_name=AWS_REGION)
                        try:
                            response = client.send_email(
                                Destination={
                                    "ToAddresses": RECIPIENTS,
                                },
                                Message={
                                    "Body": {
                                        "Html": {
                                            "Charset": CHARSET,
                                            "Data": BODY_HTML_70,
                                        },
                                        "Text": {
                                            "Charset": CHARSET,
                                            "Data": BODY_TEXT_70,
                                        },
                                    },
                                    "Subject": {
                                        "Charset": CHARSET,
                                        "Data": SUBJECT,
                                    },
                                },
                                Source=SENDER,
                            )
                        except ClientError as e:
                            print(e.response["Error"]["Message"])
                        else:
                            print("Email sent! Message ID:"),
                            print(response["MessageId"])

                # if Access Key Age is greater then 80 days, send email alert
                if active_days == datetime.timedelta(days=int(os.environ["days_80"])):
                    userTags = iam.list_user_tags(UserName=keyValue["UserName"])
                    email_tag = list(
                        filter(lambda tag: tag["Key"] == "Email", userTags["Tags"])
                    )
                    user1_tag = list(filter(lambda tag: tag['Key'] == 'UserType', userTags['Tags']))
                    
                    if(len(user1_tag) == 1):
                            user1tag = user1_tag[0]['Value']
                            if user1tag == "Employee":
                                iam.update_access_key(AccessKeyId=UserAccessKeyID,Status='Inactive',UserName=IAMUserName)
                                print("Status has been updated to Inactive")
                    
                                if len(email_tag) == 1:
                                    email = email_tag[0]["Value"]
                                    email_80_employee.append(email)
                                    print(
                                        "The User: ",
                                        IAMUserName,
                                        ", with the email: ",
                                        email,
                                        ", is having access key age is 80 days",
                                    )
                                    
            
                                    email_unique = list(set(email_80_employee))
                                    print("Email list: ", email_unique)
                                    RECIPIENTS = email_unique
                                    SENDER = os.environ["sender_email"]
                                    print("Sender: ", SENDER)
                                    AWS_REGION = os.environ["region"]
                                    SUBJECT = os.environ["SUBJECT"]
                                    BODY_TEXT_80_employee = os.environ["BODY_TEXT_80_employee"]
                                    BODY_HTML_80_employee = os.environ["BODY_HTML_80_employee"]
                                    CHARSET = "UTF-8"
                                    client = boto3.client("ses", region_name=AWS_REGION)
                                    try:
                                        response = client.send_email(
                                            Destination={
                                                "ToAddresses": RECIPIENTS,
                                            },
                                            Message={
                                                "Body": {
                                                    "Html": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_HTML_80_employee,
                                                    },
                                                    "Text": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_TEXT_80_employee,
                                                    },
                                                },
                                                "Subject": {
                                                    "Charset": CHARSET,
                                                    "Data": SUBJECT,
                                                },
                                            },
                                            Source=SENDER,
                                        )
                                    except ClientError as e:
                                        print(e.response["Error"]["Message"])
                                    else:
                                        print("Email sent! Message ID:"),
                                        print(response["MessageId"])
                            
                            
                            elif user1tag == "Machine":
                                print(user1_tag)
                                
                                if len(email_tag) == 1:
                                    email = email_tag[0]["Value"]
                                    email_80_machine.append(email)
                                    print(
                                        "The User: ",
                                        IAMUserName,
                                        ", with the email: ",
                                        email,
                                        ", is having access key age is greater then 90 days",
                                        )
                                    email_unique = list(set(email_80_machine))
                                    print("Email list: ", email_unique)
                                    RECIPIENTS = email_unique
                                    SENDER = os.environ["sender_email"]
                                    print("Sender: ", SENDER)
                                    AWS_REGION = os.environ["region"]
                                    SUBJECT = os.environ["SUBJECT"]
                                    BODY_TEXT_80_machine = os.environ["BODY_TEXT_80_machine"]
                                    BODY_HTML_80_machine = os.environ["BODY_HTML_80_machine"]
                                    CHARSET = "UTF-8"
                                    client = boto3.client("ses", region_name=AWS_REGION)
                                    try:
                                        response = client.send_email(
                                            Destination={
                                                "ToAddresses": RECIPIENTS,
                                            },
                                            Message={
                                                "Body": {
                                                    "Html": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_HTML_80_machine,
                                                    },
                                                    "Text": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_TEXT_80_machine,
                                                    },
                                                },
                                                "Subject": {
                                                    "Charset": CHARSET,
                                                    "Data": SUBJECT,
                                                },
                                            },
                                            Source=SENDER,
                                        )
                                    except ClientError as e:
                                        print(e.response["Error"]["Message"])
                                    else:
                                        print("Email sent! Message ID:"),
                                        print(response["MessageId"])            

                # if Access Key Age is greater then 90 days, send email alert and inactive access keys
                if active_days >= datetime.timedelta(days=int(os.environ["days_90"])):
                    userTags = iam.list_user_tags(UserName=keyValue["UserName"])
                    email_tag = list(
                        filter(lambda tag: tag["Key"] == "Email", userTags["Tags"])
                    )
                    user2_tag = list(
                        filter(lambda tag: tag["Key"] == "UserType", userTags["Tags"])
                    )
                    if len(user2_tag) == 1:
                            user2tag = user2_tag[0]["Value"]
                            if user2tag == "Employee":
                                print(user2_tag)
                                iam.delete_access_key(
                                    AccessKeyId=UserAccessKeyID,
                                    UserName=IAMUserName,
                                )
                                print("Status has been updated to deleted")
                                
                                if len(email_tag) == 1:
                                    email = email_tag[0]["Value"]
                                    email_90_employee.append(email)
                                    print(
                                        "The User: ",
                                        IAMUserName,
                                        ", with the email: ",
                                        email,
                                        ", is having access key age is greater then 90 days",
                                        )
                                    email_unique = list(set(email_90_employee))
                                    print("Email list: ", email_unique)
                                    RECIPIENTS = email_unique
                                    SENDER = os.environ["sender_email"]
                                    print("Sender: ", SENDER)
                                    AWS_REGION = os.environ["region"]
                                    SUBJECT = os.environ["SUBJECT"]
                                    BODY_TEXT_90_employee = os.environ["BODY_TEXT_90_employee"]
                                    BODY_HTML_90_employee = os.environ["BODY_HTML_90_employee"]
                                    CHARSET = "UTF-8"
                                    client = boto3.client("ses", region_name=AWS_REGION)
                                    try:
                                        response = client.send_email(
                                            Destination={
                                                "ToAddresses": RECIPIENTS,
                                            },
                                            Message={
                                                "Body": {
                                                    "Html": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_HTML_90_employee,
                                                    },
                                                    "Text": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_TEXT_90_employee,
                                                    },
                                                },
                                                "Subject": {
                                                    "Charset": CHARSET,
                                                    "Data": SUBJECT,
                                                },
                                            },
                                            Source=SENDER,
                                        )
                                    except ClientError as e:
                                        print(e.response["Error"]["Message"])
                                    else:
                                        print("Email sent! Message ID:"),
                                        print(response["MessageId"])
                                    
                                    
                            elif user2tag == "Machine":
                                print(user2_tag)
                                
                                if len(email_tag) == 1:
                                    email = email_tag[0]["Value"]
                                    email_90_machine.append(email)
                                    print(
                                        "The User: ",
                                        IAMUserName,
                                        ", with the email: ",
                                        email,
                                        ", is having access key age is greater then 90 days",
                                        )
                                    email_unique = list(set(email_90_machine))
                                    print("Email list: ", email_unique)
                                    RECIPIENTS = email_unique
                                    SENDER = os.environ["sender_email"]
                                    print("Sender: ", SENDER)
                                    AWS_REGION = os.environ["region"]
                                    SUBJECT = os.environ["SUBJECT"]
                                    BODY_TEXT_90_machine = os.environ["BODY_TEXT_90_machine"]
                                    BODY_HTML_90_machine = os.environ["BODY_HTML_90_machine"]
                                    CHARSET = "UTF-8"
                                    client = boto3.client("ses", region_name=AWS_REGION)
                                    try:
                                        response = client.send_email(
                                            Destination={
                                                "ToAddresses": RECIPIENTS,
                                            },
                                            Message={
                                                "Body": {
                                                    "Html": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_HTML_90_machine,
                                                    },
                                                    "Text": {
                                                        "Charset": CHARSET,
                                                        "Data": BODY_TEXT_90_machine,
                                                    },
                                                },
                                                "Subject": {
                                                    "Charset": CHARSET,
                                                    "Data": SUBJECT,
                                                },
                                            },
                                            Source=SENDER,
                                        )
                                    except ClientError as e:
                                        print(e.response["Error"]["Message"])
                                    else:
                                        print("Email sent! Message ID:"),
                                        print(response["MessageId"])
