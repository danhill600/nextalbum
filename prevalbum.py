#!/usr/bin/env python3

#a script for going to the beginning of the previous album on
#the mpd playlist -dmh 20190526

import mpd

def connect_client():
    """Connect to MPD Client"""
    client = mpd.MPDClient()
    client.connect("localhost", 6600)
    return client

def get_pl_tuples(client):
    pl_tuples = []
    for song in client.playlistinfo():
        mytuple = (song["id"], song["album"])
        pl_tuples.append(mytuple)
    return pl_tuples


# try index and then delete before that point
def get_sliced_list(cur_id, cur_album, pl_tuples):
    my_index=pl_tuples.index((cur_id,cur_album))
    del pl_tuples[my_index:]
    sliced_list = pl_tuples
    return sliced_list

def get_prev_album(sliced_list):
    for song in reversed(sliced_list):
        if cur_album != song[1]:
            prev_album = song[1]
            return prev_album

client  = connect_client()
#get the id and album of currently playing song
cur_id = client.currentsong()["id"]
cur_album = client.currentsong()["album"]

pl_tuples = get_pl_tuples(client)
sliced_list = get_sliced_list(cur_id, cur_album, pl_tuples)
prev_album = get_prev_album(sliced_list)

for song in client.playlistinfo():
    if song["album"] == prev_album:
        client.playid(song["id"])
        break
