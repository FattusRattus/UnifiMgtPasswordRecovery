# Unifi Management Controller password recovery/reset tool
# By Ratware
# Some original code and also cobbled together from various sources

from passlib.hash import sha512_crypt as sha512
import random
import string

import readchar

from pymongo import MongoClient

def clean_exit():
   global client
   
   client.close()

   keyin = "x"
   keyin = raw_input ("\nPress enter to close")

   # Uncomment below line when compiling with PyInstaller
   #sys.exit()
   exit()

def get_unifi_version():
   global client

   # Load admin database
   db = client.admin

   # Get data
   try:
      record = db.command('getCmdLineOpts')
   except Exception as error:
      print "\nUnable to access Unifi Mgt Controller Mongo Database!"
      print "Are you sure it is running?"
      clean_exit()

   # Filter out database path
   try:
      dbpath = record['parsed']['dbpath'].split(',')[0]
   except:
      try:
         # Later version suse upper case P
         dbpath = record['parsed']['storage']['dbPath'].split(',')[0]
      except:
         print "Unable to determine database path..."
         clean_exit()

   print "Database Path:            ", dbpath

   # Set name and full path to file that contains Unifi Mgt Controller version
   version_db = dbpath + "\\version"

   print "Unifi Version DB File:    ", version_db

   # Open file and read version
   version_file = open(version_db,"r")
   version = version_file.read()
   version_file.close()

   print "Unifi Version:            ", version

   # Split version into component parts
   version_high = int(version.split('.')[0])
   version_mid = int(version.split('.')[1])
   version_low = int(version.split('.')[2])

   if version_high < 4:
      print "Unifi Password Encrypted:  NO"
      return(False)

   if version_high == 4 and version_mid < 8:
      print "Unifi Password Encrypted:  NO"
      return(False)

   if version_high == 4 and version_mid == 8 and version_low <= 15:
      print "Unifi Password Encrypted:  NO"
      return(False)
   else:
      print "Unifi Password Encrypted:  YES"
      return(True)

def recover_plain_text_passwd():
   global client

   # Load database 'ace'
   db = client.ace

   # Get cursor for searching collection
   cursor = db.admin.find()

   try:
      for document in cursor:
         print "\nAttempting to recover pain text login & password...\n"

         print "Login:    " + (document['name'])
         print "Password: " + (document['x_password'])
   except Exception as error:
      print "\nUnable to access Unifi Mgt Controller Mongo DB - is it running?"
      clean_exit()


def export_hash():
   global client

   # Load database 'ace'
   db = client.ace

   # Get cursor for searching collection
   cursor = db.admin.find()

   try:
      for document in cursor:
         print "\nAttempting to recover login & password hash...\n"

         print "Login:         " + (document['name'])
         print "Password Hash: " + (document['x_shadow'])
         
         print "\nThis will create or append to local folder file: unifi-hash.txt"
         print "Use HASHCAT with hash optioon: -m 1800\n"

         # Open file unifi-hash.txt and append SHA512crypt password hash
         hash_file = open("unifi-hash.txt","a+")
         hash_file.write((document['x_shadow']))
         hash_file.write("\n")
         hash_file.close()
         
   except Exception as error:
      print "\nUnable to access Unifi Mgt Controller Mongo DB - is it running?"
      clean_exit()

def reset_warning():
   print "\nNOTE: USING THIS OPTION MAY POTENTIALLY DAMAGE YOUR UNIFI INSTALLATION."
   print "ENSURE YOU HAVE BACKED UP YOUR UNIFI INSTALLATION FIRST."
   print "Closing the app and service and ZIPping the installation root folder should"
   print "be a good enough backup.\n"
   print "CONTINUE AT YOUR OWN RISK!\n"
   print "Press Y to continue or any other key to exit"

   x = readchar.readkey()

   if x != "Y":
      clean_exit()


def reset_hash_1234():
   global client

   reset_warning()
   
   # Load database 'ace'
   db = client.ace

   # Get cursor for searching collection
   cursor = db.admin.find()

   for document in cursor:
      print "\nAttempting to recover login...\n"
      print "Login:              " + (document['name'])

   # Update new password in database
   login = (document['name'])      
   db.admin.update(
      {"name" : login},
      {
         '$set': { "x_shadow": "$6$kn8u0o5IAdr6$A1Bq6sslgjSa2vYU9VYrMmyzYgqOtJGFQDVgVyXUHx5MYBCXPT9Xlw2sgVV4MDgb3lB4879te4.7StEKsWD020"}
      }
   )

   print "Password reset to:  1234"


def reset_hash():
   global client

   reset_warning()

   NewPasswd = "1234"
   NewPasswd = raw_input ("\nInput new password and press <enter>: ")   

   # Create 8 char random salt
   SHA512_Salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

   # Create SHA512crypt hash of password
   SHA512_Passwd = sha512.encrypt(NewPasswd, rounds = 5000, salt = SHA512_Salt)

   # Load database 'ace'
   db = client.ace

   # Get cursor for searching collection
   cursor = db.admin.find()

   for document in cursor:
      print "\nAttempting to recover login...\n"
      print "Login:              " + (document['name'])

   # Update new password in database
   login = (document['name'])      
   db.admin.update(
      {"name" : login},
      {
         '$set': { "x_shadow": SHA512_Passwd}
      }
   )

   print "Password reset to:  " + NewPasswd


# MAIN PROGRAM

print "\n"
print "Ratware Unifi Mgt Login & Password Recovery/Reset Tool"
print "======================================================\n"

print "Attempting to access Mongo Database...\n"

# Connect to Mongo database
client = MongoClient("mongodb://localhost:27117")

# Check Unifi version and see if password in Databse is encrypted
isPasswdEncrypted = get_unifi_version()

if isPasswdEncrypted == False:
   recover_plain_text_passwd()
   clean_exit()

# Password must be encrypted, give several options
print "\nUnifi password is encrypted, please choose from the following options:\n"
print "  1) Print and export SHA512 hash to a file for cracking in Hashcat or similar."
print "  2) Reset password to '1234'."
print "  3) Reset password to your choice (note: it is displayed onscreen)."
print "\n Or any other key to exit menu.\n"

x = readchar.readkey()
print "Option choice: ", x

if x == "1":
   export_hash()
   clean_exit()

if x == "2":
   reset_hash_1234()
   clean_exit()

if x == "3":
   reset_hash()
   clean_exit()

clean_exit()

