#!/usr/bin/env python3
import boto3
import sys

from datetime import datetime, timedelta

ec2 = boto3.resource('ec2')
cloudwatch = boto3.resource('cloudwatch')


# #Lists the number of instances
def list_inst():
	for instance in ec2.instances.all():
	    print (instance.id, instance.state)

# #stops the current instance running
def stop_inst():
    try:
        for instance in ec2.instances.all():
            print (instance.id, instance.state)
            response = instance.stop()
            print (response)
    except Exception:
        print('Unable to stop instance!')



# #terminates the current instance
def term_inst():
    try:
        for instance_id in sys.argv[1:]:
            instance = ec2.Instance(instance_id)
            response = instance.terminate()
            print (response)
    except Exception:
        print('Unable to terminate!')


#metric check here (add more metrics for cloudwatch monitoring)
def cloudWatch():
  instid = input("Please enter instance ID: ")

  metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2', 
                                             MetricName='CPUUtilization', 
                                             Dimensions=[{'Name':'InstanceId', 'Value': instid}])

  for metric in metric_iterator:
      response = metric.get_statistics(StartTime=datetime.now() - timedelta(minutes=65),     # 5 minutes ago
                                       EndTime=datetime.now() - timedelta(minutes=60),       # now
                                       Period=300,                                           # 5 minute intervals
                                       Statistics=['Average'])
      print ("Average CPU utilisation:", response['Datapoints'][0]['Average'])
  #   print (response)   # for debugging only