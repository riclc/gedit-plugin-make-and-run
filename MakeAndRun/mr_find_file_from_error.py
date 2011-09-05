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
import gio
from glob import *

from mr_msgbox import *


def find_file_from_error(mrplugin, error_iter, can_msgbox = True):
    
    # error_iter = iter do objeto 'storeOutput'
    #
    
    arq = mrplugin.storeOutput.get_value( error_iter, 0 )
    linha = mrplugin.storeOutput.get_value( error_iter, 1 ) - 1

    arq_full = os.path.abspath( os.path.join( mrplugin.get_src().get_dir(), arq ) )
    arq_full_uri = gio.File( arq_full ).get_uri()

    # procura o documento aberto no gedit que possa ter o mesmo
    # basename que o arquivo indicado no erro relatado.
    #
    for d in mrplugin.window.get_documents():
        doc_arq_uri = d.get_uri()
        
        if arq_full_uri == doc_arq_uri:
        
            # define um novo 'active_document' 
            #
            tab = gedit.tab_get_from_document( d )
            mrplugin.window.set_active_tab( tab )
            
            mrplugin.get_src().remove_error()
            mrplugin.get_src().mark_error( linha )
            
            return
            
    # chegou aqui? entao nao achou o arquivo aberto no gedit.
    # tenta abrir entao..
        
    if not os.path.exists( arq_full ):
        if can_msgbox:
            msgbox( "Ir para linha do erro", \
                "O arquivo indicado nessa linha do erro não foi encontrado." + \
                "\n\n" + \
                "<small><b>Arquivo buscado:</b> " + arq_full + " </small>", \
                "warning" \
            )
            
        return
    
    #arq_uri = "file://" + arq_full
    arq_uri = gio.File( arq_full ).get_uri()
    
    new_tab = mrplugin.window.create_tab_from_uri(
        uri = arq_uri,
        encoding = gedit.encoding_get_current(),
        line_pos = linha,
        create = False,
        jump_to = True
    )
    
    # pra variar, mais outro esquema do gedit que eh assincrono,
    # isto eh, a criacao de tabs (acima) vai emitir signals e etc.
    #
    # pra continuar o codigo supondo que tudo isso ja foi processado,
    # devemos rodar varias iteracoes do looping do gtk.
    #
    # sem fazer isso, os comandos em seguida (get_src().mark_error
    # etc.) nao funcionarao adequadamente.
    #
    while gtk.events_pending():
        gtk.main_iteration( block=False )
    
    # com a nova tab ativada, o 'active_document' muda.
    # assim, fazemos get_src() pra ativar o erro nele.
    #
    mrplugin.get_src().remove_error()
    mrplugin.get_src().mark_error( linha )


