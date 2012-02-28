#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os 
from glob import *

from gi.repository import Gedit, Gtk, Gio

from mr_msgbox import *


def find_file_from_error(mrplugin, error_iter, can_msgbox = True):
    
    # error_iter = iter do objeto 'storeOutput'
    #
    
    arq = mrplugin.storeOutput.get_value( error_iter, 0 )
    linha = mrplugin.storeOutput.get_value( error_iter, 1 ) - 1

    # tenta algumas alternativas para achar o arquivo
    #
    base_dir = mrplugin.get_src().get_dir()
    candidates = ["", "..", "src", "include"]
    for i in range(len(candidates)):
        candidates[i] = os.path.abspath( os.path.join(base_dir, candidates[i], arq) )
    
    arq_full = candidates[0]
    for c in candidates:
        if os.path.exists(c):
            arq_full = c
            break
    arq_full_uri = Gio.File.new_for_path( arq_full ).get_uri()


    # procura o documento aberto no gedit que possa ter o mesmo
    # uri que o arquivo indicado no erro relatado.
    #
    for d in mrplugin.window.get_documents():
        gfile = d.get_location()
        doc_arq_uri = "" if gfile == None else gfile.get_uri()
        
        if arq_full_uri == doc_arq_uri:
        
            # define um novo 'active_document' 
            #
            #tab = Gedit.tab_get_from_document( d )
            tab = mrplugin.window.get_tab_from_location( d.get_location() )
            mrplugin.window.set_active_tab( tab )
            
            mrplugin.clear_errors()
            mrplugin.get_src().mark_error( linha )
            
            return

    # já que não achou um URI completo, procura um documento aberto
    # no gedit que possa ter pelo menos o mesmo basename (ex.: a.c).
    #
    arq_basename = os.path.basename( Gio.File.new_for_path( arq_full ).get_path() )
    
    for d in mrplugin.window.get_documents():
        gfile = d.get_location()
        doc_arq_path = "" if gfile == None else gfile.get_path()
        
        doc_arq_basename = os.path.basename( doc_arq_path )        
        if arq_basename == doc_arq_basename:
        
            # define um novo 'active_document' 
            #
            #tab = Gedit.tab_get_from_document( d )
            tab = mrplugin.window.get_tab_from_location( d.get_location() )
            mrplugin.window.set_active_tab( tab )
            
            mrplugin.clear_errors()
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
    
    arq_loc = Gio.File.new_for_path( arq_full )
    
    new_tab = mrplugin.window.create_tab_from_location(
        location = arq_loc,
        encoding = None,
        line_pos = linha,
        column_pos = 0,
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
    while Gtk.events_pending():
        Gtk.main_iteration_do( blocking=False )
    
    # com a nova tab ativada, o 'active_document' muda.
    # assim, fazemos get_src() pra ativar o erro nele.
    #
    mrplugin.clear_errors()
    mrplugin.get_src().mark_error( linha )


