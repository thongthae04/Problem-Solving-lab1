# %%writefile app.py
import streamlit as st

st.title("🎶 Music Playlist App")

# --- Song Class ---
class Song:
    def __init__(self, title, artist, audio_file):
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

    def add_song(self, title, artist, audio_file):
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
        songs = []
        current = self.head
        i = 1
        while current:
            songs.append(f"{i}. {current.title} by {current.artist}")
            current = current.next_song
            i += 1
        return songs

    def play_current_song(self):
        if not self.current_song:
            st.warning("Playlist is empty.")
            return

        st.info(f"Now playing: {self.current_song}")
        st.audio(self.current_song.audio_file)

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        else:
            st.warning("End of playlist.")

    def prev_song(self):
        if self.current_song == self.head:
            st.warning("Already at first song.")
            return

        current = self.head
        while current and current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def get_length(self):
        return self.length

# --- Session State ---
if "playlist" not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# --- Sidebar: Add Song ---
st.sidebar.header("➕ Add New Song")

title = st.sidebar.text_input("Song Title")
artist = st.sidebar.text_input("Artist")
audio_file = st.sidebar.file_uploader(
    "Upload Audio File",
    type=["mp3", "wav"]
)

if st.sidebar.button("Add Song"):
    if title and artist and audio_file:
        st.session_state.playlist.add_song(title, artist, audio_file)
    else:
        st.sidebar.warning("Please provide title, artist, and audio file.")

# --- Main Playlist Display ---
st.header("📃 Playlist")
playlist = st.session_state.playlist.display_playlist()

if playlist:
    for song in playlist:
        st.write(song)
else:
    st.write("No songs yet.")

# --- Controls ---
st.markdown("---")
st.header("▶️ Playback Controls")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⏪ Previous"):
        st.session_state.playlist.prev_song()
        st.session_state.playlist.play_current_song()

with c2:
    if st.button("▶️ Play"):
        st.session_state.playlist.play_current_song()

with c3:
    if st.button("⏩ Next"):
        st.session_state.playlist.next_song()
        st.session_state.playlist.play_current_song()

st.markdown("---")
st.write(f"Total songs: {st.session_state.playlist.get_length()}")
