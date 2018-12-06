# SSD - Secure File System Storage
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

A link that will probably be useful: [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
