# -*- coding: utf-8 -*-
import os
import errno
from settings import ROOT_DIR
import json
from string import Template

class Constructor:
    
    def __init__(self, app_name):
        self.app_name = app_name
        self.app_codename = app_name.lower().replace(' ', '_')
        
        if not os.path.exists("%s/models/%s" % (ROOT_DIR, self.app_codename)):
            self.use_app()
        if not os.path.exists("%s/views/%s" % (ROOT_DIR, self.app_codename)):
            self.use_app()
            
        print("* Modelos e Views carregadas para: %s" % self.app_name)
        
    def use_app(self):
        os.makedirs('%s/views/%s' % (ROOT_DIR, self.app_codename))
        os.makedirs('%s/models/%s' % (ROOT_DIR, self.app_codename))
            
    def view_page(self, page_name='home', style='material', template='basic'):
        
        #Open template file
        template_content = None
        with open('%s/templates/%s/%s.cia' % (ROOT_DIR, style, template), 'r') as content_file:
            template_content = content_file.read()
        
        # Build with model
        fina_template = Template(template_content).safe_substitute({
            "title": "Usuários",
            "description": "Um site para usuários",
            "search_label": "Buscar",
            "h3": "Biografia",
            "body_content": "Eu sou o guilherme e criei essa porra.",
        })
            
        # Write View
        view_file = open("%s/views/%s/%s.html" % (ROOT_DIR, self.app_codename, page_name), "w") 
        view_file.write(fina_template)
        view_file.close()
        
    def create_model(self, model_name, data=None):
        #Write Model
        model_file = open("%s/models/%s/%s.db" % (ROOT_DIR, self.app_codename, model_name), "w") 
        if data:
            model_file.write(json.dumps(data))
        model_file.close()
        
    def select_model(self, model_name, id_model=None):
        with open('%s/models/%s/%s.db' % (ROOT_DIR, self.app_codename, model_name), 'r') as content_file:
            model_content = content_file.read()
        model_content = json.loads(model_content)
        if id_model:
            for m in model_content:
                if id_model == m.id:
                    selected_model = m
            return selected_model
        return model_content
        
        
    def run(self, port=3000):
        os.system( "cd %s/views/%s && python -m SimpleHTTPServer %s" % (ROOT_DIR, self.app_codename, port) )
        print(" * Rodando em http://localhost:%s * " % port)
