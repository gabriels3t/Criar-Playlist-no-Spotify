import spotipy
from spotipy.oauth2 import SpotifyOAuth
import credencial
# Autenticação com o Spotify
# Permissão para modificar playlists privadas
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=credencial.client_id,
    client_secret=credencial.client_secret,
    redirect_uri='http://localhost:3000/',
    scope='playlist-modify-private playlist-modify-public user-library-read'

))

playlist_id = credencial.playlist_id

offset = 0
limit = 50  # Número de músicas a serem recuperadas por solicitação
liked_tracks = []
while True:
    response = sp.current_user_saved_tracks(limit=limit, offset=offset)
    tracks = response['items']
    liked_tracks.extend(tracks)
    if len(tracks) < limit:
        break
    offset += limit

# Adicionando as musicas na playlist
track_uris = [track['track']['uri'] for track in liked_tracks]

# Dividir a lista de músicas em lotes menores
batch_size = 50  # Número máximo de músicas por lote
batches = [track_uris[i:i + batch_size] for i in range(0, len(track_uris), batch_size)]

# Adicionar cada lote à playlist
for batch in batches:
    sp.playlist_add_items(playlist_id, batch)

print("Músicas adicionadas à playlist com sucesso!")