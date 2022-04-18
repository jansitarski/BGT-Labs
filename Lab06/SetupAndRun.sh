mkdir database
cd ./database
sudo apt-get -y install postgresql pv
sudo -u postgres createuser musicbrainz
sudo -u postgres createdb music

gsutil -m cp gs://pjwstk-bigdata/db.tar .
sudo -u postgres pg_restore -c -d music -v db.tar -w

sudo su

for i in {1..6}; do
  sudo -u postgres psql -d music -c "\timing" -c 'SELECT tr.name  AS "Track Name",re.name  AS "Album Name",art.name AS "Artist Name",ar1.name AS "Artist Country",ar2.name AS "Release Country"FROM (SELECT track.id, track.name FROM musicbrainz.track) tr JOIN (SELECT release.id, release.name FROM musicbrainz.release) re ON tr.id = re.id JOIN (SELECT artist.id, artist.name FROM musicbrainz.artist) art ON tr.id = art.id JOIN (SELECT area.id, area.name FROM musicbrainz.area) ar1 ON art.id = ar1.id JOIN (SELECT release_country.release, release_country.country FROM musicbrainz.release_country) rel_c ON re.id = rel_c.release JOIN (SELECT area.id, area.name FROM musicbrainz.area) ar2 ON rel_c.country = ar2.id limit 1000000000;' | tail -1 >> result.txt
done
