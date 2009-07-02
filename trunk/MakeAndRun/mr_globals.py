#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os.path

GLADE_FILE_CONFIG = os.path.join( os.path.dirname( __file__ ), "gui_config.glade" )
GLADE_FILE_OUTPUT = os.path.join( os.path.dirname( __file__ ), "gui_output.glade" )
GLADE_FILE_MAKEFILE = os.path.join( os.path.dirname( __file__ ), "gui_makefile.glade" )
GLADE_FILE_PROCESS = os.path.join( os.path.dirname( __file__ ), "gui_process.glade" )
GLADE_FILE_RUNNING = os.path.join( os.path.dirname( __file__ ), "gui_running.glade" )

IMG_COMP = os.path.join( os.path.dirname( __file__ ), "imgs", "iconComp.png" )
IMG_SAVE = os.path.join( os.path.dirname( __file__ ), "imgs", "iconSave.png" )
IMG_TERM = os.path.join( os.path.dirname( __file__ ), "imgs", "iconTerm.png" )
IMG_PYTHON = os.path.join( os.path.dirname( __file__ ), "imgs", "iconPython.png" )
IMG_GEDIT = os.path.join( os.path.dirname( __file__ ), "imgs", "iconGedit.png" )
IMG_MAKE = os.path.join( os.path.dirname( __file__ ), "imgs", "iconMake.png" )
IMG_PYTHON_BIG = os.path.join( os.path.dirname( __file__ ), "imgs", "iconPythonBig.png" )

# opcao default: mostra console
checked_show_terminal = True

