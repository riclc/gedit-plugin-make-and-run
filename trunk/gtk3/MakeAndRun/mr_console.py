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


def roda_cmd(cmd, auto_close = False):
    
    # quando executamos algo tipo 'make &', o processo nao interrompe
    # o gedit, e retorna 0 como resposta. eh assincrono.
    
    if configurations.show_terminal:    
        if auto_close:
            full_cmd = \
                "gnome-terminal --execute bash -c '" + cmd + " && "     + \
                "echo && clear ' &"
        else:
            console_exec = os.path.join( os.path.dirname(__file__), "mr_console_exec.py" )
            full_cmd = "gnome-terminal --execute python %s %s  &" % (console_exec, cmd)
            
    else:
        full_cmd = cmd + " &"
    
    #print "Command: '%s'" % full_cmd
    os.system( full_cmd )
    



def roda_cmd_on_dir(cmd, on_dir, auto_close = False):
    os.chdir( on_dir )
    roda_cmd( cmd, auto_close )


