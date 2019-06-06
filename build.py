# -*- coding: utf-8 -*-
from controllers.constructor import Constructor
import speech_recognition as sr
import pyautogui as pag
import os
from controllers.util import speak
import time

ACTUAL_CONSTRUCTOR = None
ACTUAL_LIST = None
ACTUAL_INTENTION = False
ACTUAL_CONFIRMATION = False
ACTUAL_TYPE_VIEW = None
ACTUAL_SUB_INTENTION = None
ACTUAL_TITLE_CONTENT = False
ACTUAL_DESCRIPTION_CONTENT = False

def build_basic():
    build = Constructor(app_name = "Usuario", app_description = "Um site de testes legais")
    m_users = build.create_model(model_name = "users", data = [
        {
            "id": 1,
            "name": "Guilherme",
            "age": 23,
            "location": "Sao Paulo, Brazil",
        },
        {
            "id": 2,
            "name": "Joaozinho",
            "age": 30,
            "location": "Bahia, Brazil",
        }
    ])
    build.view_page(
        page_name = "index", 
        style = "material", 
        template = "basic",
        data = {
            "title": build.app_name,
            "description": build.app_description,
            "search_label": "Buscar",
            "h3": "Biografia",
            "body_content": build.get_widget(
                style='material', 
                widget='table', 
                data=m_users['results']
            ),
        })
    build.run()

while True:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        os.system('cls' if os.name=='nt' else 'clear')
        print('Voice Programming')
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language = "pt-br", show_all=False)
        text = text.lower()
        print(text)
        
        if not ACTUAL_INTENTION:
            if 'atualizar' in text:
                pag.press("command")
                pag.press("shift")
                pag.press("r")
                # speak('Página atualizada.')

            elif 'criar aplicativo' in text:
                app_name = text.replace('criar aplicativo', '').strip()
                if app_name:
                    ACTUAL_CONSTRUCTOR = Constructor( app_name = app_name.capitalize() )
                    speak('Aplicativo %s criado com sucesso.' % app_name)
                    ACTUAL_INTENTION = 'build_project'
                else:
                    speak('Qual seria o nome do aplicativo?')
                    ACTUAL_INTENTION = 'create_app'
                    
            elif 'publicar' in text:
                speak('Iniciando construção do aplicativo %s.' % ACTUAL_CONSTRUCTOR.app_name)
                ACTUAL_INTENTION = 'build_project'
        
        else:
            # INTENTIONS
            
            # Criar aplicativo
            if ACTUAL_INTENTION == 'create_app':
                ACTUAL_CONSTRUCTOR = Constructor( app_name = text.capitalize() )
                speak('Aplicativo %s criado com sucesso.' % text)
                ACTUAL_INTENTION = 'build_project'
                
            # Construir página
            if ACTUAL_INTENTION == 'build_project':
                
                if ACTUAL_SUB_INTENTION == 'type_view':
                    ACTUAL_TYPE_VIEW = text
                elif ACTUAL_SUB_INTENTION == 'title':
                    ACTUAL_TITLE_CONTENT = text
                elif ACTUAL_SUB_INTENTION == 'description':
                    ACTUAL_DESCRIPTION_CONTENT = text
                elif ACTUAL_SUB_INTENTION == 'confirmation':
                    if text == 'sim':
                        ACTUAL_CONFIRMATION = True
                
                if not ACTUAL_TYPE_VIEW:
                    speak('Qual seria o tipo de conteúdo?')
                    ACTUAL_SUB_INTENTION = 'type_view'
                elif not ACTUAL_TITLE_CONTENT:
                    speak('Qual seria o título do conteúdo?')
                    ACTUAL_SUB_INTENTION = 'title'
                elif not ACTUAL_DESCRIPTION_CONTENT:
                    speak('Qual seria a descrição do conteúdo?')
                    ACTUAL_SUB_INTENTION = 'description'
                elif not ACTUAL_CONFIRMATION:
                    speak('Você confirma a criação do aplicativo %s?' % ACTUAL_CONSTRUCTOR.app_name)
                    ACTUAL_SUB_INTENTION = 'confirmation'
                else:
                    ACTUAL_CONSTRUCTOR.view_page(
                        page_name = "index", 
                        style = "material", 
                        template = "basic",
                        data = {
                            "title": ACTUAL_CONSTRUCTOR.app_name,
                            "description": ACTUAL_CONSTRUCTOR.app_description,
                            "search_label": "Buscar",
                            "h3": ACTUAL_TITLE_CONTENT,
                            "body_content": ACTUAL_DESCRIPTION_CONTENT,
                        })
                    ACTUAL_CONSTRUCTOR.run()
                    # Clean
                    ACTUAL_TYPE_VIEW = None
                    ACTUAL_CONFIRMATION = False
                    ACTUAL_TITLE_CONTENT = False
                    ACTUAL_DESCRIPTION_CONTENT = False
                    ACTUAL_INTENTION = False
                    ACTUAL_SUB_INTENTION = False

        time.sleep(1)

    except LookupError as e:
        print("Could not understand audio: %s" % str(e))
    except sr.UnknownValueError:
        print("Slo could not understand audio")
    except sr.RequestError as e:
        print("Slo error; {0}".format(e))