from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import cred
import pandas as pd

#_________________________________________________________________________________________________ STEP 1
#Get users Top artists in an array

scope = "user-top-read"
sp_1 = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret=cred.client_secret,
                                               redirect_uri=cred.redirect_url, scope=scope))
#results = sp.current_user_recently_played()
results = sp_1.current_user_top_artists(limit=3)

#User artist array
user_artists = []

#print(results)
for idx, item in enumerate(results['items']):
    genres = item['genres']
    artist = item['name']
    print(artist)
    user_artists.append(artist)
    print(genres)
    length = len(genres)

print(user_artists)

#____________________________________________________________________Step 2


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cred.client_id, client_secret=cred.client_secret,
                                                           ))


my_url = 'https://aesthetics.fandom.com/wiki/List_of_Aesthetics'

#Opening up connection, grabbing the main page
uClient = uReq(my_url)
main_page = uClient.read()
uClient.close #Closes the page

#Parse the html, cause its too massive at the moment
page_soup = soup(main_page, "html.parser") #Does html parsing

#Traversing the page, Grabs the alphabet links
category_list = page_soup.findAll("table", {"style":"background-color:transparent; color:inherit; width:100%;"})
list_Y_Z = page_soup.findAll("ul")
#Needed to add the Y and Z categories
category_list.append(list_Y_Z[112])
category_list.append(list_Y_Z[113])
del category_list[0]
print(len(category_list))

link_array = []
title_array = []
#playlist = [] #empty array to put the playlists into

for item in category_list:
    for title in item.find_all("a"):
        if 'title' in title.attrs:
            a = title.attrs['title']
            title_array.append(a)
            print(a)
            whitespace_pos = 0
            #Making the links work for titles that have a space inbetween
            for chcr in a:
                if (chcr.isspace()) == True:
                    title_list = list(a) #Need to make the title from a str to a list
                    title_list[whitespace_pos] = "_" #replace the white space with a _
                    a = "".join(title_list)
                whitespace_pos += 1
            link = 'https://aesthetics.fandom.com/wiki/{0}'.format(a) #Makes each aestethic a web-link
            print(link)
            link_array.append(link)
            print("")
del link_array[356] #Deleting Shae mae te
del link_array[428] #Deleting Virgo's tears

i = 0
while i < len(link_array):
    a_link = link_array[i] #aesthetic link
    #__________________________________________________________________________________________________________
    #Opening up connection to the specifc aesthetic page
    uClient_aesthetic = uReq(a_link)
    aesthetic_page = uClient_aesthetic.read()
    uClient_aesthetic.close()
    #Parse the html, cause its too massive at the moment
    aesthetic_page_soup = soup(aesthetic_page, "html.parser") #Does html parsing
    playlist = []
    print(a_link)
    print(" ")
    i += 1
    artist_array = user_artists

    #Find the first playlist link to scrape for artists
    def spotify(href):
        return href and re.compile("https://open.spotify.com/playlist").search(href)

    #playlist = aesthetic_page_soup.find_all(href=spotify)
    for a_link in aesthetic_page_soup.findAll(href=spotify):
        playlist.append((a_link.get('href')))

    print(len(playlist))
    if len(playlist) > 0:
        if len(playlist) == 1:
            playlist = playlist[0]
        else:
            playlist = playlist[1]

        #Need to just get the unique identifier for the playlist. From pos 34:56
        playlist_identifier = playlist[34:56]
        def call_playlist(creator,playlist_id):
            break_out_flag = False
            playlist_features_list = ["artist"]
            playlist_df = pd.DataFrame(columns = playlist_features_list)
            playlist_features = [] #Creating empty dict
            playlist_list = sp.user_playlist_tracks(creator, playlist_id)["items"]
            for item in playlist_list:
                if break_out_flag == True:
                    b = 1
                    final_aesthtic = title_array[i-1]
                    message = 'Your Aesthetic is {0}'.format(final_aesthtic)
                    final_aesthtic_link = link_array[i-1]
                    print(final_aesthtic_link)
                    print(message)
                    quit()
                else:
                    if item['track'] is None:
                        continue
                    else:
                        # Create empty dict

                        # Get metadata
                        playlist_features = item["track"]["artists"][0]["name"]
                        print(playlist_features)
                        j = 0
                        while j < len(artist_array):
                            if playlist_features == artist_array[j]:
                                break_out_flag = True
                                b = 1
                                break
                            else:
                                j += 1

            return playlist_df
        artists_in_playlist = call_playlist("spotify",playlist_identifier)

