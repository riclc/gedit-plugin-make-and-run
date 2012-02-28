#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

from gi.repository import GObject, Gtk


def msgbox(titulo_window, texto, tipo = 'info'):

    if tipo == 'error':
        gtipo = Gtk.MessageType.ERROR
        gb = Gtk.ButtonsType.OK
    elif tipo == 'warning':
        gtipo = Gtk.MessageType.WARNING
        gb = Gtk.ButtonsType.OK
    elif tipo == 'question':
        gtipo = Gtk.MessageType.QUESTION
        gb = Gtk.ButtonsType.YES_NO
    else: # info
        gtipo = Gtk.MessageType.INFO
        gb = Gtk.ButtonsType.OK

    dlg = Gtk.MessageDialog( type = gtipo, buttons = gb )
    dlg.set_title( titulo_window )
    dlg.set_markup( texto )

    r = dlg.run()
    dlg.destroy()

    if r == Gtk.ResponseType.OK or r == Gtk.ResponseType.YES:
        return True
    else: # r == Gtk.ResponseType.DELETE_EVENT or r == Gtk.ResponseType.NO
        return False





def _msgbox_teste():

    print msgbox( "ola 1", "texto info", 'info' )
    print msgbox( "ola 2", "texto error", 'error' )
    print msgbox( "ola 3", "texto warning", 'warning' )
    print msgbox( "ola 4", "texto question", 'question' )


if __name__ == '__main__':
    _msgbox_teste()
