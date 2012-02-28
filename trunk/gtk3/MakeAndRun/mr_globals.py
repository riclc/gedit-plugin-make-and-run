#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os.path
#from gi.repository import GConf

GLADE_FILE_CONFIG = os.path.join( os.path.dirname( __file__ ), "gui_config.glade" )
GLADE_FILE_OUTPUT = os.path.join( os.path.dirname( __file__ ), "gui_output.glade" )
GLADE_FILE_MAKEFILE = os.path.join( os.path.dirname( __file__ ), "gui_makefile.glade" )
GLADE_FILE_PROCESS = os.path.join( os.path.dirname( __file__ ), "gui_process.glade" )

IMG_COMP = os.path.join( os.path.dirname( __file__ ), "imgs", "iconComp.png" )
IMG_SAVE = os.path.join( os.path.dirname( __file__ ), "imgs", "iconSave.png" )
IMG_TERM = os.path.join( os.path.dirname( __file__ ), "imgs", "iconTerm.png" )
IMG_PYTHON = os.path.join( os.path.dirname( __file__ ), "imgs", "iconPython.png" )
IMG_GEDIT = os.path.join( os.path.dirname( __file__ ), "imgs", "iconGedit.png" )
IMG_MAKE = os.path.join( os.path.dirname( __file__ ), "imgs", "iconMake.png" )
IMG_PYTHON_BIG = os.path.join( os.path.dirname( __file__ ), "imgs", "iconPythonBig.png" )

IMG_RESULT_OK = os.path.join( os.path.dirname( __file__ ), "imgs", "animOK.gif" )
IMG_RESULT_ERROR = os.path.join( os.path.dirname( __file__ ), "imgs", "animError.gif" )
IMG_RESULT_CLEAN = os.path.join( os.path.dirname( __file__ ), "imgs", "animClean.gif" )


#GCONF_DIR = "/apps/gedit-2/plugins/make-and-run/"
GCONF_DIR = ""
#
#
# nesse exato momento, GConf papoca (crash), e o GSettings (que usa o DConf
# aqui no Linux) só aceita configurações se houver um schema-file em
# /usr/share/glib-2.0/schemas/ (não aceita ainda ~/.local/...). ver bug
# https://bugzilla.gnome.org/show_bug.cgi?id=645254. então, por enquanto,
# salvamos tudo num arquivo por aqui mesmo, manualmente.
#
#
#
class ManualClientItem:
    def __init__(self, val):
        self.val = val
        
    def get_string(self):
        return str(self.val)
    
    def get_int(self):
        return int(self.val)
    
    def get_bool(self):
        if type(self.val) == str:
            return self.val.lower() == 'true'
        else:
            return bool(self.val)
        
class ManualClient:
    def __init__(self):
        self.vars = {}
        self.filename = os.path.join( os.path.dirname( __file__ ), "config.ini" )
    
    def manual_load(self):
        self.vars = {}
        if not os.path.exists( self.filename ): return
        f = open( self.filename, "r" )
        s = f.read()
        f.close()
        for line in s.split('\n'):
            line = line.strip()
            if len(line) == 0: continue
            var_name, var_value = line.split(' => ')
            self.vars[var_name] = ManualClientItem( var_value )
    
    def manual_save(self):
        f = open( self.filename, "w" )
        for var_name in self.vars:
            f.write( "%s => %s\n" % (var_name, self.vars[var_name].val) )
        f.close()
        
    def get(self, name):
        return self.vars[name]
    
    def set_string(self, name, val):
        self.vars[name] = ManualClientItem( str(val) )
    
    def set_int(self, name, val):
        self.vars[name] = ManualClientItem( int(val) )
    
    def set_bool(self, name, val):
        self.vars[name] = ManualClientItem( bool(val) )        



class configurations:
    cmd_run_python                       = "python"
    cmd_run_js                           = "gjs"
    
    compile_autosave                     = True

    cmd_make_exec                        = "exec"
    show_terminal                        = True
    show_warnings			             = False
    make_auto_close_window               = True    
    run_auto_close_window                = True

    bottom_panel_size                    = 200
    bottom_panel_size_ignore             = False


    @staticmethod
    def load():
        #gclient = GConf.Client()
        gclient = ManualClient()
        gclient.manual_load()
 
        try:
            configurations.cmd_run_python = gclient.get( \
                GCONF_DIR + "cmd_run_python" ).get_string()
            configurations.cmd_run_js = gclient.get( \
                GCONF_DIR + "cmd_run_js" ).get_string()
            configurations.compile_autosave = gclient.get( \
                GCONF_DIR + "compile_autosave" ).get_bool()

            configurations.cmd_make_exec = gclient.get( \
                GCONF_DIR + "cmd_make_exec" ).get_string()
            configurations.show_terminal = gclient.get( \
                GCONF_DIR + "show_terminal" ).get_bool()
            configurations.show_warnings = gclient.get( \
                GCONF_DIR + "show_warnings" ).get_bool()
            configurations.make_auto_close_window = gclient.get( \
                GCONF_DIR + "make_auto_close_window" ).get_bool()
            configurations.run_auto_close_window = gclient.get( \
                GCONF_DIR + "run_auto_close_window" ).get_bool()

            configurations.bottom_panel_size = gclient.get( \
                GCONF_DIR + "bottom_panel_size" ).get_int()
            configurations.bottom_panel_size_ignore = gclient.get( \
                GCONF_DIR + "bottom_panel_size_ignore" ).get_bool()
        except:
            pass



    @staticmethod
    def save():
        #gclient = GConf.Client()
        gclient = ManualClient()

        gclient.set_string( GCONF_DIR + "cmd_run_python", \
            configurations.cmd_run_python )
        gclient.set_string( GCONF_DIR + "cmd_run_js", \
            configurations.cmd_run_js )
        gclient.set_bool( GCONF_DIR + "compile_autosave", \
            configurations.compile_autosave )

        gclient.set_string( GCONF_DIR + "cmd_make_exec", \
            configurations.cmd_make_exec )
        gclient.set_bool( GCONF_DIR + "show_terminal", \
            configurations.show_terminal )
        gclient.set_bool( GCONF_DIR + "show_warnings", \
            configurations.show_warnings )        
        gclient.set_bool( GCONF_DIR + "make_auto_close_window", \
            configurations.make_auto_close_window )
            
        gclient.set_bool( GCONF_DIR + "run_auto_close_window", \
            configurations.run_auto_close_window )

        gclient.set_int( GCONF_DIR + "bottom_panel_size", \
            configurations.bottom_panel_size )
        gclient.set_bool( GCONF_DIR + "bottom_panel_size_ignore", \
            configurations.bottom_panel_size_ignore )
        
        gclient.manual_save()
