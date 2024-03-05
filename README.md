# Auto-Schedule Start & Stop EC2 Instances using AWS Lambda

## Background

In this guide, we will demonstrate how to automatically schedule the start and stop of EC2 instances using AWS Lambda and CloudWatch Events. By leveraging Lambda functions and CloudWatch Events, you can create a cost-effective solution to manage EC2 instance runtime based on a predefined schedule (eg, start at 8am and stop at 6pm). This guide assumes you already have a dummy EC2 instance created for testing purpose.

## 1. Create IAM Execution Role

- Log in to the AWS Management Console.
- Navigate to the IAM service.
- Click on Roles in the left navigation pane.
- Click on Create role.
- Under Select type of trusted entity, choose AWS service.
- Select Lambda as the service that will use this role.
- Click on Next: Permissions.
- Attach policies to the role that allow Lambda to interact with EC2 instances and CloudWatch Logs. Use the following managed policies:
   * "AWSLambdaBasicExecutionRole"
   * "AmazonEC2FullAccess"
- Click on Next: Tags (optional) and Next: Review.
- Enter a name and description for the role, then click on Create role.

## 2. Create Lambda Function

- Navigate to the Lambda service.
- Click on Create function.
- Choose Author from scratch.
- Enter a name for your Lambda function (e.g., "AutoScheduleEC2").
- Choose the appropriate runtime (e.g., Python 3.12).
- Under Permissions, select Use an existing role and choose the IAM role created in step 1.
- Click on Create function.
- In the function code editor, paste the Python code provided below and then click Deploy:

```bash
import boto3
import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    current_time = datetime.datetime.utcnow().time()
    start_time = datetime.time(8, 0)  # 8 AM UTC -> 9:00 AM CET
    end_time = datetime.time(17, 0)  # 5 PM UTC -> 6:00 PM CET

    if current_time >= start_time and current_time <= end_time:
        start_ec2_instances()
    else:
        stop_ec2_instances()

def start_ec2_instances():
    # Get instances that are stopped
    stopped_instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])

    # Start each stopped instance
    for reservation in stopped_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            ec2.start_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} started.")

def stop_ec2_instances():
    # Get instances that are running
    running_instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    # Stop each running instance
    for reservation in running_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Instance {instance_id} stopped.")
```

## 3. Add Trigger and Create EventBridge CloudWatch Event
- Click on your Lambda function "AutoScheduleEC2" created in step 2.
- In the Lambda function configuration page, scroll down to the **Designer** section.
- Click on **Add trigger**.
- Choose **EventBridge (CloudWatch Events)** as the trigger type.
- Configure the trigger as follows:
   * **Rule type**: Choose **Create a new rule**.
   * **Rule name**: Enter a name for the rule (e.g., "AutoScheduleEC2Trigger").
   * **Rule description**: Optionally, enter a description for the rule.
   * **Rule type**: Choose **Event pattern**.
   * **Event matching pattern**: Select **Schedule pattern**.
   * **Schedule pattern**: Enter `cron(0 8,18 ? * MON-FRI *)` to trigger the Lambda function every hour.
   * Leave other options as default.
- This schedule expression specifies the following:
    * Run at 8 AM and 6 PM (UTC time).
    * On Monday to Friday.
    * The ? indicates no specific day of the month.
    * The * indicates every month.
- Click on **Add** to add the trigger and create the EventBridge CloudWatch Event rule.
- Ensure that the Lambda function and the trigger are both enabled by checking the status in the top-right corner of the Lambda function configuration page.
- Click on **Save** to save the changes to the Lambda function configuration.

## Conclusion

In this guide, we have demonstrated how to automatically schedule the start and stop of EC2 instances using AWS Lambda and CloudWatch Events. By following the steps outlined above, you can create a cost-effective and efficient solution for managing EC2 instance runtime based on predefined schedules.