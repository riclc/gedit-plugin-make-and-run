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
from glob import *

from mr_globals import *
from mr_msgbox import *
from mr_source_file import *
from mr_processo import *



class CompileSource:

    def __init__(self, src):

        self.src = src


        # vamos compilar com qual compilador? gcc / g++ / etc?
        #

        if self.src.get_lang() == "":
            return

        cmdC = configurations.compile_c
        cmdCpp = configurations.compile_cpp
        cmdPython = configurations.compile_python

        if self.src.is_lang_c():
            cmd = cmdC
        elif self.src.is_lang_cpp():
            cmd = cmdCpp
        elif self.src.is_lang_python():
            cmd = cmdPython
        else:
            msgbox( "Compilar", "Não há suporte para o arquivo atual." )
            return

        self.run_compiler( cmd )



    def run_compiler(self, cmd):

        arq = os.path.basename( self.src.get_filename() )

        p = CmdProcess()
        p.run_cmd_on_dir( cmd + " " + arq, self.src.get_dir() )

        self.erros = p.erros_gcc
        self.compilou_ok = p.return_code == 0

        self.compiler_process = p
