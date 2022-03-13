import pandas as pd
import matplotlib.pyplot as plt
import csv

out = pd.read_csv("./charts.csv")

# Zad1.1
print("Most popular: ", out['title'].value_counts().head(1))
print("Most popular: ", out['title'].value_counts().tail(1))

# Zad1.2
artist = "Daft Punk"
lowest_song = out.loc[out["artist"] == artist].sort_values(by=['rank']).max()
songs = out.loc[out["title"] == lowest_song["title"]]
plt.scatter(pd.to_datetime(songs["date"]),songs["rank"])
plt.show()

# Zad2.1
count_songs = dict()
with open('./charts.csv', mode='r', encoding="utf8") as file:
    csvFile = csv.DictReader(file)
    for lines in csvFile:
        if lines["title"] in count_songs:
            count_songs[lines["title"]] += 1
        else:
            count_songs[lines["title"]] = 1
    count_songs2 = dict(sorted(count_songs.items(), key=lambda x: x[1]))
for x in list(count_songs2)[0:3]:
    print("song: {}, {} ".format(x, count_songs2[x]))
for x in list(reversed(count_songs2))[0:3]:
    print("song: {}, {} ".format(x, count_songs2[x]))

# Zad2.1
count_songs = dict()
rank = 100000
lowest_ranking = ""
artist = "Daft Punk"
with open('./charts.csv', mode='r', encoding="utf8") as file:
    csvFile = csv.DictReader(file)
    for lines in csvFile:
        if int(lines["rank"]) < rank:
            lowest_ranking = lines["title"]
            rank = int(lines["rank"])
    print("song: {}, {}".format(lowest_ranking, rank))

# Zad2.2
with open('./charts.csv', mode='r', encoding="utf8") as file:
    csvFile = csv.DictReader(file)
    for lines in csvFile:
        if lines["title"] == lowest_ranking:
            print("{}, {}, {}".format(lines["title"], lines["rank"], lines["date"]))
