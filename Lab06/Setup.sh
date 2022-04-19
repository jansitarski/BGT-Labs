mkdir database
cd ./database
sudo apt-get -y install postgresql pv
sudo -u postgres createuser musicbrainz
sudo -u postgres createdb music

gsutil -m cp gs://pjwstk-bigdata/db.tar .
sudo -u postgres pg_restore -c -d music -v db.tar -w
touch done.txt
