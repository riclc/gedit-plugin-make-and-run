#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import os
import os.path
import signal

import gtk
import gobject
import pango
from subprocess import *
import fcntl

from mr_globals import *
from mr_msgbox import *
from mr_processo import *


class PythonRun:

    def __init__(self):

        self.processo = None
        self.finished = False
        self.killed = False
        self.arq = ""
        self.pluginManager = None

        builder = gtk.Builder()
        builder.add_from_file( GLADE_FILE_RUNNING )

        self.windowRunning = builder.get_object( "windowRunning" )
        self.btnCancel = builder.get_object( "btnCancel" )
        self.btnClose = builder.get_object( "btnClose" )
        self.labelMsg1 = builder.get_object( "labelMsg1" )
        self.labelMsg2 = builder.get_object( "labelMsg2" )
        self.imgExec = builder.get_object( "imgExec" )

        self.areaStdout = builder.get_object( "areaStdout" )
        self.textOutput = builder.get_object( "textOutput" )
        self.bufferOutput = builder.get_object( "bufferOutput" )

        self.areaStderr = builder.get_object( "areaStderr" )
        self.textErr = builder.get_object( "textErr" )
        self.bufferErr = builder.get_object( "bufferErr" )

        self.imgExec.set_from_file( IMG_PYTHON_BIG )

        self.textErr.modify_text( \
            gtk.STATE_NORMAL, gtk.gdk.color_parse('#880000') )

        self.textOutput.modify_font( \
            pango.FontDescription( "Monospace 8" ) )
        self.textErr.modify_font( \
            pango.FontDescription( "Monospace Bold 8" ) )

        self.btnCancel.connect( "clicked", self.on_cancel )
        self.btnClose.connect( "clicked", self.on_close )
        self.windowRunning.connect( "delete-event", self.on_window_close )
        self.windowRunning.connect( "focus-in-event", self.on_window_focus_in )
        self.windowRunning.connect( "focus-out-event", self.on_window_focus_out )

        self.timeout_id = -1
        self.timeout_counter = 10


    def from_file(self, src):

        # supoe que ja foi pro diretorio do arquivo.

        self.pluginManager = src.pluginManager
        self.arq = src.get_filename()

        self.processo = Popen(
            args = ["python", "-u", self.arq],
            stdout = PIPE,
            stderr = PIPE
        )

        self.windowRunning.show()
        self.windowRunning.set_focus( self.btnCancel )

        self.wait_finish()


    def file_desbloqueia(self, fd):
        flags = fcntl.fcntl( fd, fcntl.F_GETFL )
        fcntl.fcntl( fd, fcntl.F_SETFL, flags | os.O_NONBLOCK )



    def gtk_do(self):
        while gtk.events_pending():
            gtk.main_iteration( block=False )


    def processo_feedback(self):

        stdout_ok = False
        stderr_ok = False

        try:
            msg1 = self.processo.stdout.readline()
        except IOError, ioerr:
            msg1 = ''

        if msg1 <> '':
            stdout_ok = True
            self.bufferOutput.insert( self.bufferOutput.get_end_iter(), msg1 )

        try:
            msg2 = self.processo.stderr.readline()
        except IOError, ioerr:
            msg2 = ''

        if msg2 <> '':
            stderr_ok = True
            self.bufferErr.insert( self.bufferErr.get_end_iter(), msg2 )


        self.gtk_do()
        return stdout_ok, stderr_ok



    def wait_finish(self):

        self.finished = False

        self.file_desbloqueia( self.processo.stdout.fileno() )
        self.file_desbloqueia( self.processo.stderr.fileno() )

        stdout_vazio = True
        stderr_vazio = True

        while not self.finished:

            stdout_ok, stderr_ok = self.processo_feedback()

            if stdout_ok: stdout_vazio = False
            if stderr_ok: stderr_vazio = False

            if self.processo.poll() != None:
                self.finished = True


        # terminou o processo, tenta ver se ainda tem coisa pra ler.
        # varias vezes ainda tem.
        while True:
            stdout_ok, stderr_ok = self.processo_feedback()
            if stdout_ok == stderr_ok == False:
                break

            if stdout_ok: stdout_vazio = False
            if stderr_ok: stderr_vazio = False


        err = self.processo.returncode != 0

        if err:

            # deixa em vermelho
            self.labelMsg1.set_markup( \
                "<big><big><b><span foreground='red'>" + \
                "Execução Finalizada" + \
                "</span></b></big></big>" )

            if stdout_vazio and stderr_vazio:
                self.labelMsg2.set_text( \
                    "O programa retornou " + \
                    str(self.processo.returncode) + \
                    ", mas não gerou nenhuma saída." )
            else:
                self.labelMsg2.set_text( \
                    "Verifique a saída gerada pelo programa." )

            if stdout_vazio:
                self.areaStdout.hide()

            if stderr_vazio:
                self.areaStderr.hide()

        else:
            if configurations.run_python_auto_close_window:
                self.windowRunning.destroy()
                return

            # deixa em azul
            self.labelMsg1.set_markup( \
                "<big><big><b><span foreground='blue'>" + \
                "Execução Finalizada" + \
                "</span></b></big></big>" )

            self.labelMsg2.set_text( "" )


        self.btnCancel.hide()
        self.btnClose.show()
        self.windowRunning.set_focus( self.btnClose )
        self.gtk_do()



    def on_cancel(self, *args):

        self.btnCancel.hide()
        print( "Kill: enviando SIGTERM para pid " + str(self.processo.pid) )
        os.kill( self.processo.pid, signal.SIGTERM )


    def on_close(self, *args):

        self.windowRunning.destroy()


    def on_window_close(self, *args):

        if self.btnCancel.get_property("visible"):
            # atua como se fosse um cancel
            self.on_cancel()

        elif self.btnClose.get_property("visible"):
            # atua como se fosse um close
            self.on_close()

        # caso contrario, nao faz nada.
        return True


    def on_window_focus_in(self, widget, event, *args):
        if not configurations.run_python_auto_close_window_by_time:
            return

        if self.timeout_id != -1:
            gobject.source_remove( self.timeout_id )
            self.timeout_id = -1
            self.windowRunning.set_title( "Execução do Programa" )


    def on_window_focus_out(self, widget, event, *args):
        if not configurations.run_python_auto_close_window_by_time:
            return

        if self.timeout_id == -1:
            self.timeout_counter = 10
            self.timeout_id = gobject.timeout_add( 1000, self.no_more_used )


    def no_more_used(self):
        if not configurations.run_python_auto_close_window_by_time:
            return

        if self.timeout_id == -1:
            return

        if not self.finished:
            return

        self.windowRunning.set_title( \
            "Execução do Programa [%d]" % self.timeout_counter )

        self.timeout_counter -= 1
        if self.timeout_counter < 0:
            self.on_close()
            return False
        else:
            return True
