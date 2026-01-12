# %%writefile app.py
import io
import streamlit as st

st.title("Music Playlist")

# --- Song Class ---
class Song:
    
    def __init__(self, title, artist, audio_file=None):
        self.title = title
        self.artist = artist
        self.audio_file = audio_file
        self.next_song = None


    def __str__(self):
        return f"{self.title} by {self.artist}"

# --- MusicPlaylist Class ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_file=None):
        new_song = Song(title, artist, audio_file)

        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1
        st.success(f"Added: {new_song}")

    def display_playlist(self):
        if self.head is None:
            return []

        playlist_songs = []
        current = self.head
        count = 1
        while current:
            playlist_songs.append(f"{count}. {current.title} by {current.artist}")
            current = current.next_song
            count += 1
        return playlist_songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
        if self.current_song.audio_file:
            st.audio(self.current_song.audio_file)
        else:
            st.warning("Playlist is empty.")


    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        elif self.current_song and not self.current_song.next_song:
            st.warning("End of playlist. No next song.")
        else:
            st.warning("Playlist is empty.")

    def prev_song(self):
        if self.head is None or self.current_song is None:
            st.warning("Playlist is empty or no song is selected.")
            return
        if self.current_song == self.head:
            st.warning("Already at the beginning of the playlist.")
            return

        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def get_length(self):
        return self.length
    def reset_playlist(self):
        self.head = None
        self.current_song = None
        self.length = 0
        

    def delete_song(self, title):
        if self.head is None:
            st.error(f"Cannot delete '{title}'. Playlist is empty.")
            return

        # If the song to be deleted is the head
        if self.head.title == title:
            if self.current_song == self.head:
                self.current_song = self.head.next_song
            self.head = self.head.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
            if self.length == 0:
                self.current_song = None
            return

        current = self.head
        prev = None
        while current and current.title != title:
            prev = current
            current = current.next_song

        if current:
            if self.current_song == current:
                if current.next_song:
                    self.current_song = current.next_song
                elif prev:
                    self.current_song = prev
                else:
                    self.current_song = None

            prev.next_song = current.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
        else:
            st.error(f"Song '{title}' not found in the playlist.")

# --- Streamlit App Layout ---
st.title("🎶 Music Playlist App")

# Initialize playlist in session state
if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# Sidebar for adding songs
st.sidebar.header("Add New Song")
new_title = st.sidebar.text_input("Title")
new_artist = st.sidebar.text_input("Artist")
if st.sidebar.button("Add Song to Playlist"):
    if new_title and new_artist:
        st.session_state.playlist.add_song(new_title, new_artist)
    else:
        st.sidebar.warning("Please enter both title and artist.")

st.sidebar.markdown("--- 🎶")
st.sidebar.header("Upload Audio File (Optional)")
uploaded_file = st.sidebar.file_uploader(
    "Upload audio file",
    type=["mp3", "wav"]
)
if uploaded_file is not None:
    # Read the file line by line
    # Sidebar for uploading song list file
    st.sidebar.markdown("--- 🎶")
    st.sidebar.header("Upload Song List (CSV-like)")

uploaded_file = st.sidebar.file_uploader(
    "Upload file (Title,Artist)",
    type=["txt", "csv"]
)

# ใช้ flag ป้องกันการเพิ่มซ้ำ
if 'uploaded_once' not in st.session_state:
    st.session_state.uploaded_once = False

if uploaded_file is not None and not st.session_state.uploaded_once:
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))

    for line in stringio.readlines():
        parts = line.strip().split(',')
        if len(parts) == 2:
            title, artist = parts
            st.session_state.playlist.add_song(title.strip(), artist.strip())
        elif line.strip():
            st.sidebar.warning(
                f"Skipping malformed line: {line.strip()}"
            )

    st.session_state.uploaded_once = True

st.sidebar.markdown("--- 🎶")
if st.sidebar.button("🔄 Reset Playlist"):
    st.session_state.playlist.reset_playlist()
    st.session_state.uploaded_once = False
    st.sidebar.success("Playlist has been reset.")

# Main content for playlist display and controls
st.header("Your Current Playlist")
playlist_content = st.session_state.playlist.display_playlist()
if playlist_content:
    for song_str in playlist_content:
        st.write(song_str)
else:
    st.write("Playlist is empty. Add some songs from the sidebar!")

st.markdown("--- 🎶")
st.header("Playback Controls")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏪ Previous"):
        st.session_state.playlist.prev_song()
        st.session_state.playlist.play_current_song()

with col2:
    if st.button("▶️ Play Current"):
        st.session_state.playlist.play_current_song()

with col3:
    if st.button("⏩ Next"):
        st.session_state.playlist.next_song()
        st.session_state.playlist.play_current_song()

st.markdown("--- 🎶")
st.write(f"Total songs in playlist: {st.session_state.playlist.get_length()} song(s)")
