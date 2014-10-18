import re
import numpy as np

def sas_to_csv(sas_name, ascii_name, csv_name):

	# Open sas file
	x         = open(sas_name,"r")
	dat       = x.read()
	dat_split = dat.split('\n')

	re_var    = '^\s*(?P<variable>\S+)\s+' # RE for variable designation
	re_label  = '[(LABEL)(label)]\s*=\s*"(?P<label>[^"]+)"' # RE for variable label
	re_format = '[(FORMAT)(format)]\s*=\s*(?P<format>\S+)\s' # RE for variable format
	re_length = '\s*(?P<length1>\d*)\s*-\s*(?P<length2>\d*)\s*' # RE for variable position

	meta = []

	for dstr in dat_split:
		res_var    = re.search(re_var, dstr) # Find variable name in line
		res_label  = re.search(re_label, dstr) # Find variable label
		res_format = re.search(re_format, dstr) # Find variable format

		if not (res_var is None or res_label is None or res_format is None):

			# Now that we have a verified variable name...
			counts = re.search(res_var.group('variable')+re_length,dat) # Find position RE
			l1     = int(counts.group('length1')) # Grab out first position
			l2     = int(counts.group('length2')) # Grab out second position

			# Add to meta data
			meta        = meta +[ {	'variable'    : res_var.group('variable'),
								'label'    : res_label.group('label'),
								'format' : res_format.group('format'),
								'l1' : l1,
								'l2' : l2,
								'l3' : l2 - l1 + 1
							}]

	# Get relevant descriptions
	names   = [z['label'] for z in meta]
	formats = [z['format'] for z in meta]
	lengths = [z['l3'] for z in meta]
	del meta

	# Use numpy to read fixed width file and write as .csv
	data = np.genfromtxt(ascii_name, names=names, delimiter=lengths)
	np.savetxt(csv_name, data, delimiter=',', header=','.join(data.dtype.names))
	del data