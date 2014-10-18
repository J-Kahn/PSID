import re
import numpy as np

sas_to_csv(sas_name, ascii_name, csv_name)
	x         = open(sas_name,"r")
	dat       = x.read()
	dat_split = dat.split('\n')

	re_var    = '^\s*(?P<variable>\S+)\s+'
	re_label  = '[(LABEL)(label)]\s*=\s*"(?P<label>[^"]+)"'
	re_format = '[(FORMAT)(format)]\s*=\s*(?P<format>\S+)\s'
	re_length = '\s*(?P<length1>\d*)\s+-\s+(?P<length2>\d*)\s*'

	meta = []

	for dstr in dat_split:
		res_var    = re.search(re_var, dstr)
		res_label  = re.search(re_label, dstr)
		res_format = re.search(re_format, dstr)

		if not (res_var is None or res_label is None or res_format is None):

			counts = re.search(res_var.group('variable')+re_length,dat)
			l1     = int(counts.group('length1'))
			l2     = int(counts.group('length2'))

			meta        = meta +[ {	'variable'    : res_var.group('variable'),
								'label'    : res_label.group('label'),
								'format' : res_format.group('format'),
								'l1' : l1,
								'l2' : l2,
								'l3' : l2 - l1 + 1
							}]

	names   = [z['label'] for z in meta]
	formats = [z['format'] for z in meta]
	lengths = [z['l3'] for z in meta]

	data = np.genfromtxt(ascii_name, names=names, delimiter=lengths)
	np.savetxt(csv_name, data, delimiter=',', header=','.join(data.dtype.names))