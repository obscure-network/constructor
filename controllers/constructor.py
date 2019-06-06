# -*- coding: utf-8 -*-
import os
import errno
from settings import ROOT_DIR
import json
from string import Template
import unidecode

class Constructor:
    
    def __init__(self, app_name, app_description="Site gerado por voz pelo Constructor."):
        self.app_name = app_name
        self.app_description = app_description
        self.app_codename = unidecode.unidecode(app_name.lower().replace(' ', '_'))
        print(self.app_codename)
        
        if not os.path.exists("%s/models/%s" % (ROOT_DIR, self.app_codename)):
            self.use_app()
        if not os.path.exists("%s/views/%s" % (ROOT_DIR, self.app_codename)):
            self.use_app()
            
        print("* Modelos e Views carregadas para: %s" % self.app_name)
        
    def use_app(self):
        os.makedirs('%s/views/%s' % (ROOT_DIR, self.app_codename))
        os.makedirs('%s/models/%s' % (ROOT_DIR, self.app_codename))
            
    def view_page(self, page_name='home', style='material', template='basic', data=None):
        
        #Open template file
        template_content = None
        with open('%s/templates/%s/%s.cia' % (ROOT_DIR, style, template), 'r') as content_file:
            template_content = content_file.read()
        
        # Build with model
        # {
        #     "title": "Usuários",
        #     "description": "Um site para usuários",
        #     "search_label": "Buscar",
        #     "h3": "Biografia",
        #     "body_content": "Eu sou o guilherme e criei essa porra.",
        # }
        if data:
            fina_template = Template(template_content).safe_substitute(data)
            
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
        return self.select_model(model_name)
        
    def select_model(self, model_name, id_model=None):
        with open('%s/models/%s/%s.db' % (ROOT_DIR, self.app_codename, model_name), 'r') as content_file:
            model_content = content_file.read()
        model_content = json.loads(model_content)
        if id_model:
            for m in model_content:
                if id_model == m.id:
                    selected_model = m
            return selected_model
        return {"name": model_name, "results": model_content}
        
    def get_widget(self, style='material', widget='table', data=None):
        widget_content = None
        if widget == 'table':
            _final_th = "<tr>"
            for key, value in reversed(data[0].items()):
                _final_th += "<th>%s</th>" % key.capitalize()
            _final_th += "</tr>"
            _final_td = ""
            for td in data:
                _final_td += "<tr>"
                for key, value in reversed(td.items()):
                    _final_td += "<td>%s</td>" % value
                _final_td += "</tr>"
            with open('%s/templates/%s/%s.cia' % (ROOT_DIR, style, widget), 'r') as content_file:
                widget_content = content_file.read()
            widget_content = Template(widget_content).safe_substitute({"th": _final_th, "td": _final_td})
        if widget == 'text':
            widget_content = data
        return widget_content
    
    def run(self, port=3000):
        os.system( "cd %s/views/%s && python -m http.server %s" % (ROOT_DIR, self.app_codename, port) )
        print(" * Rodando em http://localhost:%s * " % port)
