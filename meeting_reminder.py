import subprocess

# Two types of remind message
# TODO add storage and add/update/delete interface for messages


def say_words(words):
    subprocess.check_call('say %s' % words)


def play_audio_file(path):
    from pygame import mixer
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
