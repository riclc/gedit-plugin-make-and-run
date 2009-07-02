#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os 
import os.path
import gtk
import gedit

from mr_msgbox import *
from mr_doc_error import *



class SourceFile:

    def __init__(self, window, pluginManager):
        self.window = window
        self.doc = window.get_active_document()
        self.view = window.get_active_view()        
        self.pluginManager = pluginManager
                
        self.docError = DocError( self.doc, self.view )

        
    def get_doc(self):
        return self.doc

        
    def get_arq(self):    
        if self.doc == None:
            return ""
        
        arq = self.doc.get_uri()
        if arq != "":
            arq = arq.replace( "file://", "" )
        
        return arq
        

    def get_dir(self):
        diretorio = os.path.dirname( self.get_arq() )
        return diretorio


    def get_lang(self):    
        if self.doc == None:
            return ""

        lang = self.doc.get_language()
        
        if lang == None:
            msgbox( "Linguagem",
                "O arquivo não está com uma linguagem " +
                "(<i>C, Python, etc.</i>) definida ainda.", "erro" )
            return ""
            
        return lang.get_id()


    def is_lang_python(self):    
        return self.get_lang() == 'python'


    def is_lang_c(self):    
        return self.get_lang() == 'c'
        

    def is_lang_cpp(self):
        return self.get_lang() == 'cpp'

            
    def check_salvou(self):
        if self.doc == None:
            msgbox(
                "Arquivo inexistente",
                "Nenhum arquivo está aberto.",
                "erro"
            )
            return False
            
        if self.doc.is_untitled():
            msgbox(
                "Arquivo não salvo",
                "Você precisa <b>salvar</b> seu arquivo.",
                "warning"
            )
            return False
        
        if self.doc.get_modified():
        
            save_auto = self.pluginManager.radioSaveAuto.get_active()
            
            if not save_auto:
                msgbox(
                    "Arquivo modificado",
                    "Você precisa salvar o código antes.\n",
                    "warning"
                )
                return False
            
            
            # faz o 'save' automaticamente...
            
            # isso vai emitir um signal "save"...
            self.doc.save(0)
            
            # observei que esse 'save' eh assincrono, entao...
            while gtk.events_pending():
                gtk.main_iteration( block=False )
                
            #while self.doc.get_modified() == True:
            #    gtk.main_iteration( block=False )
            #    continue
            
            # nesse ponto, o 'save' foi de fato efetuado.

        return True
    

    def muda_pro_diretorio_do_arquivo(self):
        os.chdir( self.get_dir() )
    

    def marca_erro(self, line):
        self.docError.marca_erro( line )
    
    
    def remove_erro(self):
        self.docError.remove_erro()

