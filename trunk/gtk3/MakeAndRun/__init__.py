#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file



from gi.repository import GObject, Gedit, Gtk

from mr_main import *
from mr_globals import *


make_and_run_singleton = None
make_and_run_counter = 0


class MakeAndRun_PerWindow(GObject.Object, Gedit.WindowActivatable):

    window = GObject.property( type=Gedit.Window )

    def __init__(self):
        global make_and_run_counter, make_and_run_singleton
        GObject.Object.__init__(self)

        #print "MakeAndRun perWindow: __init__() [counter = %d]" % make_and_run_counter
        make_and_run_counter += 1
        if make_and_run_counter == 1: make_and_run_singleton = MakeAndRunManager()


    def __del__(self):
        global make_and_run_counter, make_and_run_singleton

        #print "MakeAndRun perWindow: __del__() [counter = %d]" % make_and_run_counter        
        make_and_run_counter -= 1
        if make_and_run_counter == 0: make_and_run_singleton.__del__()


    def do_activate(self):
        make_and_run_singleton.new_window( self.window )

    def do_deactivate(self):
        make_and_run_singleton.del_window( self.window )

    def do_update_state(self):
        make_and_run_singleton.update_window( self.window )




# é um singleton
#
class MakeAndRunManager:

    def __init__(self):
        self.per_window_plugins = {}
        self.build_gui()
        configurations.load()
        #print "MakeAndRunManager: __init__()"

    def __del__(self):
        #print "MakeAndRunManager: __del__()"
        pass
    
    def new_window(self, window):
        self.per_window_plugins[window] = MakeAndRun( window, self )

    def del_window(self, window):
        self.per_window_plugins[window].__del__()

    def update_window(self, window):
        self.per_window_plugins[window].update()



    def create_configure_dialog(self):
        self.read_configurations()
        return self.windowConfig

    def build_gui(self):
        builder = Gtk.Builder()
        builder.add_from_file( GLADE_FILE_CONFIG )

        self.windowConfig = builder.get_object( "windowConfig" )
        self.btnOK = builder.get_object( "btnOK" )
        self.btnCancel = builder.get_object( "btnCancel")
        self.radioSaveAuto = builder.get_object( "radioSaveAuto" )
        self.radioSaveManual = builder.get_object( "radioSaveManual" )
        self.textMakeExec = builder.get_object( "textMakeExec" )
        self.textPanelSize = builder.get_object( "textPanelSize" )
        self.checkPanelSizeIgnore = builder.get_object( "checkPanelSizeIgnore" )
        self.checkShowTerminal = builder.get_object( "checkShowTerminal" )
        self.checkShowWarnings = builder.get_object( "checkShowWarnings" )
        self.checkFecharAuto = builder.get_object( "checkFecharAuto" )
        self.checkMakeFecharAuto = builder.get_object( "checkMakeFecharAuto" )
        self.entryCmdRunPython = builder.get_object("entryCmdRunPython")
        self.entryCmdRunJs = builder.get_object("entryCmdRunJs")        

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

        self.entryCmdRunPython.set_text( configurations.cmd_run_python )
        self.entryCmdRunJs.set_text( configurations.cmd_run_js )
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
        configurations.cmd_run_python = self.entryCmdRunPython.get_text()
        configurations.cmd_run_js = self.entryCmdRunJs.get_text()
        configurations.compile_autosave = self.radioSaveAuto.get_active()

        configurations.cmd_make_exec = self.textMakeExec.get_text()
        configurations.show_terminal = self.checkShowTerminal.get_active()
        configurations.show_warnings = self.checkShowWarnings.get_active()
        configurations.make_auto_close_window = self.checkMakeFecharAuto.get_active()        
        configurations.run_auto_close_window = self.checkFecharAuto.get_active()

        configurations.bottom_panel_size = int( self.textPanelSize.get_text() )
        configurations.bottom_panel_size_ignore = self.checkPanelSizeIgnore.get_active()

        configurations.save()
    
