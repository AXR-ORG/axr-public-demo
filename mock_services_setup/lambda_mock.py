from contextlib import contextmanager
import boto3
import json

@contextmanager
def mock_lambda_setup(iamClient, lambdaClient, functionName):
    try:
        # Create a mock IAM role
        role_name = 'MyLambdaRole'
        iamClient.create_role(RoleName=role_name, AssumeRolePolicyDocument='{}')
        
        # Create a custom policy
        policy_name = 'MyCustomPolicy'
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "*",
                    "Resource": "*",
                    "Effect": "Allow"
                }
            ]
        }
        response = iamClient.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document)
        )
        policy_arn = response['Policy']['Arn']
        
        # Attach the custom policy to the role
        iamClient.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)

        # Create the Lambda function with the mock role
        lambdaClient.create_function(
            FunctionName=functionName,
            Runtime='python3.8',
            Role='arn:aws:iam::123456789012:role/{}'.format(role_name),
            # Handler='lambda_function.lambda_handler',
            Handler='lambda_function.handler',
            Code={
                'ZipFile': b'bytes'
            },
            Timeout=300,
            MemorySize=512
        )
        
        return True
        
    except Exception as ex:
        print("error while creating lambda")
        print(str(ex))
        
        return False