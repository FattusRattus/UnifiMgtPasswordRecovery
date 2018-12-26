# UnifiMgtPasswordRecovery
Unifi management controller password recovery/reset

Description
----
The script first started way back around V3.2.10 or earlier of the Unifi Controller. It came about due to clients in IT support losing/forgetting/failing to  document their Unifi Controller credentials, or on boarding clients with the same/similar issue. The first incarnation just accessed the Mongo Database and  displayed the plain text login & password from the below reference (now updated, so no longer exists in its original form)

Mongo Client commands to recover password: 

https://help.ubnt.com/hc/en-us/articles/204909294-UniFi-How-to-recover-lost-password-and-username

These community pages show similar info to what was on the original Unifi page:

https://community.ubnt.com/t5/UniFi-Wireless/Lost-UniFi-Controller-Login-Password/td-p/179127
https://community.ubnt.com/t5/UniFi-Wireless/Password-reset/td-p/182435/page/2

Later on, I found it no longer worked as Unifi had started to encrypt the passwords in the Mongo database with SHA512crypt (see Bugfixes/Changes from 4.8.15 in  the link below):
https://community.ubnt.com/t5/UniFi-Updates-Blog/UniFi-4-8-18-is-released/ba-p/1555743

So as of V4.8.15, the password was encrypted, so I had to find a new method - the easiest, was to just generate a hash for a simple password (1234) within the  app itself and make a copy of the hash to use for password resets.

I have also added 2 more options - exporting the has for cracking with something like hashcat (tested and working using -m 1800 option) and the option of  choosing your own password for the reset.

As we only dealt with Windows installs, I have only tested it against these in the following versions:


Windows EXEs
----
Standalone EXE is the Build folder (compiled with PyInstaller to x86 app)

Requirements
----
It seems the command have changed in the later versions of pymongo, so you have to install the older version that is compatible. You only need PyInstaller if  you want to compile the code to an EXE
```
pip install pymongo==3.4.0
pip install readchar
pip install passlib
pip install pyinstaller 
```


Usage
----
Just run the Python code or compiled EXE.

Tested against Unifi Controller versions:
----
```
V3.2.10 (tested on Win8.1 x86)
V4.8.15 (tested on Win8.1 x86)
V4.8.18 (tested on Win8.1 x86) - my version has an odd issue in that you can't change the password in the app itself.
V5.0.6 (tested on Win8.1 x86)
V5.2.9 (tested on Win8.1 x86)
V5.5.24 (tested on Win8.1 x86) 
V5.6.29-LTS (tested on Win8.1 x86)
V5.9.29 (tested on Win8.1 x64) - could not get Unifi installation working on x86.
```

Not done any testing on Linux installation yet.
