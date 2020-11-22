yum -y update
yum -y install incron inotify-tools nginx python3 screen
pip3 install requests pipenv
mkdir /tmp/upload
mkdir /tmp/final
echo "root" > /etc/incron.allow
echo -e "/tmp/upload\tIN_CLOSE_WRITE\tcurl -s -X POST -d \"file=\$#&path=\$@/\" http://localhost:8000" > /etc/incron.d/upload
systemctl enable incrond.service
systemctl start incrond.service
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload
