import boto3
import os
import urllib.parse

SNS_TOPIC_ARN = "" #sns-arn
API_BASE = "" #api-gw-endpoint-for-token

def lambda_handler(event, context):
    sns = boto3.client('sns')
    task_token = event['TaskToken']
    user = event['User']

    username = user['UserName']
    inactive_days = user['InactiveDays']
    mfa_enabled = user['MFAEnabled']
    admin_access = user['AdminAccess']

    safe_token = urllib.parse.quote(task_token, safe='')

    approve_url = f"{API_BASE}/approve?token={safe_token}"
    deny_url = f"{API_BASE}/deny?token={safe_token}"

    fallback_message = (
        f"Risky IAM user detected!\n\n"
        f"User: {username}\n"
        f"Inactive Days: {inactive_days}\n"
        f"MFA Enabled: {mfa_enabled}\n"
        f"Admin Access: {admin_access}\n\n"
        f"Approve: {approve_url}\n"
        f"Deny: {deny_url}"
    )
    subject = f"Approval Needed: IAM User {username}"

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=fallback_message, 
        MessageStructure='raw'
    )
    return {
        "status": "approval_sent",
        "user": username
    }
