# -*- coding: utf-8 -*-
"""
	imapy.imapy
	~~~~~~~~~~~
	This module is implemented on top of imaplib and handles imap server
	communication stuff, like searching and fetching emails.
	Hereby, search results are returned in the form of a `generator`
	and messages itself as `email.message.Message` objects as created
	by the standard Python email library.
	For further parsing, decoding, etc. use the `imapy.utils` module! 

	:copyright: (c) 2015 by Stefan Kuethe.
	:license: GPLv3, see LICENSE.md for more details.
"""
from imaplib import IMAP4, IMAP4_SSL
from email import message_from_string
import criterion
try:
	from . addons.imapUTF7 import imapUTF7Decode as decode_imap_utf7
	UTF7_SUPPORT = True
except Exception as e:
	UTF7_SUPPORT = False

__author__ = "Stefan Kuethe"
__version__ = "0.1.1"

MESSAGE_ALL = "(BODY.PEEK[])"
MESSAGE_HEADER = "(BODY.PEEK[HEADER])"
MESSAGE_RFC822_ALL = "(RFC822)"
MESSAGE_RFC822_HEADER = "(RFC822.HEADER)"

def create_engine(host, user, password, ssl=False, decoder=None):
	"""Establish connection to default mailbox.
	
	In case password is encoded, you must pass the
	decoder	function as optional argument. 
	"""
	if ssl:
		mbox = Imapy_SSL(host)
	else:
		mbox = Imapy(host)
	if decoder:
		password = decoder(password)
	mbox.login(user, password)
	return mbox

class Imapy:
	def __init__(self, host):
		self.imap = IMAP4(host)

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.kill()

	def __call__(self, *args, **kwargs):
		"""Call function `query`.""" 
		return self.query(*args, **kwargs)

	def __getitem__(self, name):
		"""Call function `select_mbox`."""
		self.select_mbox(name)
		return self

	def get_uids(self, criteria=criterion.ALL):
		"""Return uids for given search `criteria`."""
		return self.imap.uid("search", None, criteria)[1][0].split()

	# maybe rename to get_msg_by_uid, because get_by_uid should return raw stuff!
	# or set parser like `parser=message_from_string`!?
	def get_by_uid(self, uid, msg_parts=MESSAGE_ALL, minimal=False, raw=False):
		"""Fetch selected message parts for given `uid`.

		:param msg_parts: string in the form of ``'(BODY.PEEK[...])'`` or ``'(RFC822)'``,
		                  defaults to ``'(BODY.PEEK[])'``
		:param minimal: if set to ``True`` only header will be fetched
		                and `msg_parts` is ignored
		:return: `email.message.Message` object
		"""
		if minimal:
			msg_parts = MESSAGE_HEADER
		status, msg = self.imap.uid("fetch", uid, msg_parts)
		if raw:
			return msg[0][1]
		return message_from_string(msg[0][1])

	# maybe tuple including uid should be returned!?
	# this function can be killed, because it is better to put code to query directly!?
	def get_result(self, uids, **kwargs):
		"""Return message generator for given `uids`.

		:**kwargs: see function `get_by_uid`
		"""
		for uid in uids:
			yield self.get_by_uid(uid, **kwargs)


	# rename to get_msgs!
	def query(self, criteria=criterion.ALL, count=False, reverse=False, **kwargs):
		"""Return uids and message generator for given search `criteria`.

		:param criteria: string containing all search criteria e. g. ``'(UNSEEN) (FROM "gabbo")'``
		:param count: number of messages to be returned
		:param reverse: if set to ``True`` messages are returned the other way round
		:**kwargs: see function `get_by_uid`
		:return: `list` uids, `email.message.Message` generator
		"""
		uids = self.get_uids(criteria)
		if count and len(uids) > 0:
			uids = uids[-count:]
		if reverse:
			uids.reverse()
		# create `generator`
		#result = ((uid, self.get_by_uid(uid, **kwargs)) for uid in uids)
		result = (self.get_by_uid(uid, **kwargs) for uid in uids)
		return (uids, result)
		#return (uids, self.get_result(uids, **kwargs))

	def copy(self, uid, folder):
		"""Copy message to given `folder`."""
		pass

	def move(self, uid, folder):
		"""Move message to given `folder`."""

	def delete(self, uid):
		"""Delete message."""
		pass

	def get_s(self):
		"""Return `imaplib.IMAP4` or `imaplib.IMAP4_SLL` object used by `Imapy`."""
		return self.imap

	def s(self, func_name, *args, **kwargs):
		"""Call `imaplib.IMAP4.func_name(*args, **kwargs)`.

		You can also use `Imapy.imap.func_name` instead ...
		e. g. mbox = Imapy(host)
		      `mbox.imap.list()` instead of `mbox.s("list")`
		"""
		return getattr(self.imap, func_name)(*args, **kwargs)

	def select_mbox(self, name):
		"""Change mailbox/folder.
		
		:param name: original raw (special utf7 encoded) mailbox name
		             as returned by function `get_mbox_names` with ``decode=False``
		"""
		return self.imap.select(name)

	def get_mbox_names(self, decode=False):
		"""Get mailbox names.

		:param decode: if ``True`` mailbox names are decoded using `special utf7 charset definition`
		               important, if you got international mailbox names with special characters

 		utf7 support from <http://slivlen-oss.googlecode.com/svn/trunk/projects/python/scripts/imapUTF7.py>
		"""
		mbox_info = self.imap.list()[1]
		mbox_names = [mbox.split()[-1].strip('"') for mbox in mbox_info]
		if decode and UTF7_SUPPORT:
			mbox_names = map(decode_imap_utf7, mbox_names)
		return mbox_names

	def make_mbox(self, name):
		"""Create new mailbox/folder."""
		pass

	def login(self, user, password):
		"""Log in to server and select default mailbox.

		:return: `tuple` with status messages
		"""
		status_login = self.imap.login(user, password)
		status_select = self.imap.select()
		return (status_login, status_select)

	def kill(self):
		"""Close mailbox and log out from server.

		:return: `tuple` with status messages
		"""
		status_close = self.imap.close()
		status_logout = self.imap.logout()
		return (status_close, status_logout)

class Imapy_SSL(Imapy):
	def __init__(self, host, *args, **kwargs):
		"""Use ssl to connect to imap server.

		for ``*args`` and ``**kwargs`` see documentation of imaplib.IMAP4_SSL
		"""
		self.imap = IMAP4_SSL(host, *args, **kwargs)

