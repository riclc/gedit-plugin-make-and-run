#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os 
import os.path


from mr_msgbox import *
from mr_globals import *


def roda_cmd(cmd):
    
    # quando executamos algo tipo 'make &', o processo nao interrompe
    # o gedit, e retorna 0 como resposta. eh assincrono.

    if configurations.show_terminal:    
        os.system(
            "gnome-terminal --execute bash -c '" +
            cmd +
            " && " +
            "echo && echo \"Aperte Enter para finalizar\"" +
            " && " +
            "read' &"
        )
    else:
        os.system( cmd + " &" )
    



def roda_cmd_on_dir(cmd, on_dir):
    os.chdir( on_dir )
    roda_cmd( cmd )



