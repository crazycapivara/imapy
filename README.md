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

# ==========

from imapy.imapy import create_engine
from imapy.utils import load_config
import imapy.criterion

# read account data from JSON-config file
account_data = load_config("config.json")["accounts"]["default"]
mbox = create_engine(**account_data)

uids, msgs = mbox(criterion.UNSEEN)
[...]
mbox.kill()
      
to be continued [...]
```
