# A helper module to simply print menus to the user.
# This python module keeps the main code clean and readable.

def start_awsmenu():
  print('\n######################################################################')
  print('#                     AWS Manager                                      #')
  print('########################################################################')
  print('#        Welcome to AWS Manager. A program to help                     #')
  print('#           you manage your AWS instances.                             #')
  #print('#        Please enter the name of your .pem key below,                #')
  print('#        Without the extension and ensure it is in                     #')
  print('#                the current directory.                                #')
  print('#                                                                      #')
  print('######################################################################\n')

def aws_main_menu():
  print('\n|====================================================================|')
  print('|                         Main Menu                                    |')
  print('|======================================================================|')
  print('| 1) Instance Manager                                                  |')
  print('| 2) Bucket Manager                                                    |')
  print('| 0) Exit                                                              |')
  print('|______________________________________________________________________|\n')


def aws_instance_manager():
  print('\n|====================================================================|')
  print('|                         Instance Manager                             |')
  print('|======================================================================|')
  print('| 1) Create an EC2 Instance                                            |')
  print('| 2) List Instances                                                    |')
  print('| 3) Terminate All Instances                                           |')
  print('| 4) View CPU Average Utilization Time of an Instance                  |')
  print('| 0) Return                                                            |')
  print('|______________________________________________________________________|\n')


def aws_bucket_manager():
  print('\n|======================================================================|')
  print('|                         Bucket Manager                                 |')
  print('|========================================================================|')
  print('| 1) List Buckets and Contents                                           |')
  print('| 0) Return                                                              |')
  print('|________________________________________________________________________|\n')