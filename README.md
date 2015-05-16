# imapy
(Another) Python imap package on top of imaplib with the intention to keep things simple but flexible.
Therefor, searching and fetching, dealing with mailboxes etc. is simplified but messages are only parsed in a minimal way by default. They are returned as (simple) Message objects created by the python standard email module in the form of a generator.
```Python
uids, msgs = mbox["INBOX"](UNSEEN)
```
So you can iterate over found messages and apply several parsing functions to them suitable to your needs.
Hence, the included utility module "imapy.utils" contains already a lot of parsing functions ... This modular approach (more function than class based) allows adding needed parsing functions not already included in imapy.utils in an easy way. Extend the lib to your needs!

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
