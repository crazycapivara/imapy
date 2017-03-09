from email.utils import getaddresses
from .. utils import decode_header_field

def parse_addresses(msg, field="from"):
	result = msg.get_all(field)
	if not result:
		#return {field: ("", "")}
		return False
	addresses = getaddresses(result)
	# Decode names. 
	addresses = [(decode_header_field(address[0]), address[1]) for address in addresses]
	#print parsed_addresses
	if len(addresses) > 1:
		return {field: addresses[0], "%s_more" % field: addresses[1:]}
	return {field: addresses[0]}

# what is the best name for this ask?
parse_address_field = parse_addresses

#
# check problems, if no charset is given, how to decode!?
# will utf-8 always work?
#
def decode_header_field(field):
	"""Decode and return given (header) `field`."""
	print "before", field
	parts = decode_email_header(field)
	print "parts", parts
	for idx, (text, charset) in enumerate(parts):
		# check this part, in case there is a charset problem!
		if charset:
			#print charset
			parts[idx] = text.decode(charset, errors="replace")
		else:
			print "I am here"
			parts[idx] = text
	#print "parts", parts
	data = "".join(parts)
	if type(data) != unicode:
		#print type(data)
		data = unicode(data, errors="ignore")
	#print "data now:", repr(data)
	return data
	#return unicode(" ".join(parts), errors="replace")

