#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

from gi.repository import GObject, Gedit, Gtk, Gdk


class DocError:
    def __init__(self, mr, doc, view):
        self.mr = mr
        self.doc = doc
        self.view = view

        self.error_tag = self.doc.create_tag()
        self.error_tag.set_property(
            "paragraph-background-gdk",
            Gdk.Color.parse( "#dd0000" )[1]
        )
        
        self.mr.doc_errors.append( self )

    
    def mark_error(self, line):
        if self.doc == None:
            return
            
        lin_ini = self.doc.get_iter_at_line( line )
        lin_end = self.doc.get_iter_at_line( line )
        lin_end.forward_to_line_end()

        self.doc.apply_tag( self.error_tag, lin_ini, lin_end )
        
        self.doc.goto_line( line )
        self.view.scroll_to_cursor()
    
    
    def remove_error(self):
        if self.doc == None:
            return
            
        a, b = self.doc.get_bounds()
        self.doc.remove_tag( self.error_tag, a, b )

