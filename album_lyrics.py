import os
import csv
import json
import pandas as pd
import lyricsgenius as lg

genius_access_token = os.environ['GENIUS_ACCESS_TOKEN']
genius = lg.Genius(genius_access_token,remove_section_headers=True)

print('Enter album name: ')
album_name = input()
print('Enter artist: ')
artist = input()

albun_name_file = album_name.replace(' ','')
album = genius.search_album(album_name, 'The Smiths')

album.save_lyrics()

songs_data = json.load(open('Lyrics_' + albun_name_file + ".json"))


# Lyrics in Dataframe
songs = songs_data.get('tracks')
df = pd.DataFrame()
for item in songs:
    df = df.append({
        'Title': item['song']['title'],
        'Lyrics': item['song']['lyrics']
    }, ignore_index=True)

# Split lyrics by verse
lyrics_df = pd.DataFrame(df.Lyrics.str.split('\n').tolist(), index=df.Title).stack()
lyrics_df = lyrics_df.reset_index([0, 'Title'])
lyrics_df.columns = ['Title', 'Lyrics']

# Drop empty rows (does not detect nan values)
lyrics_df['length'] = lyrics_df.Lyrics.str.len()
lyrics_df = lyrics_df[lyrics_df.length > 0]
lyrics_df = lyrics_df.drop(columns=['length'])

# Remove "EmbedShare URLCopyEmbedCopy" tag
pattern = r'[0-9]+EmbedShare URLCopyEmbedCopy$'
lyrics_df = lyrics_df.replace(pattern,'',regex=True)

lyrics_df = lyrics_df.drop_duplicates()
lyrics_df['Lyrics'] = lyrics_df['Lyrics'].str.lower()

# Export to csv
lyrics_df.to_csv('/Users/paolagomez/MITCloud/lyrics' + albun_name_file + '.csv')

