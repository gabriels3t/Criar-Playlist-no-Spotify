import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credencial


# Autenticação com o Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=credencial.client_id,
    client_secret=credencial.client_secret,
    redirect_uri='http://localhost:3000/',
    scope='playlist-modify-private playlist-modify-public user-library-read'

))

# ID da playlist original e nome da nova playlist
playlist_id = credencial.playlist_id
new_playlist_name = 'Tudo BrBr'
# Função para verificar se a música é brasileira
def is_brazilian(track):
    portuguese_chars = set('áàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ')
  
    title = track['name'].lower()
    album = track['album']['name'].lower()
    for artist in track['artists']:
        artist_name = artist['name'].lower()
        if artist_name=="terra celta" or artist_name=="yung lixo" or artist_name=="angra" or artist_name=="planet hemp" or artist_name=="cpm 22"\
            or artist_name=="mamonas assassinas"or artist_name=="gabriel o pensador"or artist_name=="os paralamas do sucesso"or artist_name=="charlie brown jr"\
                or artist_name=="racionais mc's"or artist_name=="skinner" :
            return True
        if any(char in portuguese_chars for char in title) \
            or any(char in portuguese_chars for char in album) \
            or any(char in portuguese_chars for char in artist_name):
            return True
    return False

# Cria uma nova playlist
user_id = sp.me()['id']
new_playlist = sp.user_playlist_create(user=user_id, name=new_playlist_name)

# Obtém as músicas da playlist original
playlist = sp.playlist(playlist_id)
tracks = playlist['tracks']

# Adiciona as músicas brasileiras na nova playlist
while tracks:
    for item in tracks['items']:
        track = item['track']
        if is_brazilian(track):
            sp.playlist_add_items(new_playlist['id'], [track['id']])
    if tracks['next']:
        tracks = sp.next(tracks)
    else:
        tracks = None

print("Playlist de músicas brasileiras criada com sucesso!")