#!/usr/bin/python3

import cgi
import os
import cgitb

cgitb.enable(format="text")

form = cgi.FieldStorage()

# Get filename here
file_list = form['filename']
message = ""

for file_item in file_list:
	if file_item.filename:

		# strip leading path from file name to avoid
		# directory traversal attacks

		fn = os.path.basename(file_item.filename.replace("\\", "/"))
		open('/tmp/upload/' + fn, 'wb').write(file_item.file.read())
		message += '<p>The file "'+fn+'" was uploaded successfully</p>'
	else:
		message = '<p>No file was uploaded</p>'

print ("Content-Type: text/html")
print ("")
print ("<html>")
print ("<body>")
print (message)
print ("</body>")
print ("</html>")