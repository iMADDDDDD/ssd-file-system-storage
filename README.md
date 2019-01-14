# SSD - Secure File System Storage

**Updates:**

13/01/2019: added captcha security, session time out and email 
email logs : autosecuremail@gmail.com /  project2019secure
Reset password doesn't work yet, error 111 connection refused

12/01/2019: added a project for security features / database architecture

![alt text](https://github.com/iMADDDDDD/ssd-file-system-storage/blob/master/DataBase.jpg)

**Technology:** 

 - [Python (Flask)](http://flask.pocoo.org/)
 - [PostgreSQL](https://www.postgresql.org/) (Database)
 - 2-factor authentication: [PyOTP](https://pyotp.readthedocs.io/en/latest/) (Only a suggestion, if you have a better idea please share)

**Goal:** Implementing a *secure* client/server file system storage

**Requirements:**

 - Clients must be able to register to the server
 - Clients must be able to log in to the server
 - Authenticated clients must be able to store files
 - Authenticated clients must be able to download files if they are allowed to
 - Authenticated clients must be able to delete files if they are allowed to
 - Server is not a trusted entity, thus, securely transfer the public keys to the client and check ownership
 - An administrator has to manually allow a client to log in after registration request
 - 2-factor authentication must be implemented
 - An administrator can deactivate/delete a user
 - Implementation of group files (ability to delete only if enough members allow it)

**TODO**:
- User control panel (part of web application)
- Administrator control panel (part of web application)
- Notification system for both users & admins (for deletion requests...)
- Server-side implementation (upload/download/delete operations)
- Think about security measures (RSA, AES, password policies...)

**Fast tutorial**

How to install python3.6
- sudo apt update
- sudo apt install python3.6

Didn't work for me to install python3.6 on ubuntu 16, I had to upgrade to ubuntu 18.04

How to install flask on ubuntu/linux 
- create folder /project ang open it
- check if virtualenv is already install else install it
(once downloaded you can run it with: "source venv/bin/activate" command
- pip install flask
- then copy
ref : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

How to install postgresql
- sudo apt update
- sudo apt install postresql postgresql-contrib
ref : https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

