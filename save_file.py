#!/usr/bin/python3

import cgi, os
import cgitb; cgitb.enable()

form = cgi.FieldStorage()

#Get filename here

fileitem = form['filename']

print(fileitem)

if fileitem.filename:

	#strip leading path from file name to avoid
	#directory traversal attacks

	fn = os.path.basename(fileitem.filename)
	open('/tmp/'+fn, 'wb').write(fileitem.file.read())
	message = 'The file "'+fn+'" was uploaded successfully'
else:
	message = 'No file was uploaded'

print ("Content-Type: text/html")
print ("<html>")
print ("<body>")
print ("<p>"+message+"</p>")
print ("</body>")
print ("</html>")