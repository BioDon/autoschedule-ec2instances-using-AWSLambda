import boto3
import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    current_time = datetime.datetime.utcnow().time()
    start_time = datetime.time(10, 0)  # 10 AM UTC -> 11:00 AM CET
    end_time = datetime.time(17, 0)  # 17 PM UTC -> 6:00 PM CET

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
