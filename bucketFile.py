#!/usr/bin/env python3
import sys
import boto3
import run_newwebserver
s3 = boto3.resource("s3")


# #Lists buckets and its contents
def list_buckets_and_contents():
  try:
    for bucket_name in s3.buckets.all():
      print (bucket_name)
      print("-------------------------------------------------")
    for item in bucket_name.objects.all():
      print("\t%s" % item.key)
  except Exception:
    print('No Buckets Found!')
  

# #Delete entire bucket
def delete_bucket():
  for bucket_name in s3.buckets.all():
    try:
      response = bucket_name.delete()
      print (response)
    except Exception as error:
      print (error)


# #delete contents in bucket
def delete_contents():
  for bucket_name in s3.buckets.all():
    for key in bucket_name.objects.all():
      try:
        response = key.delete()
        print (response)
      except Exception as error:
        print (error)