for i in {1..6}; do
  sudo -u postgres psql -d music -c "\timing" -c 'SELECT tr.name  AS "Track Name",re.name  AS "Album Name",art.name AS "Artist Name",ar1.name AS "Artist Country",ar2.name AS "Release Country"
  FROM (SELECT track.id, track.medium, track.name, track.artist_credit FROM musicbrainz.track) tr
  JOIN (SELECT medium.id, medium.release FROM musicbrainz.medium) med ON tr.medium = med.id
  JOIN (SELECT release.id, release.name FROM musicbrainz.release) re ON med.release = re.id
    JOIN (SELECT artist.id, artist.name, artist.area FROM musicbrainz.artist) art ON tr.artist_credit = art.id
  JOIN (SELECT area.id, area.name FROM musicbrainz.area) ar1 ON art.area = ar1.id
  JOIN (SELECT release_country.release, release_country.country FROM musicbrainz.release_country) rel_c ON re.id = rel_c.release
  JOIN (SELECT area.id, area.name FROM musicbrainz.area) ar2 ON rel_c.country = ar2.id limit 1000000;' | tail -1 >> result.txt
done
