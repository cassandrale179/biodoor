# # from gtts import gTTS
# # import os
# # cwd = os.getcwd()
# # tts = gTTS(text='Hello', lang='en', slow=True)
# # tts.save(os.path.join(cwd, "hello.mp3"))
# from gtts import gTTS
# import os
# # def tts(doorStatus, ownername):
# # text_tts = 'Welcome Minh';
# tts = gTTS(text='Motherfucker', lang='en')
# tts.save("welcome.mp3")
# # os.system("mpg321 welcome.mp3")

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
def speakNow(name):
    str_speech = "Welcome home " + name
    speak.Speak(str_speech)
