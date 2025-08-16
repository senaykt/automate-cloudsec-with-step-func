import boto3
import json

def lambda_handler(event, context):
    sfn = boto3.client('stepfunctions')
    
    # Get the TaskToken from query string
    params = event.get('queryStringParameters') or {}
    print(params)
    token = params.get('token')
    if not token:
        return {"statusCode": 400, "body": "Missing token"}
    
    # Determine path: /approve or /deny
    path = event.get('path', '').lower()
    if '/approve' in path:
        output = {
            "Payload": {
                "ApprovalStatus": "Approved"
            }
        }
        msg = "Approval recorded. Remediation will proceed."
    elif '/deny' in path:
        output = {
            "Payload": {
                "ApprovalStatus": "Rejected"
            }
        }
        msg = "Rejection recorded. No action will be taken."
    else:
        return {"statusCode": 400, "body": "Invalid path."}
    
    # Notify Step Functions
    try:
        sfn.send_task_success(
            taskToken=token,
            output=json.dumps(output)  # <== Important: must be a string
        )
        return {
            "statusCode": 200,
            "body": msg
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Callback failed: {str(e)}"
        }
