#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os

from gi.repository import Gedit, Gtk, Gdk

from mr_globals import *
from mr_msgbox import *
from mr_source_file import *
from mr_console import *
from mr_make import *
from mr_find_file_from_error import *


menu_ui = """
<ui>

    <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">

      <placeholder name="ToolsOps_3">
        <menuitem action="Make" />
        <menuitem action="Rebuild" />
        <separator/>
        <menuitem action="Run" />
        <separator/>
        <menuitem action="MakeClean" />
        <menuitem action="ConfigMakeAndRun" />
      </placeholder>

    </menu>
    </menubar>

    <toolbar name="ToolBar">
        <separator/>
        <toolitem action="Make"/>
        <toolitem action="Rebuild"/>
        <separator/>
        <toolitem action="Run"/>
        <separator/>
        <toolitem action="MakeClean"/>
        <toolitem action="ConfigMakeAndRun" />
    </toolbar>

</ui>
"""



class MakeAndRun:

    def __init__(self, window, pluginManager):
        Gdk.threads_init()
        
        self.window = window
        self.pluginManager = pluginManager
        self.src = None
        self.doc_errors = []

        global menu_ui

        actionMake = ("Make",
                  Gtk.STOCK_CONVERT,
                  "_Make",
                  "<Shift>F5",
                  "Executa make no diretório atual",
                  self.on_action_make )

        actionMakeClean = ("MakeClean",
                  Gtk.STOCK_CLEAR,
                  "Make C_lean",
                  "",
                  "Executa make clean no diretório atual",
                  self.on_action_make_clean )

        actionRebuild = ("Rebuild",
                  Gtk.STOCK_REFRESH,
                  "_Rebuild",
                  "<Control>F5",
                  "Executa make clean seguido de make no diretório atual",
                  self.on_action_rebuild )

        actionRun = ("Run",
                  Gtk.STOCK_MEDIA_PLAY,
                  "_Executar",
                  "F5",
                  "Roda o script python ou executa 'make exec'",
                  self.on_action_run )

        actionConfigMakeAndRun = ("ConfigMakeAndRun",
                  Gtk.STOCK_PREFERENCES,
                  "_Configurar Make and Run...",
                  "",
                  "Configura o plugin MakeAndRun",
                  self.on_action_config )

        self.action_group = Gtk.ActionGroup("MakePluginActions")
        self.action_group.add_actions( [ \
            actionMake,
            actionMakeClean,
            actionRebuild,
            actionRun,
            actionConfigMakeAndRun], window )


        # ajusta algumas coisas extras pra ficar bonito em todas
        # as configuracoes de visual de barras:
        # text beside items, text below items, icons only, etc.
        #
        self.action_group.get_action( "Run" ).set_property("is-important", True)
        self.action_group.get_action( "Run" ).set_property( \
            "short-label", " Executar") # deixa um espaço a mais, de propósito.
        self.action_group.get_action( "ConfigMakeAndRun" ).set_property( \
            "short-label", "Config. Make")

        ui_manager = window.get_ui_manager()
        ui_manager.insert_action_group( self.action_group, 0 )

        self.ui_id = ui_manager.add_ui_from_string( menu_ui )

        # constroi a gui nesta window
        #

        builder = Gtk.Builder()
        builder.add_from_file( GLADE_FILE_OUTPUT )

        self.area = builder.get_object( "area" )
        self.listOutput = builder.get_object( "listOutput" )
        self.storeOutput = builder.get_object( "storeOutput" )
        self.btnClear = builder.get_object( "btnClear" )

        self.btnClear.connect( "clicked", self.on_btnClear )
        self.listOutput.connect( "row-activated", self.on_listOutput_itemActivated )

        renderer1 = Gtk.CellRendererText()
        renderer2 = Gtk.CellRendererText()
        renderer3 = Gtk.CellRendererText()

        renderer1.set_property( "cell-background", "#ddcd4d" )
        renderer2.set_property( "font", "Bold" )
        renderer2.set_property( "cell-background", "#dd8d8d" )
        renderer3.set_property( "font", "Monospace Bold" )
        renderer3.set_property( "cell-background", "#dd8d8d" )

        coluna1 = Gtk.TreeViewColumn( "Arquivo", renderer1, text=0 )
        coluna2 = Gtk.TreeViewColumn( "Linha", renderer2, text=1 )
        coluna3 = Gtk.TreeViewColumn( "Mensagem", renderer3, text=2 )

        self.listOutput.append_column( coluna1 )
        self.listOutput.append_column( coluna2 )
        self.listOutput.append_column( coluna3 )

        img = Gtk.Image()
        img.set_from_icon_name( "stock_mark", Gtk.IconSize.MENU )

        bottom = window.get_bottom_panel()
        bottom.add_item( self.area, "CompilerOutput", "Saída do Compilador", img )



    def __del__(self):
        ui_manager = self.window.get_ui_manager()
        ui_manager.remove_ui( self.ui_id )
        ui_manager.remove_action_group( self.action_group )
        ui_manager.ensure_update()

        bottom = self.window.get_bottom_panel()
        bottom.remove_item( self.area )



    def update(self):
        tem_doc = self.window.get_active_document() != None
        self.action_group.set_sensitive( tem_doc )



    def clear_errors(self):
        for er in self.doc_errors:
            er.remove_error()
        self.doc_errors = []

    
    def on_btnClear(self, *args):
        self.storeOutput.clear()
        self.clear_errors()

        bottom = self.window.get_bottom_panel()
        bottom.hide()


    def on_listOutput_itemActivated(self, treeview, path, *args):
        it = self.storeOutput.get_iter( path )
        find_file_from_error( self, it )


    def get_src(self):
        # tenta re-utilizar um SourceFile() ja construido,
        # se for o mesmo documento.
        #
        if self.src != None:

            same_window = self.src.window == self.window
            same_doc = self.src.doc.get_location() == \
                self.window.get_active_document().get_location()

            if same_window and same_doc:
                return self.src

        self.src = SourceFile( self, self.window, self.pluginManager )
        return self.src



    def on_action_make(self, *args):

        src = self.get_src()
        if not src.check_salvou():
            return

        MakefileManager( src ).make_build( self, rebuilding = False )


    def on_action_make_clean(self, *args):

        src = self.get_src()
        if not src.check_salvou():
            return

        MakefileManager( src ).make_clean()


    def on_action_rebuild(self, *args):

        src = self.get_src()
        if not src.check_salvou():
            return

        MakefileManager( src ).make_build( self, rebuilding = True )


    def on_action_run(self, *args):

        src = self.get_src()
        if not src.check_salvou():
            return

        src.muda_pro_diretorio_do_arquivo()

        if src.is_lang_python():

            cmd = configurations.cmd_run_python + " -u"
            roda_cmd( cmd + " " + ("\'\"%s\"\'" % src.get_filename()) , \
                auto_close = configurations.run_auto_close_window )
            return
        
        if src.is_lang_js():

            cmd = configurations.cmd_run_js
            roda_cmd( cmd + " " + ("\'\"%s\"\'" % src.get_filename()) , \
                auto_close = configurations.run_auto_close_window )
            return


        # chegou aqui? entao eh pra rodar algo como 'make exec'
        #

        MakefileManager( src ).make_exec()


    def on_action_config(self, *args):

        w = self.pluginManager.create_configure_dialog()
        w.show()

