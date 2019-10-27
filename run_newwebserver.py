#!/usr/bin/env python3
import sys
import boto3
import subprocess
import time
import logger
import urllib
import usermenu
from botocore.exceptions import ClientError


client = boto3.client('ec2')
ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')


#EC2 Instance is created here with the Tag Specifications and Security Groups as well as the installation of the Apache Server  
#==================================================================
#==================================================================
#def createInstance():
usercmd='ls -a'

def createInstance():
    instance_name = input ("Please Enter the Name of your Instance: ")
    if instance_name == "":
        instance_name = 'RobertS1-Instance4Assignment'
    bucket_name = 'rob5768435425'
    print('Starting instance. This may take a moment.')
    instance = ec2.create_instances(
    ImageId='ami-047bb4163c506cd98',
    MinCount=1,
    MaxCount=1,
    KeyName= 'RSolomon1912',
    Monitoring = {'Enabled' : True},
    UserData ='''
       #!/bin/bash
       yum update
       yum install httpd -y
       service httpd start
                 ''',
    #Monitoring = {Enabled : true},
    TagSpecifications=[
        {
            'ResourceType':'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': instance_name
		},
            ]
        },
    ],
    SecurityGroupIds=['sg-0acbfdc4b647eb4cc'],  #HTTP and SSH
    InstanceType='t2.micro'
    )
    print (instance[0].id)


    #Adding a Tag to keep track of Instance
    name_tag = {'Key': 'Name', 'myValue': instance_name}
    instance[0].create_tags

    urllib.request.urlretrieve('http://devops.witdemo.net/image.jpg', 'wit-image.jpg') #curl for python

    s3.Object(bucket_name, 'wit-image.jpg').put(Body=open('wit-image.jpg', 'rb'),ACL='public-read') #puts the image in bucket
    instance[0].wait_until_running()
    instance[0].reload()
    print('Public IP:',instance[0].public_ip_address)
    ip_add=instance[0].public_ip_address

    cmd1 ="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " '" + usercmd + "'"
    print(cmd1)

    cmd_w0="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'curl http://169.254.169.254/latest/meta-data/local-ipv4' > meta.json"
    print(cmd_w0)
    cmd_w1="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \"<html>\" > index.html'"
    print(cmd_w1)
    cmd_w2="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \'Private IP Address:\' >> index.html'"
    print(cmd_w2)
    cmd_w3="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html'"
    print(cmd_w3)
    cmd_w4="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \"<br>The WIT Image is located here:<br> \" >> index.html'"
    print(cmd_w4)
    cmd_w5="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \"<img src=\"https://"+bucket_name+".s3-eu-west-1.amazonaws.com/"+"wit-image.jpg\">\" >> index.html'"
    print(cmd_w5)
    cmd_w6="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'sudo cp index.html /var/www/html'"
    print(cmd_w6)

    subprocess.call(cmd1, shell=True)

    time.sleep(30)

#All processes above this script are called through the subprocess module below to append the relevant objects to the index page and s3 bucket
    subprocess.call(cmd_w0, shell=True)
    subprocess.call(cmd_w1, shell=True)
    subprocess.call(cmd_w2, shell=True)
    subprocess.call(cmd_w3, shell=True)
    subprocess.call(cmd_w4, shell=True)
    subprocess.call(cmd_w5, shell=True)
    subprocess.call(cmd_w6, shell=True)



#sleep time is set to 80 seconds due to cloudwatch setting up and instance setup process with website
    time.sleep(80)

#view cpu runtime
def cloudwatch_monitoring_cpu_usage_EC2():
  subprocess.call('python3 cloudwatch-inst-cpu.py ',shell=True)

#lists all instances and its state
def list_instances():
    for instance in ec2.instances.all():
        print (instance.id, instance.state)

#stops all instances
def stop_instances():
    for instance in ec2.instances.all():
        print (instance.id, instance.state)
        response = instance.stop()
        print (response)


#terminates all instances
def terminate_instances():
    decision = input ("Are you sure you want to delete all instances? (y/n) ")
    if decision == 'y':
        print("All Instances are terminated!")
        for instance in ec2.instances.all():
            print (instance.id, instance.state)
            response = instance.terminate()
            print (response)
    else:
        print("Termination aborted! ")
        
#Lists buckets and its contents
def list_buckets_and_contents():
    #s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print (bucket.name)
        print("--")
        for item in bucket.objects.all():
            print ("\t%s" % item.key)



# The main method is the method which controls the menu and flow of the program.
# All menus are called from the usermenu.py module in this directory. 
def main():
    usermenu.start_awsmenu()
    time.sleep(2)
    usermenu.aws_main_menu()

choice = None
while choice != '0':
    usermenu.start_awsmenu()
    time.sleep(2)
    usermenu.aws_main_menu()

    choice = input("Please enter your choice >>> ")
    if choice == '1':
     print('loading...')
     time.sleep(2)
     usermenu.aws_instance_manager()
     submenu_choice = input("Please enter your choice >>> ")


     # this while loop controls the "Instance Manager" menu
     while submenu_choice != '0':
       usermenu.aws_instance_manager()
       submenu_choice = input("Please enter your choice >>> ")
       if submenu_choice == '1':
           print('loading...')
           time.sleep(2)
           createInstance()
       if submenu_choice == '2':
           print('loading...')
           time.sleep(2)
           list_instances()
       if submenu_choice == '3':
           print('loading...')
           time.sleep(2)
           terminate_instances()
       if submenu_choice == '4':
           print('loading...')
           time.sleep(2)
           cloudwatch_monitoring_cpu_usage_EC2()


    if choice == '2':
       print('loading...')
       time.sleep(2)
       bucket_choice = None
       usermenu.aws_bucket_manager()


       # This while loop cntrols the "Bucket Manager" menu
       while bucket_choice != '0':
           usermenu.aws_bucket_manager()
           bucket_choice = input("Please enter your choice >>> ")
           if bucket_choice == '1':
               print('loading...')
               time.sleep(2)
               list_buckets_and_contents()

if __name__ == '__main__':
#runs main routine  
  main()

