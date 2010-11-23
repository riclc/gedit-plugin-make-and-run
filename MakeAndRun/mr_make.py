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



makefile_1_c = """
OBJETOS = $(FONTES:.c=.o)
COMPILADOR = gcc
"""

makefile_1_cpp = """
OBJETOS = $(FONTES:.cpp=.o)
COMPILADOR = g++
"""


makefile_1_c_mpi = """
NUM_OF_P = 2

OBJETOS = $(FONTES:.c=.o)
COMPILADOR = mpicc
"""

makefile_1_cpp_mpi = """
NUM_OF_P = 2

OBJETOS = $(FONTES:.cpp=.o)
COMPILADOR = mpic++
"""


makefile_2_common = """
all: $(FONTES) $(PROGRAMA)

$(PROGRAMA): $(OBJETOS)
\t$(COMPILADOR) $(OBJETOS) $(LDFLAGS) -o $@
"""

makefile_3_c = """
.c.o:"""

makefile_3_cpp = """
.cpp.o:"""

    
makefile_4_common = """
\t$(COMPILADOR) $(CFLAGS) $< -o $@

clean:
\trm -rfv *.o $(PROGRAMA) 
"""


makefile_5_default = """
exec:
\t./$(PROGRAMA)
"""

makefile_5_mpi = """
exec:
\tmpirun -n $(NUM_OF_P) $(PROGRAMA)
"""


makefile_6_profiling = """
profile: exec	
\tgprof $(PROGRAMA) | gprof2dot.py | dot -Tpng -o gprof_profile.png
\teog gprof_profile.png
"""






class MakefileManager:

    def __init__(self, src):

        self.src = src


    def makefile_candidates_from_src(self):

	    arqs = [ "Makefile", "makefile" ]
	    for i in range( len(arqs) ):
		    arqs[i] = os.path.join( self.src.get_dir(), arqs[i] )
		
            return arqs


    def default_makefile_from_src(self):

    	return self.makefile_candidates_from_src()[0]


    def any_makefile_exists(self):

	    arqs = self.makefile_candidates_from_src()
	    for arq in arqs:
		    if os.path.exists( arq ):
			    return True
	
	    return False


    def get_makefile_contents(self):

        arqs = self.makefile_candidates_from_src()
        for arq in arqs:
            if os.path.exists( arq ):
                f = open( arq, "r" )
                lines = f.readlines()
                f.close()
                return lines

        return []



    def make_build(self, mrplugin, rebuilding):

        self.mrplugin = mrplugin

        if self.any_makefile_exists():
            self.makefile_run( rebuilding )
        else:
            self.show_dlg_makefile()



    def makefile_run(self, rebuilding):

        if rebuilding:
            cmd = "make clean && make"
        else:
            cmd = "make"
            
        p = CmdProcess()
        p.run_cmd_on_dir( cmd, self.src.get_dir() )
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
        self.btnAdicionaTodos = builder.get_object( "btnAdicionaTodos" )
        self.btnRemoveTodos = builder.get_object( "btnRemoveTodos" )
        self.listArquivos1 = builder.get_object( "listArquivos1" )
        self.listArquivos2 = builder.get_object( "listArquivos2" )
        self.storeArquivos1 = builder.get_object( "storeArquivos1" )
        self.storeArquivos2 = builder.get_object( "storeArquivos2" )
        
        self.checkWall = builder.get_object( "checkWall" )
        self.checkO2 = builder.get_object( "checkO2" )
        self.checkMath = builder.get_object( "checkMath" )
        self.checkOpenGL = builder.get_object( "checkOpenGL" )
        self.checkGLEW = builder.get_object( "checkGLEW" )
        self.checkX11 = builder.get_object( "checkX11" )
        self.checkOpenMP = builder.get_object( "checkOpenMP" )
        self.checkOpenMPI = builder.get_object( "checkOpenMPI" )
        self.checkDebug = builder.get_object( "checkDebug" )
        self.checkProfiling = builder.get_object( "checkProfiling" )
        self.checkGTK = builder.get_object( "checkGTK" )
        self.textLDFLAGS = builder.get_object( "textLDFLAGS" )
        self.textCFLAGS = builder.get_object( "textCFLAGS" )


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

        self.windowMakefile.connect( "delete-event", self.on_dlg_makefile_cancel )
        self.btnOK.connect( "clicked", self.on_dlg_makefile_ok )
        self.btnCancelar.connect( "clicked", self.on_dlg_makefile_cancel )
        self.btnAdiciona.connect( "clicked", self.on_dlg_makefile_add )
        self.btnRemove.connect( "clicked", self.on_dlg_makefile_del )
        self.btnAdicionaTodos.connect( "clicked", self.on_dlg_makefile_add_all )
        self.btnRemoveTodos.connect( "clicked", self.on_dlg_makefile_del_all )

        # tenta adivinhar o nome do projeto com base no codigo atual
        #
        self.textPrograma.set_text( self.src.get_filename_without_path_and_ext().lower() )


        # filtra os arquivos do diretorio e poe na lista de arquivos 2
        #
        self.usando_c = self.src.get_filename_ext().lower() == '.c'

        self.fontes = self.makefile_get_fontes( self.src.get_filename_ext() )

        for f in self.fontes:

            # ja deixa o arquivo atual na lista de arquivos 1, claro.
            if f == self.src.get_filename_without_path():
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
        if self.checkOpenMP.get_active():
            self.use_cflags += " -fopenmp"      # em LDFLAGS tambem
        if self.checkDebug.get_active():
            self.use_cflags += " -g"
        if self.checkProfiling.get_active():
            self.use_cflags += " -pg"           # em LDFLAGS tambem
        if self.checkGTK.get_active():
            self.use_cflags += " `pkg-config --cflags gtk+-2.0` "
        
        self.use_cflags += " " + self.textCFLAGS.get_text()
        

        # pega os parametros de ldflags
        #
        self.use_ldflags = ""
        if self.checkMath.get_active():
            self.use_ldflags += " -lm "
        if self.checkOpenGL.get_active():
            self.use_ldflags += " -lglut -lGL -lGLU "
        if self.checkGLEW.get_active():
            self.use_ldflags += " -lGLEW "
        if self.checkX11.get_active():
            self.use_ldflags += " -lXmu -lXi -lXext -lX11 "
        if self.checkOpenMP.get_active():
            self.use_ldflags += " -fopenmp"     # em CFLAGS tambem
        if self.checkProfiling.get_active():
            self.use_ldflags += " -pg"          # em CFLAGS tambem
        if self.checkGTK.get_active():
            self.use_ldflags += " `pkg-config --libs gtk+-2.0` "

        self.use_ldflags += " " + self.textLDFLAGS.get_text()


        # lê o resto dos campos antes de a janela ser destruída
        #
        self.makefile_prog_name = self.textPrograma.get_text()
        self.makefile_check_openmpi = self.checkOpenMPI.get_active()
        self.makefile_check_profiling = self.checkProfiling.get_active()


        # fecha a janela
        #
        self.windowMakefile.destroy()
        gtk.main_quit()

        # gera um Makefile conforme os dados da janela
        #
        self.makefile_generate()

        # roda com o Makefile gerado!
        #
        self.makefile_run( rebuilding = False )



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


    def on_dlg_makefile_add_all(self, *args):

        # remove tudo de 'arquivos 1' e 'arquivos 2'
        self.storeArquivos1.clear()
        self.storeArquivos2.clear()
        
        # adiciona cada arquivo-fonte em 'arquivos 1'        
        for f in self.fontes:
            it = self.storeArquivos1.append()
            self.storeArquivos1.set( it, 0, f )


    def on_dlg_makefile_del_all(self, *args):

        # remove tudo de 'arquivos 1' e 'arquivos 2'
        self.storeArquivos1.clear()
        self.storeArquivos2.clear()
        
        # adiciona cada arquivo-fonte em 'arquivos 2'        
        for f in self.fontes:
            it = self.storeArquivos2.append()
            self.storeArquivos2.set( it, 0, f )


    def makefile_generate(self):

        makefile = self.default_makefile_from_src()
        mdir = self.src.get_dir()

        f = open( makefile, "w" )
        
        # parte basica inicial
        #
        
        f.write( "PROGRAMA = " + self.makefile_prog_name + "\n" )
        f.write( "FONTES = " + self.fontes_marcados + "\n" )

        f.write( "\n" )
        f.write( "CFLAGS = " + self.use_cflags + "\n" )
        f.write( "LDFLAGS = " + self.use_ldflags + "\n" )

        
        # parte 1
        #
        
        if self.makefile_check_openmpi:
            if self.usando_c:
                f.write( makefile_1_c_mpi )
            else:
                f.write( makefile_1_cpp_mpi )
        else:
            if self.usando_c:
                f.write( makefile_1_c )
            else:
                f.write( makefile_1_cpp )

        # parte 2
        #        
        f.write( makefile_2_common )
        
        
        # parte 3
        #
        if self.usando_c:
            f.write( makefile_3_c )
        else:
            f.write( makefile_3_cpp )
        
        
        # parte 4
        #        
        f.write( makefile_4_common )
        
        
        # parte 5
        #
        if self.makefile_check_openmpi:
            f.write( makefile_5_mpi )
        else:
            f.write( makefile_5_default )
            
        
        # parte 6 (opcional)
        #
        if self.makefile_check_profiling:
            f.write( makefile_6_profiling )
            

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

        # existe o arquivo de makefile?
        #
        if not self.any_makefile_exists():
            print "Makefile não encontrado"
            
            msgbox(
                "Rodar Programa",
                "Não foi encontrado um arquivo de Makefile no diretório.\n" +
                "Por causa disso, não é possível rodar o código atual.",
                "erro"
            )
            return



        # descobre o comando de 'make exec' que deve-se fazer pra
        # rodar o projeto (c / c++)
        #

        makeExecTarget = configurations.cmd_make_exec
        if makeExecTarget == '':
            makeExecTarget = "exec"


        # existe o target 'exec' no makefile em questao?
        #
        found_exec = False
        alt_target = makeExecTarget + "_" + self.src.get_filename_without_path_and_ext()
        
        makefile_lines = self.get_makefile_contents()
        for line in makefile_lines:
            if line[0:5] == 'exec:':
                found_exec = True
                break
            elif line[0: len(alt_target)+1] == alt_target + ':':
                found_exec = True
                makeExecTarget = alt_target
                break
                
        if not found_exec:
            print "Makefile encontrado, mas sem '%s' ou '%s'" % (makeExecTarget, alt_target)
            
            msgbox(
                "Rodar Programa",
                ("Não foi encontrado '%s' ou '%s' no Makefile no diretório.\n" %
                    (makeExecTarget, alt_target) ) +
                "Por causa disso, não é possível rodar o código atual.",
                "erro"
            )
            return
            
        
        #print "Makefile encontrado com '%s', executando..." % makeExecTarget
        
        cmd = "make " + makeExecTarget
        roda_cmd_on_dir( cmd, self.src.get_dir(), \
            auto_close = configurations.run_auto_close_window )



    def make_clean(self):

        # o arquivo makefile existe?

        if self.any_makefile_exists():

            p = CmdProcess()
            p.run_cmd_on_dir( "make clean", self.src.get_dir() )

            if configurations.make_auto_close_window:
                p.imgResult.set_from_file( IMG_RESULT_CLEAN )
                p.imgResult.show()
                p.start_auto_close()                
            return


        # o arquivo makefile nao existe...

        msgbox(
            "Make Clean",
            "Não foi encontrado um arquivo de Makefile no diretório.\n" +
            "Por causa disso, não é possível executar <i>make clean</i>.",
            "erro"
        )
