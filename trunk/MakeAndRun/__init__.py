#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file



import gedit
import gtk

from mr_main import *
from mr_globals import *


class MakeAndRunManager(gedit.Plugin):

    def __init__(self):
        gedit.Plugin.__init__(self)
        self.per_window_plugins = {}
        self.build_gui()
        configurations.load()

    def activate(self, window):
        self.per_window_plugins[window] = MakeAndRun( window, self )

    def deactivate(self, window):
        self.per_window_plugins[window].__del__()

    def update_ui(self, window):
        self.per_window_plugins[window].update()


    def is_configurable(self):
        return True

    def create_configure_dialog(self):
        self.read_configurations()
        return self.windowConfig


    def build_gui(self):
        builder = gtk.Builder()
        builder.add_from_file( GLADE_FILE_CONFIG )

        self.windowConfig = builder.get_object( "windowConfig" )
        self.btnOK = builder.get_object( "btnOK" )
        self.btnCancel = builder.get_object( "btnCancel")
        self.textC = builder.get_object( "textC" )
        self.textCpp = builder.get_object( "textCpp" )
        self.textPythonComp = builder.get_object( "textPythonComp" )
        self.radioSaveAuto = builder.get_object( "radioSaveAuto" )
        self.radioSaveManual = builder.get_object( "radioSaveManual" )
        self.textMakeExec = builder.get_object( "textMakeExec" )
        self.textPanelSize = builder.get_object( "textPanelSize" )
        self.checkPanelSizeIgnore = builder.get_object( "checkPanelSizeIgnore" )
        self.checkShowTerminal = builder.get_object( "checkShowTerminal" )
        self.checkShowWarnings = builder.get_object( "checkShowWarnings" )
        self.checkFecharAuto = builder.get_object( "checkFecharAuto" )
        self.checkMakeFecharAuto = builder.get_object( "checkMakeFecharAuto" )

        # ajeita algumas imagens
        #
        self.imgComp = builder.get_object( "imgComp" )
        self.imgComp.set_from_file( IMG_COMP )

        self.imgSave = builder.get_object( "imgSave" )
        self.imgSave.set_from_file( IMG_SAVE )

        self.imgTerm = builder.get_object( "imgTerm" )
        self.imgTerm.set_from_file( IMG_TERM )

        self.imgGedit = builder.get_object( "imgGedit" )
        self.imgGedit.set_from_file( IMG_GEDIT )
        #
        ######

        self.btnOK.connect( "clicked", self.configure_on_close_saving )
        self.btnCancel.connect( "clicked", self.configure_on_close )
        self.windowConfig.connect( "delete-event", self.configure_on_close )


    def configure_on_close(self, *arg):
        self.windowConfig.hide()

    def configure_on_close_saving(self, *arg):
        self.windowConfig.hide()
        self.write_configurations()


    def read_configurations(self):
        configurations.load()

        self.textC.set_text( configurations.compile_c )
        self.textCpp.set_text( configurations.compile_cpp )
        self.textPythonComp.set_text( configurations.compile_python )
        self.radioSaveAuto.set_active( configurations.compile_autosave )
        self.radioSaveManual.set_active( not configurations.compile_autosave )

        self.textMakeExec.set_text( configurations.cmd_make_exec )
        self.checkShowTerminal.set_active( configurations.show_terminal )
        self.checkShowWarnings.set_active( configurations.show_warnings )
        self.checkMakeFecharAuto.set_active( configurations.make_auto_close_window )        
        self.checkFecharAuto.set_active( configurations.run_auto_close_window )

        self.textPanelSize.set_text( str(configurations.bottom_panel_size) )
        self.checkPanelSizeIgnore.set_active( configurations.bottom_panel_size_ignore )


    def write_configurations(self):
        configurations.compile_c = self.textC.get_text()
        configurations.compile_cpp = self.textCpp.get_text()
        configurations.compile_python = self.textPythonComp.get_text()
        configurations.compile_autosave = self.radioSaveAuto.get_active()

        configurations.cmd_make_exec = self.textMakeExec.get_text()
        configurations.show_terminal = self.checkShowTerminal.get_active()
        configurations.show_warnings = self.checkShowWarnings.get_active()
        configurations.make_auto_close_window = self.checkMakeFecharAuto.get_active()        
        configurations.run_auto_close_window = self.checkFecharAuto.get_active()

        configurations.bottom_panel_size = int( self.textPanelSize.get_text() )
        configurations.bottom_panel_size_ignore = self.checkPanelSizeIgnore.get_active()

        configurations.save()
    
