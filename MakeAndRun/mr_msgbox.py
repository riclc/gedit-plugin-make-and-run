#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import gtk


def msgbox(titulo_window, texto, tipo = 'info'):

    if tipo == 'error':
        gtipo = gtk.MESSAGE_ERROR
        gb = gtk.BUTTONS_OK
    elif tipo == 'warning':
        gtipo = gtk.MESSAGE_ERROR
        gb = gtk.BUTTONS_OK
    elif tipo == 'question':
        gtipo = gtk.MESSAGE_WARNING
        gb = gtk.BUTTONS_YES_NO
    else: # info
        gtipo = gtk.MESSAGE_INFO
        gb = gtk.BUTTONS_OK

    dlg = gtk.MessageDialog( type = gtipo, buttons = gb )
    dlg.set_title( titulo_window )
    dlg.set_markup( texto )

    r = dlg.run()
    dlg.destroy()

    if r == gtk.RESPONSE_OK or r == gtk.RESPONSE_YES:
        return True
    else: # r == gtk.RESPONSE_DELETE_EVENT or r == GTK.RESPONSE_NO
        return False





def _msgbox_teste():

    print msgbox( "ola 1", "texto info", 'info' )
    print msgbox( "ola 2", "texto error", 'error' )
    print msgbox( "ola 3", "texto warning", 'warning' )
    print msgbox( "ola 4", "texto question", 'question' )


if __name__ == '__main__':
    _msgbox_teste()
