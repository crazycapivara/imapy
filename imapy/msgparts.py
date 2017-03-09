HEADER = '(BODY.PEEK[HEADER.FIELDS (%s)])'

def all():
	return "(BODY.PEEK[])"

def header(fields="SUBJECT FROM DATE TO"):
	"""
	:param fields: e. g. 'SUBJECT FROM DATE'
	"""
	return HEADER % fields

def RFC822():
	return "(RFC822)"
