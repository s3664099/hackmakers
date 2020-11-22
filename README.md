# Team TARDIS - DigitalDefence Hack project

This repository contains the building blocks of the proof-of-concept (POC) file upload watcher.

It utilises incron (inotify) to watch for file upload events and to reach out to
IBM's X-Force Exchange API to retrieve threat intelligence based on the uploader's
IP address and the uploaded file's SHA256 hash.

If the file is considered a threat, is is removed within milliseconds after the upload completes.

## Prerequisites:

The POC was tested using an instance in the Oracle Cloud Infrastructure. The watcher
folder contains a startup script fragment which preinstalls and preconfigures the
required services. The application's files were deployed manually, and the POC's server
side scripts also need to be started manually.

It also requires access to IBM X-Force Exchange using an API key - password pair.

## Components:

### Uploader

The `uploader` folder contains the basic HTML UI for the POC's file upload.

### Upload processor

The upload processor is a thin backend script which accepts the file upload request,
retrieves the request's source IP, and saves the file to a temporary folder.

### Watcher

The watcher is a self-contained thin HTTP server app which listens to requests
on port 8000. It is called via `cURL` commands by `incron`.

`incron` is configured to listen to `IN_CLOSE_WRITE` events in the temporary folder,
and when they occur, it asynchronously validates the source IP and the file content hash
against IBM X-Force Exchange's database.

# Future Expansion

One area in which this product can be expanded is to provide data back into X-Force Exchange, where if our product detects malicious IP addresses or files that are not present on the database, we can pass the information along so that the community is better advised.

A second expansion would include monitoring TOR exit points and known IP addresses associated with commercial VPN providers. It is anticipated that these IP addresses would more likely than not be used by attackers, and in this instance any uploads coming from these addresses can be blocked.

Another expansion could relate to file type monitoring. This way unauthorised files can be prevented from being injected into a pipeline. For instance, if a pipeline only allows pdf files, then any files that aren't in a pdf format can be blocked.

Other way round the traffic can be blocked if something is being advertised and making it to the DMZ.
