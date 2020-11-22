# Team TARDIS - DigitalDefence Hack project

This repository contains the building blocks of the proof-of-concept file upload watcher.

It utilises incron (inotify) to watch for file upload events and to reach out to
IBM's X-Force Exchange API to retrieve threat intelligence based on the uploader's
IP address and the uploaded file's SHA256 hash.
