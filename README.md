# imapy
Python imap package on top of imaplib

# Usage
```Python
from imapy import Imapy

# fetch latest messages and print header to terminal
with Imapy(host) as mbox:
   mbox.login(user, password)
   uids, msgs = mbox(count=5)
   for msg in msgs:
      print msg["Subject"], msg["From"], msg["Date"]

# ==========

from imapy.imapy import create_engine
from imapy.utils import load_config
from imapy import criteria

# read account data from JSON-config file
account_data = load_config("config.json")["accounts"]["default"]

mbox = create_engine(**account_data)
uids, msgs = mbox(criteria.UNSEEN)
[...]
mbox.kill()

# using encoded password
from base64 import b64decode
mbox = create_engine(decoder=b64decode, **account_data)

#change mailbox and parse header from fetched messages
from imapy.utils import parse_header
uids, msgs = mbox["INBOX.Sent"](count=10)
   for msg in msgs:
      print parse_header(msg)
      
to be continued [...]
```
