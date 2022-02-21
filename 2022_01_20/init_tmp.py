import os
from datetime import datetime

def getName():
	date = datetime.now()
	return date.strftime('%Y_%m_%d__%H_%M_%S')

if not os.access('tmp', os.F_OK):
	os.mkdir('tmp')

open('tmp/text.txt', 'w').close()

open('tmp/' + getName() + '.txt', 'w')

