from pygame import mixer


class Audio:
    """
    Stores the information of an audio.

    :param audio_name: str
        The audio name.
    :param file_location: str
        The absolute or relative file location.
    """
    def __init__(self, audio_name, file_location=None):
        self.audio_name = audio_name
        self.file_location = file_location
        self.playing = False
        self.paused = False

    def play(self):
        """Play the audio."""
        mixer.music.load(self.file_location)
        mixer.music.set_volume(0.5)
        mixer.music.play()
        self.playing = True

    def stop(self):
        """Stop the audio."""
        mixer.music.stop()
        self.playing = False

    def pause(self):
        """Pause the audio."""
        mixer.music.pause()
        self.playing = False
        self.paused = True

    def unpause(self):
        """Unpause the audio."""
        mixer.music.unpause()
        self.paused = False
