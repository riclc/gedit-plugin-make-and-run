#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys


def print_color(s, c):
    print ("\033[%dm" % c) + s + "\033[0m"


def main():

    if len(sys.argv) > 1:
        s = " ".join( sys.argv[1:] )
        print_color( "Executando %s..." % s, 93 )
        print
        os.system( s )

    print
    print_color( "Aperte Enter para finalizar", 91 )
    raw_input()

main()
