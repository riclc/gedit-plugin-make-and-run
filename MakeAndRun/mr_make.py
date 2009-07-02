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
from mr_console import *
from mr_processo import *



makefile_cpp = """
OBJETOS = $(FONTES:.cpp=.o)
COMPILADOR = g++

all: $(FONTES) $(PROGRAMA)

$(PROGRAMA): $(OBJETOS)
    $(COMPILADOR) $(LDFLAGS) $(OBJETOS) -o $@

.cpp.o:
    $(COMPILADOR) $(CFLAGS) $< -o $@

clean:
    rm -rfv *.o $(PROGRAMA)

exec:
    ./$(PROGRAMA)
"""        


makefile_c = """
OBJETOS = $(FONTES:.c=.o)
COMPILADOR = gcc

all: $(FONTES) $(PROGRAMA)

$(PROGRAMA): $(OBJETOS)
    $(COMPILADOR) $(LDFLAGS) $(OBJETOS) -o $@

.c.o:
    $(COMPILADOR) $(CFLAGS) $< -o $@

clean:
    rm -rfv *.o $(PROGRAMA)

exec:
    ./$(PROGRAMA)
"""





class MakefileManager:

    def __init__(self, src):
        
        self.src = src

        
    def makefile_from_src(self):

        makefile = os.path.join( self.src.get_dir(), "Makefile" )
        return makefile


    def makefile_exists(self):

        makefile = self.makefile_from_src()
        return os.path.exists( makefile )
    

    def make_build(self, mrplugin):

        self.mrplugin = mrplugin
        
        if self.makefile_exists():
            self.makefile_run()
        else:
            self.show_dlg_makefile()
    
    
    
    def makefile_run(self):
        
        p = CmdProcess()
        p.run_cmd_on_dir( "make", self.src.get_dir() )

        p.mostra_erros( self.mrplugin )
        

    
    def show_dlg_makefile(self):

        global GLADE_FILE_MAKEFILE
    
        builder = gtk.Builder()
        builder.add_from_file( GLADE_FILE_MAKEFILE )
    
        self.windowMakefile = builder.get_object( "windowMakefile" )
        self.textPrograma = builder.get_object( "textPrograma" )
        self.btnOK = builder.get_object( "btnOK" )
        self.btnCancelar = builder.get_object( "btnCancelar" )
        self.btnAdiciona = builder.get_object( "btnAdiciona" )
        self.btnRemove = builder.get_object( "btnRemove" )
        self.listArquivos1 = builder.get_object( "listArquivos1" )
        self.listArquivos2 = builder.get_object( "listArquivos2" )
        self.storeArquivos1 = builder.get_object( "storeArquivos1" )
        self.storeArquivos2 = builder.get_object( "storeArquivos2" )
        self.checkWall = builder.get_object( "checkWall" )
        self.checkO2 = builder.get_object( "checkO2" )
        self.checkMath = builder.get_object( "checkMath" )
        self.checkOpenGL = builder.get_object( "checkOpenGL" )
        self.checkX11 = builder.get_object( "checkX11" )
        self.textLibs = builder.get_object( "textLibs" )
        
        # ajeita a figura
        #
        self.imgMake = builder.get_object( "imgMake" )
        self.imgMake.set_from_file( IMG_MAKE )
        #
        ##

        # configura as listas de arquivos
        #    
        renderer = gtk.CellRendererText()
        coluna = gtk.TreeViewColumn( "Arquivo", renderer, text=0 )    
        self.listArquivos1.append_column( coluna )

        coluna = gtk.TreeViewColumn( "Arquivo", renderer, text=0 )    
        self.listArquivos2.append_column( coluna )
        #
        ####

        self.btnOK.connect( "clicked", self.on_dlg_makefile_ok )
        self.btnCancelar.connect( "clicked", self.on_dlg_makefile_cancel )
        self.windowMakefile.connect( "delete-event", self.on_dlg_makefile_cancel )
        self.btnAdiciona.connect( "clicked", self.on_dlg_makefile_add )
        self.btnRemove.connect( "clicked", self.on_dlg_makefile_del )

        # tenta adivinhar o nome do projeto com base no codigo atual
        #
        arq = self.src.get_arq()
        arq_sem_dir = os.path.basename(arq)
        arq_nome_sem_ext, arq_ext = os.path.splitext( arq_sem_dir )
        
        self.textPrograma.set_text( arq_nome_sem_ext.lower() )
        
        
        # filtra os arquivos do diretorio e poe na lista de arquivos 2
        #
        self.usando_c = arq_ext.lower() == '.c'
        
        fontes = self.makefile_get_fontes( arq_ext )
        
        for f in fontes:
        
            # ja deixa o arquivo atual na lista de arquivos 1, claro.
            if f == arq_sem_dir:
                it = self.storeArquivos1.append()
                self.storeArquivos1.set( it, 0, f )
            else:
                it = self.storeArquivos2.append()
                self.storeArquivos2.set( it, 0, f )
        
        #
        #
        ###########
    
        self.windowMakefile.show()
        gtk.main()


    def on_dlg_makefile_ok(self, *args):

        # pega os arquivos marcados pro makefile        
        self.fontes_marcados = self.makefile_get_fontes_from_dlg()

        # pega os parametros de cflags
        #
        self.use_cflags = "-c -pipe"
        if self.checkWall.get_active():
            self.use_cflags += " -Wall "
        if self.checkO2.get_active():
            self.use_cflags += " -O2 "

        # pega os parametros de ldflags
        #        
        self.use_ldflags = ""
        if self.checkMath.get_active():
            self.use_ldflags += " -lm "
        if self.checkOpenGL.get_active():
            self.use_ldflags += " -lglut -lGL -lGLU "
        if self.checkX11.get_active():
            self.use_ldflags += " -lXmu -lXi -lXext -lX11 "
        self.use_ldflags += " " + self.textLibs.get_text()
            
        
        # fecha a janela
        #
        self.windowMakefile.destroy()
        gtk.main_quit()
        
        # gera um Makefile conforme os dados da janela
        #
        self.makefile_generate()
        
        # roda com o Makefile gerado!
        #
        self.makefile_run()


        
    def on_dlg_makefile_cancel(self, *args):

        self.windowMakefile.destroy()
        gtk.main_quit()


    def on_dlg_makefile_add(self, *args):
        
        # pega o item atualmente selecionado em 'arquivos 2' e o remove
        treeView, it = self.listArquivos2.get_selection().get_selected()
        if it == None:
            return
            
        arq = self.storeArquivos2.get_value( it, 0 )
        self.storeArquivos2.remove( it )

        # adiciona em 'arquivos 1'
        it = self.storeArquivos1.append()
        self.storeArquivos1.set_value( it, 0, arq )


    def on_dlg_makefile_del(self, *args):

        # pega o item atualmente selecionado em 'arquivos 1' e o remove
        treeView, it = self.listArquivos1.get_selection().get_selected()
        if it == None:
            return

        arq = self.storeArquivos1.get_value( it, 0 )
        self.storeArquivos1.remove( it )

        # adiciona em 'arquivos 2'
        it = self.storeArquivos2.append()
        self.storeArquivos2.set_value( it, 0, arq )
    
    
    def makefile_generate(self):

        makefile = self.makefile_from_src()
        mdir = self.src.get_dir()
    
        prog = self.textPrograma.get_text()
    
        f = open( makefile, "w" )
        f.write( "PROGRAMA = " + prog + "\n" )
        f.write( "FONTES = " + self.fontes_marcados + "\n" )
        
        f.write( "\n" )
        f.write( "CFLAGS = " + self.use_cflags + "\n" )
        f.write( "LDFLAGS = " + self.use_ldflags + "\n" )
        f.write( "\n" )
    
        if self.usando_c:
            f.write( makefile_c )
        else:
            f.write( makefile_cpp )
    
        f.close()



    def makefile_get_fontes(self, ext = ".c"):
        
        self.src.muda_pro_diretorio_do_arquivo()
    
        lfontes = glob( "./*" + ext )

        fontes = []    
        for f in lfontes:
            fontes.append( f.replace("./", "") )
            
        return fontes

        
    def makefile_get_fontes_from_dlg(self):
    
        arqs = ""
        
        it = self.storeArquivos1.get_iter_first()
        while it != None:
            arq = self.storeArquivos1.get_value( it, 0 )            
            arqs = arqs + arq + " "
            
            it = self.storeArquivos1.iter_next( it )
            
        return arqs



    def make_exec(self):
    
        # descobre o comando de 'make exec' que deve-se fazer pra
        # rodar o projeto (c / c++)
        #

        makeExecTarget = self.src.pluginManager.textMakeExec.get_text() 
                
        if makeExecTarget == '':
            makeExecTarget = "exec"
            return
        
        cmd = "make " + makeExecTarget


        # o arquivo makefile existe?
        
        if self.makefile_exists():
            roda_cmd_on_dir( cmd, self.src.get_dir() )
            return
            
        
        # o arquivo makefile nao existe...

        msgbox(
            "Rodar Programa",
            "Não foi encontrado um arquivo de Makefile no diretório.\n" +
            "Por causa disso, não é possível rodar o código atual.",
            "erro"
        )



    def make_clean(self):
    
        # o arquivo makefile existe?
        
        if self.makefile_exists():

            p = CmdProcess()
            p.run_cmd_on_dir( "make clean", self.src.get_dir() )

            #roda_cmd_on_dir( "make clean", self.src.get_dir() )
            return
            
        
        # o arquivo makefile nao existe...

        msgbox(
            "Make Clean",
            "Não foi encontrado um arquivo de Makefile no diretório.\n" +
            "Por causa disso, não é possível executar <i>make clean</i>.",
            "erro"
        )

