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
import mr_globals


class MakeAndRunManager(gedit.Plugin):

    def __init__(self):
        gedit.Plugin.__init__(self)
        self.per_window_plugins = {}
        self.build_gui()

    def activate(self, window):
        self.per_window_plugins[window] = MakeAndRun( window, self )
    
    def deactivate(self, window):
        self.per_window_plugins[window].__del__()
        
    def update_ui(self, window):
        self.per_window_plugins[window].update()


    def is_configurable(self):
        return True
    
    def create_configure_dialog(self):        
        return self.windowConfig
    
    
    def build_gui(self):    
        builder = gtk.Builder()
        builder.add_from_file( GLADE_FILE_CONFIG )
        
        self.windowConfig = builder.get_object( "windowConfig" )
        self.btnClose = builder.get_object( "btnClose" )        
        self.textC = builder.get_object( "textC" )
        self.textCpp = builder.get_object( "textCpp" )
        self.textPythonComp = builder.get_object( "textPythonComp" )
        self.radioSaveAuto = builder.get_object( "radioSaveAuto" )
        self.radioSaveManual = builder.get_object( "radioSaveManual" )
        self.textMakeExec = builder.get_object( "textMakeExec" )
        self.radioPythonMake = builder.get_object( "radioPythonMake" )
        self.radioPythonInterp = builder.get_object( "radioPythonInterp" )
        self.textPanelSize = builder.get_object( "textPanelSize" )
        self.checkPanelSizeIgnore = builder.get_object( "checkPanelSizeIgnore" )
        self.checkShowTerminal = builder.get_object( "checkShowTerminal" )
        self.checkFecharAuto = builder.get_object( "checkFecharAuto" )

        # ajeita algumas imagens
        #        
        self.imgComp = builder.get_object( "imgComp" )
        self.imgComp.set_from_file( IMG_COMP )

        self.imgSave = builder.get_object( "imgSave" )
        self.imgSave.set_from_file( IMG_SAVE )

        self.imgTerm = builder.get_object( "imgTerm" )
        self.imgTerm.set_from_file( IMG_TERM )
        
        self.imgPython = builder.get_object( "imgPython" )
        self.imgPython.set_from_file( IMG_PYTHON )
        
        self.imgGedit = builder.get_object( "imgGedit" )
        self.imgGedit.set_from_file( IMG_GEDIT )
        #
        ######

        
        self.btnClose.connect( "clicked", self.configure_on_close )
        self.windowConfig.connect( "delete-event", self.configure_on_close )
        self.radioPythonInterp.set_active( True )


    def configure_on_close(self, *arg):
        self.windowConfig.hide()

        print "setando checked_show_terminal..."
        mr_globals.checked_show_terminal = self.checkShowTerminal.get_active()

