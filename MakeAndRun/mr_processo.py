#!/usr/bin/env python
# coding: utf-8
#
# Make-and-Run
# by Ricardo Lenz (riclc@hotmail.com)
#
# see README file

import gtk
import gobject
import glib

import os
import os.path
#import fcntl
import time
from subprocess import *
import thread

from mr_msgbox import *
from mr_globals import *
from mr_find_file_from_error import *


class ErroGCC:

    def __init__(self):

        self.arquivo = ""
        self.linha = -1
        self.msg = ""



class CmdProcess():

    def __init__(self):

        builder = gtk.Builder()
        builder.add_from_file( GLADE_FILE_PROCESS )

        self.windowProc = builder.get_object( "windowProc" )
        self.labelCmd = builder.get_object( "labelCmd" )
        self.labelDir = builder.get_object( "labelDir" )
        self.progressBar = builder.get_object( "progressBar" )
        self.areaConclusao = builder.get_object( "areaConclusao" )
        self.btnClose = builder.get_object( "btnClose" )
        self.labelErros = builder.get_object( "labelErros" )
        self.textOutput = builder.get_object( "textOutput" )
        self.bufferOutput = builder.get_object( "bufferOutput" )
        self.scrollOutput = builder.get_object( "scrollOutput" )
        self.labelReturnCode = builder.get_object( "labelReturnCode" )
        self.labelReturnCode2 = builder.get_object( "labelReturnCode2" )
        self.imgResult = builder.get_object( "imgResult" )
        self.labelConcluded = builder.get_object( "labelConcluded" )

        self.return_code = -1
        self.erros_gcc = []
        self.processo = None
        self.processo_terminou = False

        self.outputIter = self.bufferOutput.get_start_iter()

        self.tag_fonte1 = self.bufferOutput.create_tag()
        self.tag_fonte1.set_property( "font", "Monospace 8" )
        self.tag_fonte2 = self.bufferOutput.create_tag()
        self.tag_fonte2.set_property( "font", "Monospace 8" )
        self.tag_fonte2.set_property( "foreground", "#ee0000" )


        self.btnClose.connect( "clicked", self.on_btnClose )


    def run_cmd_on_dir(self, cmd, on_dir):

        self.labelCmd.set_markup( "<i><small>" + cmd + "</small></i>" )
        self.labelDir.set_markup( "<i><small>" + on_dir + "</small></i>" )

        os.chdir( on_dir )

        try:
            self.processo = Popen(
                shell=True,
                args = cmd,
                stdout=PIPE,
                stderr=STDOUT
            )
        except:
            msgbox( "Erro de execução",
                "Erro ao executar <i>" + cmd + "</i>.", "erro" )

        self.erros_gcc = []
        self.return_code = -1
        self.cmd_executado = cmd

        self.windowProc.show()
        
        # dispara uma thread para cuidar do output do processo
        self.processo_terminou = False
        thread.start_new_thread( self.processo_thread, () )
        
        # vamos ficar, aqui, por enquanto, num looping, processando a nossa GUI
        #
        while not self.processo_terminou: 
            self.progressBar.pulse()

            # roda tb o thread dos signals do gtk/x11
            #
            while gtk.events_pending():
                gtk.main_iteration(False)

            # espera um tempinho (senao a animacao da barra de progresso
            # fica MUITO rapida). esse tempinho eh simplesmente uma suspensao
            # temporaria do nosso proprio programa (bem leve)
            #
            time.sleep( 0.05 )



    def on_btnClose(self, *args):

        # supoe que o processo ja terminou.

        self.windowProc.destroy()

        #gtk.main_quit()


    def processo_thread(self):

        # seta a flag "unblock" do descritor do arquivo,
        # usando a chamada fcntl do sistema operacional.
        #
        #fcntl.fcntl( self.processo.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK )
        #
        # UPDATE: não fazemos mais isso. vamos simplesmente ler num thread à parte,
        # então quando dá bloqueio, o thread à parte é que fica bloqueado.
        #
        ####

        while True:
            if not self.processando():
                break
        
        self.processo_terminou = True



    def processando(self, *args):

        try:
            # o metodo readline() ficaria esperando ate
            # receber o input (blocking). entao isso nao
            # adianta pra gente, pois queremos ser assincronos
            # aqui. por isso, configuramos anteriormente pra
            # ficar unblocking o file indicado por stdout.
            # nesse caso, a leitura do processo (quando ainda
            # nao tem nada pra ler) gera o ioerror 11.
            #
            # UPDATE: agora, contudo, estamos num thread à parte do
            # resto do programa, então fazemos readline() blocante.
            #
            msg = self.processo.stdout.readline()
            
        except IOError, ioerr:

            # Errno: 11 -> "Resource temporarily unavailable"
            #if ioerr.errno == 11:

            msg = ''



        if msg == '':
            if self.processo.poll() != None:

                # terminou o processo agora.
                #

                self.return_code = self.processo.returncode

                num = len( self.erros_gcc )
                if num > 0:
                    snum = "<span foreground='red'>" + str(num) + "</span>"
                else:
                    snum = str(num)

                self.labelErros.set_markup( "<small><b>" + snum + "</b></small>" )


                scode = str(self.return_code)
                if self.return_code == 0:
                    scode2 = "<span foreground='blue'>" + scode + "</span>"
                else:
                    scode2 = scode

                self.labelReturnCode.set_markup( "<small><b>" + \
                    scode2 + "</b></small>" )

                self.labelReturnCode.set_sensitive( True )
                self.labelReturnCode2.set_sensitive( True )


                self.progressBar.set_fraction( 1.0 )
                self.windowProc.set_title( "Concluído" )

                self.areaConclusao.show()
                self.windowProc.set_focus( self.btnClose )

                # terminou, nao precisa mais ficar processando.
                return False

            else:
                return True


        eg = self.erro_gcc_from_str( msg )
        if eg.linha == -1:

            # nao eh uma mensagem tipica de erro do gcc.
            self.adiciona_log( msg, cor_erro = False )

            return True


        # eh uma mensagem de erro valida do gcc!
        #

        self.erros_gcc.append( eg )
        self.adiciona_log( msg, cor_erro = True )


        # continua rodando de novo
        return True



    def adiciona_log(self, msg, cor_erro):

        if not cor_erro:
            self.bufferOutput.insert_with_tags( \
                self.outputIter, msg, self.tag_fonte1 )
        else:
            self.bufferOutput.insert_with_tags( \
                self.outputIter, msg, self.tag_fonte2 )

        v = self.scrollOutput.get_vadjustment()
        v.set_value( v.upper )

        #final = self.bufferOutput.get_end_iter()
        #self.textOutput.scroll_to_iter( final, 0.0 )

        # processa para que o texto/scroll sejam feitos adequadamente na gui.
        while gtk.events_pending():
            gtk.main_iteration(False)



    def erro_gcc_from_str(self, s):

        eg = ErroGCC()

        eg.arquivo = s[ : s.find(":") ]
        resto = s[ s.find(":")+1 : ]

        s_linha = resto[ : resto.find(":") ]
        resto = resto[ resto.find(":") + 1 : ]

        eg.msg = resto.strip()

        try:
            eg.linha = int( s_linha )
        except:
            eg.linha = -1

        return eg



    def mostra_erros(self, mr_plugin):

        src = mr_plugin.src
        window = mr_plugin.window
        bottom = window.get_bottom_panel()
        storeOutput = mr_plugin.storeOutput

        # limpa as marcas de erros atuais
        #
        src.remove_error()
        storeOutput.clear()

        # deu certo a compilacao/build/make?
        #

        deu_certo = self.return_code == 0
        num_msgs = len( self.erros_gcc )

        if deu_certo and num_msgs > 0 and configurations.show_warnings:
            s_msgs = "mensagens" if num_msgs > 1 else "mensagem"

            self.on_btnClose()
            
            if msgbox( "Compilado com possíveis erros",
                "<big><b>O arquivo foi compilado com sucesso</b></big>\n\n" +
                "Porém, o compilador gerou <b>" + str(num_msgs) + "</b> " +
                s_msgs + ",\n" +
                "provavelmente em relação a possíveis bugs.\n\n" +
                "Você deseja exibir " + ("essas" if num_msgs > 1 else "essa") +
                " " + s_msgs + "?",
                "question" ):
                    
                    deu_certo = False
                    
        else:
            if num_msgs == 0 and self.return_code != 2:

                # apesar de nao ter dado return_code = 0, mas se nao
                # tivemos nenhuma mensagem de erro do gcc, entao
                # supoe que ta tranquilo. ja observei que isso de fato
                # acontece em alguns make's com qt, por ex.
                #
                deu_certo = True


        if deu_certo:

            bottom.hide()

            status_msg = "Compilado com sucesso!"
            window.get_statusbar().flash_message( 0, status_msg )

            if configurations.make_auto_close_window:
                self.imgResult.set_from_file( IMG_RESULT_OK )
                self.imgResult.show()
                self.start_auto_close()

        else:

            status_msg = "Projeto com erros"
            window.get_statusbar().flash_message( 0, status_msg )


            
            # conseguimos fazer o parsing de um ou mais erros do gcc?
            #
            if len( self.erros_gcc ) > 0:
                
                for erro_gcc in self.erros_gcc:
                    it = storeOutput.append()
                    storeOutput.set( it, 0, erro_gcc.arquivo )
                    storeOutput.set( it, 1, erro_gcc.linha )
                    storeOutput.set( it, 2, erro_gcc.msg )

                # manda sumir essa janela para o programador se concentrar na
                # lista de erros mostrada no painel inferior.
                #
                if configurations.make_auto_close_window:
                    self.imgResult.set_from_file( IMG_RESULT_ERROR )
                    self.imgResult.show()
                    self.start_auto_close()

            
                # painel inferior - define tamanho e depois mostra
                #
                
                if not configurations.bottom_panel_size_ignore:

                    tam = int( configurations.bottom_panel_size )
                    vpan = bottom.get_parent()
                    vpan.set_position( vpan.allocation.height - tam )

                bottom.show()
                bottom.activate_item( mr_plugin.area )

                # marca o primeiro erro (caso seja o mesmo arquivo atual)
                #
                it = mr_plugin.storeOutput.get_iter_first()
                find_file_from_error( mr_plugin, it, can_msgbox = False )

            
            else:
                
                self.labelConcluded.set_markup( \
                    "<small>Comando concluído com <b>problemas</b>. " + \
                    "Verifique o log!</small>" )

            



    

    def start_auto_close(self):
        
        glib.timeout_add( 750, self.on_auto_close_animation_timer )
    
        
    def on_auto_close_animation_timer(self):

        self.on_btnClose()
        return False

