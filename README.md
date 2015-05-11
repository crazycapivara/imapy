# imapy
Python imap package on top of imaplib

# Usage
```Python
from imapy.imapy import Imapy

# fetch latest messages and print header to terminal
with Imapy(host) as mbox:
   mbox.login(user, password)
   uids, msgs = mbox[5]
   for msg in msgs:
      print msg["Subject"], msg["From"], msg["Date"]
      
to be continued [...]
```
