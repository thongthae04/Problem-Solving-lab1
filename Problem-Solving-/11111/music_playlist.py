import streamlit as st

st.set_page_config(page_title="Music Playlist", page_icon="🎶")

# ---------- Song Class ----------
class Song:
    def __init__(self, title, artist, audio_file=None):
        self.title = title
        self.artist = artist
        self.audio_file = audio_file
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"


# ---------- MusicPlaylist Class ----------
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
        songs = []
        current = self.head
        index = 1
        while current:
            marker = "▶️ " if current == self.current_song else ""
            songs.append(f"{marker}{index}. {current.title} - {current.artist}")
            current = current.next_song
            index += 1
        return songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
            if self.current_song.audio_file:
                st.audio(self.current_song.audio_file)
            else:
                st.warning("This song has no audio file.")
        else:
            st.warning("Playlist is empty.")

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        else:
            st.warning("End of playlist.")

    def prev_song(self):
        if self.current_song == self.head:
            st.warning("Already at the first song.")
            return

        current = self.head
        while current and current.next_song != self.current_song:
            current = current.next_song

        if current:
            self.current_song = current

    def delete_song(self, title):
        if not self.head:
            st.warning("Playlist is empty.")
            return

        if self.head.title == title:
            self.head = self.head.next_song
            self.current_song = self.head
            self.length -= 1
            st.success(f"Deleted: {title}")
            return

        prev = self.head
        curr = self.head.next_song

        while curr:
            if curr.title == title:
                prev.next_song = curr.next_song
                if self.current_song == curr:
                    self.current_song = prev
                self.length -= 1
                st.success(f"Deleted: {title}")
                return
            prev = curr
            curr = curr.next_song

        st.error("Song not found.")

    def get_length(self):
        return self.length


# ---------- Streamlit UI ----------
st.title("🎶 Music Playlist App")

if "playlist" not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

playlist = st.session_state.playlist

# ---------- Sidebar ----------
st.sidebar.header("➕ Add Song (Manual)")
title = st.sidebar.text_input("Song Title")
artist = st.sidebar.text_input("Artist")

if st.sidebar.button("Add Song"):
    if title and artist:
        playlist.add_song(title, artist)
    else:
        st.sidebar.warning("Please fill in both fields.")

st.sidebar.markdown("---")

st.sidebar.header("🎵 Upload MP3")
uploaded_file = st.sidebar.file_uploader(
    "Upload audio file",
    type=["mp3", "wav"]
)

if uploaded_file:
    song_title = uploaded_file.name.rsplit(".", 1)[0]
    playlist.add_song(song_title, "Unknown", uploaded_file)

st.sidebar.markdown("---")

st.sidebar.header("🗑 Delete Song")
delete_title = st.sidebar.text_input("Title to delete")
if st.sidebar.button("Delete"):
    if delete_title:
        playlist.delete_song(delete_title)

# ---------- Main Content ----------
st.header("📃 Playlist")

songs = playlist.display_playlist()
if songs:
    for s in songs:
        st.write(s)
else:
    st.write("Playlist is empty.")

st.markdown("---")

st.header("▶️ Playback Controls")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏪ Previous"):
        playlist.prev_song()
        playlist.play_current_song()

with col2:
    if st.button("▶️ Play"):
        playlist.play_current_song()

with col3:
    if st.button("⏩ Next"):
        playlist.next_song()
        playlist.play_current_song()

st.markdown("---")
st.write(f"🎶 Total songs: {playlist.get_length()}")
