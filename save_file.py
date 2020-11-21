#!/usr/bin/python3

import cgi, os
import cgitb; cgitb.enable(format="text")

form = cgi.FieldStorage()

#Get filename here
filelist = form['filename']
message = ""

for fileitem in filelist:
	if fileitem.filename:

		#strip leading path from file name to avoid
		#directory traversal attacks

		fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
		open('/tmp/'+fn, 'wb').write(fileitem.file.read())
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