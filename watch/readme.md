# Incron watcher

This folder contains the incron-based file upload watcher config, and the mini server
app which communicates with the IBM XFE API

## OCI instance startup script

`yum -y update`
`yum -y install inotify-tools incron nginx screen python3`
`pip3 install requests`
`mkdir /tmp/upload`
`echo "root" > /etc/incron.allow`
`echo -e "/tmp/upload\tIN_CLOSE_WRITE\tcurl -s -X POST -d \"file=\$@/\$#\" http://localhost:8000" > /etc/incron.d/upload`
`systemctl enable incrond.service`
`systemctl start incrond.service`
`firewall-cmd --zone=public --add-port=80/tcp --permanent`
`firewall-cmd --reload`
