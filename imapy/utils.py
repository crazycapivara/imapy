"""
	imapy.utils (imapynho.utils)
	~~~~~~~~~~~
	This module contains mostly functions to extract all kinds of
	information from message parts and decode values, if needed.
	Moreover, some function so save or rather backup emails to disk
	and to load settings, e. g. for several accounts, from json-config-file.

	:copyright: (c) 2015 by Stefan Kuethe
	:licence: GPLv3 see LICENSE.md for more details
"""

__author__ = "Stefan Kuethe"
__version__ = "0.2.0"

from email.header import decode_header as decode_email_header
import email.utils
import json, random
from datetime import datetime
from StringIO import StringIO

DEFAULT_CHARSET = "utf-8"

def load_config(filename):
	"""Read settings or configuration (e. g. account data)
	   from json-file and return `dict`.
	"""
	with file(filename) as io_stream:
		data = io_stream.read()
	return json.loads(data)

def create_query(criteria, *args):
	"""Create and return query string from several
	   search criteria as defined in `imapy.criterion` module.
	"""
	query_string = " ".join(criteria)
	return query_string %(args)

# ----------------------------testing version------------------------------------------
def decode_header_field_test(field):
	"""Decode and return given (header) `field`."""
	#print "before", field
	parts = decode_email_header(field)
	#print "parts", parts
	for idx, (text, charset) in enumerate(parts):
		# check this part, in case there is a charset problem!
		if charset:
			#print charset
			parts[idx] = text.decode(charset, errors="replace")
		else:
			#print "I am here"
			parts[idx] = text.decode(DEFAULT_CHARSET, errors="replace")
	#print "parts", parts
	data = "".join(parts)
	if type(data) != unicode:
		#print type(data)
		data = unicode(data, errors="ignore")
	#print "data now:", repr(data)
	return data
	#return unicode(" ".join(parts), errors="replace")
#-----------------------------------------------------------------------------------------
def decode_header_field(field):
	"""Decode and return given (header) `field`."""
	parts = decode_email_header(field)
	for idx, (text, charset) in enumerate(parts):
		# check this part, in case an error is raised
		parts[idx] = text.decode(charset or DEFAULT_CHARSET, errors="replace")
	return "".join(parts)

def parse_subject(msg):
	"""Decode and return subject of header."""
	return decode_header_field(msg["subject"])

def parse_date(msg, date_fmt=None):
	"""Return date as datetime object or as
	   formated string as defined by `date_fmt`.

	:param date_fmt: (str, optional) like ``'%Y-%m-%d %H:%S'``
	:return: datetime object or string in case date_fmt is given  
	"""
	#print "date before parsing", msg["date"]
	date_tuple = email.utils.parsedate(msg["date"])
	date = datetime(*date_tuple[:7])
	if date_fmt:
		date = date.strftime(date_fmt)
	return date 

def parse_address_field(msg, field="from"):
	"""Fetch and return all addresses for given `field`."""
	result = msg.get_all(field)
	if not result:
		#return {field: None}
		return False
	addresses = email.utils.getaddresses(result)
	# Decode names. 
	addresses = [(decode_header_field(address[0]), address[1]) for address in addresses]
	#return {field: addresses}
	return addresses

def parse_header(msg, date_fmt=None):
	"""Return `dict` containing parsed and decoded
	   values for subject, from, to and date.
	"""
	subject = parse_subject(msg)
	date = parse_date(msg, date_fmt)
	from_ = parse_address_field(msg, "from")[0]
	to = parse_address_field(msg, "to")
	return dict(zip(("subject", "date", "from", "to"), (subject, date, from_, to)))

# not needed anymore, done in Imapy directly!
# OBSOLETE!
def split_mbox_names(mbox_names):
	"""Returns list of (raw, special utf7 encoded) mailbox names."""
	mbox_names_ = [mbox.split()[-1].strip('"') for mbox in mboxes]
	return mbox_names

# OBSOLETE, also included in Imapy directly!
def decode_mbox_names(mbox_names):
	pass

def save_file(content, folder="", filename=None):
	with file(folder+filename, "w") as f:
		f.write(content)
	return True

def get_filename(msg):
	filename = "_out_%s.txt" %(parse_date(msg, "%Y%m%d_%H-%M-%S"))
	return filename

#: should use uid in filename if none is given (see :func get_filename:),
#: therefor, uid needs to be returned from Imapy.result as well!
def save_raw_msg(msg, folder="", filename=None):
	return save_file(msg.as_string(), folder, filename or get_filename(msg))

def save_parsed_msg(msg, folder="", filename=None):
	pass

def decode_content(part):
	content = part.get_payload(decode=True)
	charset = part.get_content_charset()
	if charset:
		return content.decode(charset)
	return content

# maybe it would be nice to strip all html tags!
# check whether code can be cleaned somehow!
def parse_content(msg, join=True, delimiter=""):
	"""Return content parts excluding attachments"""
	#print "main content type:", msg.get_content_type()
	plain = []
	html = []
	if msg.is_multipart():
		for part in msg.walk():
			# switch could be used here!
			content_type = part.get_content_type()
			if content_type == "text/plain":
				#plain.append(part.get_payload(decode=True))
				plain.append(decode_content(part))
			if content_type == "text/html":
				#html.append(part.get_payload(decode=True))
				html.append(decode_content(part))
	else:
		# Attention: inline images!?
		if msg.get_content_type() == "text/plain":
			plain.append(decode_content(msg))
		else:
			html.append(decode_content(msg))
	if join:
		plain = delimiter.join(plain)
		html = delimiter.join(html)
	return dict(zip(["plain", "html"], [plain, html]))

def get_attachments(msg):
	attachments = []
	print msg.is_multipart()
	for part in msg.walk():
		print part.get_content_type(), part.get("Content-Disposition")
		if part.get_filename():
			print "attachment found"
			#print part.get_filename(), part.get_content_type()
			#attachement = (part.get_filename(), part.get_payload(decode=True), part.get_content_type())
			#print attachement[0], len(attachement[1])
			data = part.get_payload(decode=True)
			attachment = {
				"filename": part.get_filename(),
				"data": StringIO(data),
				"size": len(data)
			}
			attachments.append(attachment)
	return attachments

#-------REGEX stuff for parsing "BODYSTRUCTURE" to get attachment names! ----
search = r'\("filename" (".*?")\)'
# ------

def __to_be_continued__():
	return """
	functions for parsing body, attachements, decoding utf7 mailbox names etc. will be added here!
	"""
