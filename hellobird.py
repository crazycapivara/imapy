"""
    hellobird.py
    ~~~~~~~~~~~~
    imapy example(s)
"""

from imapy import Imapy
from imapy import utils

HOST = "imap.gmail.com"
UID  = "You"
PWD  = "YourPwd"

def print_header():
  with Imapy(HOST) as mbox:
    mbox.login(HOST, UID)
    uids, msgs = mbox(count=5)
    for msg in msgs:
      header = utils.parse_header(msg)
      print header

if __name__ == "__main__":
  print_header()
