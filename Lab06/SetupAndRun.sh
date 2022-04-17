mkdir database
cd ./database
touch started.txt
sudo apt-get -y install postgresql pv
sudo -u postgres createuser musicbrainz
sudo -u postgres createdb music

gsutil -m cp gs://pjwstk-bigdata/db.tar .
sudo -u postgres pg_restore -c -d music -v db.tar -w
touch done.txt

for i in {1..6}; do
  sudo sh -c 'sudo -u postgres psql -d music -c "\timing" -a -f "./sql.sql"'
done
