# -*- coding: utf-8 -*-
import unicodedata
import os
import sys
    
def notify(title, message):
    sys.stdout.write('\a')
    sys.stdout.flush()
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(message, title))
    
def speak(text):
    # os.system("say -v Anna '%s'" % text)
    notify(title = 'Constructor', message  = text)