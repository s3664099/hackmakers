#!/usr/bin/python3

import cgi
import os
import cgitb

cgitb.enable(format="text")

form = cgi.FieldStorage()
# Get filename here
file_item = form['filename']

client_ip = os.getenv("HTTP_X_FORWARDED_FOR")

if file_item.filename:

	# strip leading path from file name to avoid
	# directory traversal attacks

	fn = client_ip + "_" + os.path.basename(file_item.filename.replace("\\", "/"))
	open('/tmp/upload/' + fn, 'wb').write(file_item.file.read())
	print('Status: 301 Redirect')
	print('Location: /uploader/success.html')
else:
	print('Status: 301 Redirect')
	print('Location: /uploader/failure.html')

print("Content-Type: text/html\n\n")
print("Moved permanently")
