#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os.path
import gconf

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


GCONF_DIR = "/apps/gedit-2/plugins/make-and-run/"


class configurations:
    compile_c                            = "gcc -c"
    compile_cpp                          = "g++ -c"
    compile_python                       = "pyflakes"
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
        gclient = gconf.client_get_default()

        try:
            configurations.compile_c = gclient.get( \
                GCONF_DIR + "compile_c" ).get_string()
            configurations.compile_cpp = gclient.get( \
                GCONF_DIR + "compile_cpp" ).get_string()
            configurations.compile_python = gclient.get( \
                GCONF_DIR + "compile_python" ).get_string()
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
        gclient = gconf.client_get_default()

        gclient.set_string( GCONF_DIR + "compile_c", \
            configurations.compile_c )
        gclient.set_string( GCONF_DIR + "compile_cpp", \
            configurations.compile_cpp )
        gclient.set_string( GCONF_DIR + "compile_python", \
            configurations.compile_python )
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
        
