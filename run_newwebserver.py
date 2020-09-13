#!/usr/bin/env python3
import boto3
import subprocess
import time
import urllib

# import logging


cloudwatch = boto3.resource('cloudwatch')

usercmd='ls -a'


def webserver():
#EC2 Instance is created here with the Tag Specifications and Security Groups as well as the installation of the Apache Server  
#==================================================================
#==================================================================

  
  ec2 = boto3.resource('ec2')
  s3 = boto3.resource("s3")

  instance_name = 'myinstance2020'
  bucket_name=  'mybucket2354r'

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

  SecurityGroupIds=['sg-05b63d7174b9dfbe4'],  #HTTP and SSH
  InstanceType='t2.micro'
  )
  print (instance[0].id)


  #Adding a Tag to keep track of Instance
  name_tag = {'Key': 'Name', 'myValue': instance_name}
  instance[0].create_tags

  instance[0].wait_until_running()
  instance[0].reload()
  print('Public IP:',instance[0].public_ip_address)
  print('Public DNS:',instance[0].public_dns_name)
  print('----------------------------------------')
  print('----------------------------------------')
  print('----------------------------------------')
  print('----------------------------------------')

  
  #Retrieving image from the associated link using  urlretrieve command from the irllib library

  urllib.request.urlretrieve('http://devops.witdemo.net/image.jpg', 'wit-image.jpg') #curl for python
  print("Hello World")
  #Creating Empty bucket first
  try:
    response = s3.create_bucket(Bucket= bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    print(response)
  except Exception as error:
    print (error)
  # time.sleep(20)


  try:
    response = s3.Object(bucket_name, 'wit-image.jpg').put(Body=open('wit-image.jpg', 'rb'),ACL='public-read') #puts the image in bucket
    print (response)
  except Exception as error:
    print (error)
    # time.sleep(30)

  ip_add=instance[0].public_ip_address

  time.sleep(30)

  cmd1 ="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " '" + usercmd + "'"
  print(cmd1)

  cmd2="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'curl http://169.254.169.254/latest/meta-data/local-ipv4' > pr-ip-meta.json"
  print(cmd2)

  cmd3="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'curl http://169.254.169.254/latest/meta-data/placement/availability-zone' > avz.json"
  print(cmd3)
  
  cmd_w1="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \"<html>\" > index.html'"
  print(cmd_w1) 
  cmd_w2="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \'Private IP Address: \' >> index.html'"
  print(cmd_w2)
  cmd_w3="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html'"
  print(cmd_w3)
  cmd_w4="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \"<br> Availability Zone: \" >> index.html'"
  print(cmd_w4)
  cmd_w5="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'curl http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html'"
  print(cmd_w5)
  cmd_w6="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \"<br>The WIT Image is located here: <br>\" >> index.html'"
  print(cmd_w6)
  cmd_w7="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'echo \"<img src=\"https://"+bucket_name+".s3-eu-west-1.amazonaws.com/"+"wit-image.jpg\">\" >> index.html'"
  print(cmd_w7)
  cmd_w8="ssh -o StrictHostKeyChecking=no -i RSolomon1912.pem ec2-user@" + ip_add + " 'sudo cp index.html /var/www/html'"
  print(cmd_w8)

 

  #All processes above this script are called through the subprocess module below to append the relevant objects to the index page and s3 bucket
  subprocess.call(cmd1, shell=True)

  subprocess.call(cmd2, shell=True)
  subprocess.call(cmd3, shell=True)
  subprocess.call(cmd_w1, shell=True)
  subprocess.call(cmd_w2, shell=True)
  subprocess.call(cmd_w3, shell=True)
  subprocess.call(cmd_w4, shell=True)
  subprocess.call(cmd_w5, shell=True)
  subprocess.call(cmd_w6, shell=True)
  subprocess.call(cmd_w7, shell=True)

  time.sleep(30)
  subprocess.call(cmd_w8, shell=True) 
  print('Instance & Bucket finished loading!')