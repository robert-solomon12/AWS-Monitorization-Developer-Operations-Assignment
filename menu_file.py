import instanceFile
import bucketFile
import run_newwebserver
import sys

def webserverMenu():

  print('[[+++++++++++++++++++++++++++++++++++++++++++++++++++++++]]')
  print('[[========== WELCOME TO THE AWS WEBSERVER MENU ==========}]')
  print('[[+++++++++++++++++++++++++++++++++++++++++++++++++++++++]]')
  print('[[    Please choose from one of the following options:   ]]')
  print('[[ 1) Create Instance & Bucket                           ]]')
  print('[[ 2) List Instances                                     ]]')
  print('[[ 3) Stop Instances                                     ]]')
  print('[[ 4) Terminate All Instances                            ]]')
  print('[[ 5) View CPU Average Utilization Time of an Instance   ]]')
  print('[[-------------------------------------------------------]]')
  print('[[-------------------------------------------------------]]')
  print('[[ 6) List e3 Buckets                                    ]]')
  print('[[ 7) Delete contents in e3 Bucket                       ]]')
  print('[[ 8) Delete e3 Bucket                                   ]]')
  print('[[ 0) Exit                                               ]]') 


  option = input(" >>> ")
  if (option == '1'):
    run_newwebserver.webserver()
  elif (option =='2'):
    instanceFile.list_inst()
  elif (option =='3'):
    instanceFile.stop_inst()
  elif (option == '4'):
    instanceFile.term_inst()
  elif (option == '5'):
    instanceFile.cloudWatch()
  elif (option == '6'):
    bucketFile.list_buckets_and_contents()
  elif (option =='7'):
    bucketFile.delete_contents()
  elif (option == '8'):
    bucketFile.delete_bucket()
  elif (option == '0'):
   sys.exit()
  return

if __name__ == '__main__':
  #runs main routine  
  webserverMenu()