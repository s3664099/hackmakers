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
